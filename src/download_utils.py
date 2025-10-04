from __future__ import annotations
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import planetary_computer
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm.auto import tqdm

from utils import write_provenance

log = logging.getLogger(__name__)

# --- Global Session for HTTP Requests ---
DL_SESSION = requests.Session()
DL_SESSION.headers.update({"User-Agent": f"UGA-TDA-Geomorphology-Research/1.0"})


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _fetch_url_with_retry(url: str, session: requests.Session, timeout_sec: int = 60):
    """A resilient GET request wrapper using tenacity."""
    response = session.get(url, stream=True, timeout=timeout_sec)
    response.raise_for_status()
    return response


def _download_job(job: dict, stats: dict, timeout_sec: int = 60):
    """
    Worker function to download a single file with atomic writes and provenance.
    Handles just-in-time URL signing for Planetary Computer assets.
    """
    url, out_path = job["url"], job["out_path"]
    if out_path.exists():
        with stats["lock"]: stats["skipped"] += 1
        return f"SKIP (exists): {out_path.name}"

    # --- Just-In-Time URL Signing for DEMs ---
    # A DEM job is identified by the presence of 'original_href' in its source_info.
    is_dem_job = "original_href" in job.get("source_info", {})
    download_url = planetary_computer.sign(url) if is_dem_job else url

    try:
        r = _fetch_url_with_retry(download_url, DL_SESSION, timeout_sec)
        tmp_path = out_path.with_suffix(out_path.suffix + ".part")
        with open(tmp_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20): f.write(chunk)
        tmp_path.rename(out_path)
        write_provenance(out_path, job["source_info"], {"tile_key": job["key"]})
        return f"OK: {out_path.name}"
    except Exception as e:
        # Log the original, unsigned URL for easier debugging if it's a DEM job
        log_url = url if is_dem_job else download_url
        log.error(f"Failed to download {log_url} after multiple retries: {e}")
        return f"FAIL: {out_path.name} ({e})"


def execute_downloads(jobs: list, description: str, max_workers: int):
    """Executes a list of download jobs in parallel with a progress bar."""
    if not jobs:
        log.info(f"No new files to download for {description}.")
        return

    stats = {"lock": threading.Lock(), "skipped": 0}
    log.info(f"⬇️  Starting parallel download for {len(jobs)} {description} files...")

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_job = {pool.submit(_download_job, job, stats): job for job in jobs}
        results = [future.result() for future in tqdm(as_completed(future_to_job), total=len(jobs), desc=description, unit="file")]

    failures = [r for r in results if r.startswith("FAIL")]
    if failures: log.warning(f"Completed with {len(failures)} failures.")
    log.info(f"✅ Download process complete. Skipped {stats['skipped']} existing files.")