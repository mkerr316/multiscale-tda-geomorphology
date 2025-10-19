"""
Core download utilities with atomic writes, retry logic, and integrity validation.
"""

from __future__ import annotations
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import planetary_computer
import requests
import rasterio
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm.auto import tqdm

from geoio_utils.provenance import write_provenance

log = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _fetch_url_with_retry(url: str, session: requests.Session, timeout_sec: int = 60):
    """A resilient GET request wrapper using tenacity."""
    response = session.get(url, stream=True, timeout=timeout_sec)
    response.raise_for_status()
    return response


def _validate_geotiff(file_path: Path) -> tuple[bool, str]:
    """
    Validate that a GeoTIFF file is not corrupt or empty.

    Args:
        file_path: Path to GeoTIFF file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with rasterio.open(file_path) as src:
            # Check if file has valid dimensions
            if src.width == 0 or src.height == 0:
                return False, "Zero dimensions"

            # Check if file has valid CRS
            if src.crs is None:
                return False, "Missing CRS"

            # Try to read a small sample to ensure data is accessible
            window = rasterio.windows.Window(0, 0, min(100, src.width), min(100, src.height))
            data = src.read(1, window=window)

            # Check if data is all nodata
            if src.nodata is not None and (data == src.nodata).all():
                return False, "All nodata values"

            return True, "Valid"

    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def _download_job(job: dict, stats: dict, timeout_sec: int = 60):
    """
    Worker function to download a single file with atomic writes and validation.

    Downloads to a temporary `.part` file, validates the download,
    and only renames to final path if validation passes.
    """
    url, out_path = job["url"], job["out_path"]
    part_path = out_path.with_suffix(out_path.suffix + '.part')

    # Skip if valid file already exists
    if out_path.exists():
        is_valid, msg = _validate_geotiff(out_path)
        if is_valid:
            with stats["lock"]:
                stats["skipped"] += 1
            return f"SKIP (valid file exists): {out_path.name}"
        else:
            log.warning(f"Existing file invalid ({msg}), re-downloading: {out_path.name}")
            out_path.unlink()

    try:
        # Use a new session for each thread for thread safety
        with requests.Session() as session:
            session.headers.update({"User-Agent": "UGA-TDA-Geomorphology-Research/1.0"})
            signed_url = planetary_computer.sign(url)
            response = _fetch_url_with_retry(signed_url, session, timeout_sec)

            # Download to temporary file
            with open(part_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        # Validate the downloaded file
        is_valid, msg = _validate_geotiff(part_path)
        if not is_valid:
            log.error(f"Downloaded file failed validation: {out_path.name} ({msg})")
            part_path.unlink()
            with stats["lock"]:
                stats["failed"] += 1
            return f"FAIL: {out_path.name} | Validation failed: {msg}"

        # Atomic move to final destination
        part_path.rename(out_path)

        with stats["lock"]:
            stats["downloaded"] += 1

        # Create provenance file after successful download
        if "source_info" in job:
            write_provenance(out_path, job["source_info"], parameters={})

        return f"OK: {out_path.name}"

    except Exception as e:
        log.error(f"FAIL: {out_path.name} | Error: {e}")
        # Clean up the partial file if it exists
        if part_path.exists():
            part_path.unlink()
        with stats["lock"]:
            stats["failed"] += 1
        return f"FAIL: {out_path.name} | Error: {e}"


def execute_downloads(jobs: list, description: str, max_workers: int):
    """
    Execute download jobs in parallel with progress tracking and validation.

    Args:
        jobs: List of download job dicts with 'url', 'out_path', 'key', 'source_info'
        description: Human-readable description for progress bar
        max_workers: Maximum number of concurrent download threads
    """
    if not jobs:
        log.info(f"No new files to download for {description}.")
        return

    stats = {
        "lock": threading.Lock(),
        "skipped": 0,
        "downloaded": 0,
        "failed": 0
    }

    log.info(f"⬇️  Starting parallel download for {len(jobs)} {description} files...")

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_job = {pool.submit(_download_job, job, stats): job for job in jobs}
        results = [
            future.result()
            for future in tqdm(
                as_completed(future_to_job),
                total=len(jobs),
                desc=description,
                unit="file"
            )
        ]

    # Report statistics
    failures = [r for r in results if r.startswith("FAIL")]
    log.info("=" * 70)
    log.info(f"Download Summary for {description}:")
    log.info(f"  Downloaded: {stats['downloaded']}")
    log.info(f"  Skipped:    {stats['skipped']} (valid files already exist)")
    log.info(f"  Failed:     {stats['failed']}")
    log.info("=" * 70)

    if failures:
        log.warning(f"Completed with {len(failures)} failures:")
        for failure in failures[:5]:  # Show first 5 failures
            log.warning(f"  {failure}")
        if len(failures) > 5:
            log.warning(f"  ... and {len(failures) - 5} more")
