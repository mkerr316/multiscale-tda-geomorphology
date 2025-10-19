# src/data_acquisition/download_core.py

from __future__ import annotations
import logging
import threading
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import planetary_computer
import requests
import rasterio
from rasterio.warp import transform_bounds
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm.auto import tqdm

# Assuming these utilities exist from your project structure
from src.geoio_utils.provenance import write_provenance
from src.utils.coords import get_bbox_from_key

log = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _fetch_url_with_retry(url: str, session: requests.Session, timeout_sec: int = 60):
    """A resilient GET request wrapper using tenacity."""
    # Sign the request if it's a planetary computer URL
    signed_url = planetary_computer.sign(url)
    response = session.get(signed_url, stream=True, timeout=timeout_sec)
    response.raise_for_status()
    return response


def _validate_geotiff_content(file_path: Path, expected_key: str) -> tuple[bool, str]:
    """
    Validates that a GeoTIFF's geographic bounds match the expected tile key.

    This is the core of the fix. It prevents data duplication by ensuring the
    downloaded content is geographically correct.

    Args:
        file_path: Path to the downloaded GeoTIFF file.
        expected_key: The USGS tile key we expected to download (e.g., 'n45w094').

    Returns:
        A tuple of (is_valid, message).
    """
    try:
        expected_bbox_wgs84 = get_bbox_from_key(expected_key)

        with rasterio.open(file_path) as src:
            # Transform raster bounds to WGS84 for a consistent comparison
            actual_bbox_wgs84 = transform_bounds(
                src.crs, "EPSG:4326", *src.bounds
            )

            # Compare with a tolerance to account for float precision issues
            for actual, expected in zip(actual_bbox_wgs84, expected_bbox_wgs84):
                if not abs(actual - expected) < 1e-6:
                    return (
                        False,
                        f"Bounds mismatch for key {expected_key}. "
                        f"Expected {expected_bbox_wgs84}, got {actual_bbox_wgs84}."
                    )
            return True, f"Bounds validated for key {expected_key}."

    except Exception as e:
        return False, f"Validation failed for {file_path.name} with error: {e}"


def _download_job(job: dict, stats: dict) -> str:
    """Target function for a single download thread."""
    url = job["url"]
    out_path = Path(job["out_path"])
    key = job["key"]
    part_path = out_path.with_suffix(out_path.suffix + ".part")
    success = False

    try:
        if out_path.exists() and out_path.stat().st_size > 0:
            is_valid, _ = _validate_geotiff_content(out_path, key)
            if is_valid:
                with stats["lock"]:
                    stats["skipped"] += 1
                return f"SKIP: {out_path.name} (already exists and is valid)"

        part_path.parent.mkdir(parents=True, exist_ok=True)
        with requests.Session() as session:
            response = _fetch_url_with_retry(url, session)
            with open(part_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        # --- NEW VALIDATION STEP ---
        is_valid, msg = _validate_geotiff_content(part_path, key)
        if not is_valid:
            log.error(f"Validation failed for {out_path.name}: {msg}")
            raise ValueError(msg) # Raise error to trigger failure logic

        part_path.rename(out_path)
        write_provenance(out_path, job["source_info"])
        success = True
        return f"OK: {out_path.name}"

    except Exception as e:
        log.error(f"Download failed for {out_path.name}: {e}")
        # Clean up partial file on failure
        if part_path.exists():
            part_path.unlink()
        return f"FAIL: {out_path.name} ({e})"

    finally:
        with stats["lock"]:
            if success:
                stats["downloaded"] += 1
            else:
                stats["failed"] += 1


def parallel_download(jobs: list[dict], description: str, max_workers: int):
    """
    Manages a pool of threads to download a list of files concurrently.
    """
    if not jobs:
        log.info(f"No new files to download for {description}.")
        return

    stats = {
        "lock": threading.Lock(),
        "skipped": 0,
        "downloaded": 0,
        "failed": 0,
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
                unit="file",
            )
        ]

    # Report statistics
    failures = [r for r in results if r.startswith("FAIL")]
    log.info("=" * 70)
    log.info(f"Download Summary for {description}:")
    log.info(f"  Downloaded: {stats['downloaded']}")
    log.info(f"  Skipped:    {stats['skipped']} (valid files already exist)")
    log.info(f"  Failed:     {stats['failed']} (includes validation failures)")
    log.info("=" * 70)

    if failures:
        log.error("--- Download Failures ---")
        for f in failures:
            log.error(f"  - {f}")