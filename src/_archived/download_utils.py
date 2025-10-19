from __future__ import annotations
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import planetary_computer
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm.auto import tqdm
from utils import write_provenance, get_key_from_sw_corner, get_bbox_from_key
from pystac_client import Client
import geopandas as gpd
from typing import List, Dict, Any

log = logging.getLogger(__name__)

# --- Global Session for HTTP Requests ---
DL_SESSION = requests.Session()
DL_SESSION.headers.update({"User-Agent": f"UGA-TDA-Geomorphology-Research/1.0"})

# --- Planetary Computer STAC Endpoint ---
PC_STAC_ENDPOINT = "https://planetarycomputer.microsoft.com/api/stac/v1"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _fetch_url_with_retry(url: str, session: requests.Session, timeout_sec: int = 60):
    """A resilient GET request wrapper using tenacity."""
    response = session.get(url, stream=True, timeout=timeout_sec)
    response.raise_for_status()
    return response


def _download_job(job: dict, stats: dict, timeout_sec: int = 60):
    """
    Worker function to download a single file, with atomic writes.

    Downloads to a temporary `.part` file and renames on success.
    """
    url, out_path = job["url"], job["out_path"]
    part_path = out_path.with_suffix(out_path.suffix + '.part')

    if out_path.exists():
        with stats["lock"]:
            stats["skipped"] += 1
        return f"SKIP (exists): {out_path.name}"

    try:
        # Use a new session for each thread for thread safety
        with requests.Session() as session:
            session.headers.update({"User-Agent": "UGA-TDA-Geomorphology-Research/1.0"})
            signed_url = planetary_computer.sign(url)
            response = _fetch_url_with_retry(signed_url, session, timeout_sec)

            with open(part_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

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
    Execute download jobs in parallel with progress tracking.

    Args:
        jobs: List of download job dicts with 'url', 'out_path', 'key', 'source_info'
        description: Human-readable description for progress bar
        max_workers: Maximum number of concurrent download threads
    """
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


def _generate_jobs_for_source(
        aoi_wgs84: gpd.GeoDataFrame,
        source_key: str,
        config: Dict[str, Any]
) -> List[Dict]:
    """
    Generates a list of download or processing job dictionaries for a single data source.
    This function implements the data-source-specific discovery logic (e.g., STAC query).
    """
    source_conf = config['data_sources'].get(source_key)
    if not source_conf:
        log.error(f"CRITICAL: Data source '{source_key}' not found in config.yml.")
        return []

    data_type = source_conf.get('type', 'file_download')
    jobs = []

    # --- STAC-based Acquisition (e.g., DEM and future Cloud-Native Raster Data) ---
    if data_type == 'stac_collection':
        log.info(f"Starting STAC query for source: {source_key}")
        pc_url = source_conf['stac_url']
        collection_id = source_conf['collection']
        asset_key = source_conf['asset_key']
        out_dir = Path(config['paths'][source_conf['output_dir_key']])

        # Gold Standard: Use Planetary Computer Client for URL signing
        client = Client.open(pc_url, modifier=planetary_computer.sign)
        bbox_wgs84 = aoi_wgs84.bounds.iloc[0].tolist()

        search = client.search(
            collections=[collection_id],
            bbox=bbox_wgs84,
            query={"proj:epsg": {"eq": 4326}},
        )

        items = search.item_collection()  # Use item_collection()
        log.info(f"STAC search returned {len(items)} items for {source_key}.")

        for item in items:
            tile_key = item.properties.get("usgs:tile", item.id)
            out_path = out_dir / f"{source_key}_{tile_key}.tif"

            if out_path.exists(): continue
            if asset_key not in item.assets:
                log.warning(f"Tile {tile_key} missing asset '{asset_key}'. Skipping.")
                continue

            signed_url = item.assets[asset_key].href

            jobs.append({
                "url": signed_url,
                "out_path": out_path,
                "source_info": {"stac_item": item.id, "stac_url": pc_url},
                "key": tile_key,
                "type": source_key,  # Use the key to identify the type of job
            })

    # --- Other Data Types (e.g., Soil Data, Zarr/NetCDF Data) ---
    elif data_type == 'gnatsgo_sda':
        # Soil data is typically queried/processed differently (e.g., single API call)
        # You would implement the logic from pygnatsgofetch here, or have a single job
        # that executes the Gnatsgo class method (preferred if Gnatsgo is a complex class)

        # NOTE: For the purpose of demonstration, we'll keep the Gnatsgo class separate
        # and assume the acquisition step in 1.2 calls the class directly, but if
        # you wanted full abstraction, you would integrate the logic here.
        log.warning("gNATSGO/SDA logic is executed via the pygnatsgofetch class and is skipped in this job generator.")
        pass

    elif data_type == 'zarr_subset':
        # Daymet data acquisition would be a single job entry that calls the complex
        # xarray subsetting logic, as it's not a parallel tile download.
        log.warning("Daymet Zarr subsetting is a single large job and is skipped in this tile generator.")
        pass

    else:
        log.warning(f"Unrecognized data type '{data_type}' for source '{source_key}'. Skipping.")

    return jobs


def build_dem_download_jobs_stac(
        keys_to_find: List[str],
        stac_url: str,
        collection_id: str,
        asset_key: str,
        out_dir: Path
) -> tuple[List[Dict], List[str]]:
    """
    Probes the Planetary Computer STAC API for valid DEM URLs based on calculated tile keys.
    The returned URLs are NOT pre-signed; signing happens just-in-time in _download_job.

    Args:
        keys_to_find: List of H-K keys (e.g., 'n34w118') for missing tiles.
        stac_url: The URL of the STAC catalog (e.g., PC_STAC_URL).
        collection_id: The STAC collection ID (e.g., 'usgs-3dep-dem').
        asset_key: The asset key holding the GeoTIFF ('data' or 'cog').
        out_dir: The local directory to save the files.

    Returns:
        A tuple of (jobs: list[dict], not_found_keys: list[str]).
    """
    jobs, not_found_keys = [], []
    log.info(f"Connecting to STAC Catalog at: {stac_url}")
    # CRITICAL: Do NOT sign here. The general downloader signs all PC assets.
    # We open anonymously or with no modifier since we are just doing item discovery.
    catalog = Client.open(stac_url)

    log.info(f"Querying STAC for {len(keys_to_find)} missing DEM tiles from collection '{collection_id}'...")

    # We will query all tiles together by concatenating their bounding boxes (an optimization).
    # Create a collective bounding box to reduce API calls (optional optimization)
    # The current notebook structure, however, iterates over keys one-by-one. We will keep
    # the original iteration structure to align with the existing notebook logic.

    for key in tqdm(keys_to_find, desc="STAC Query", unit="key"):
        try:
            bbox = get_bbox_from_key(key)

            # Use item_collection() as per gold-standard instructions
            search = catalog.search(
                collections=[collection_id],
                bbox=bbox,
                datetime=None  # No temporal filter for static DEMs
            )
            items = search.item_collection()

            if not items:
                not_found_keys.append(key)
                continue

            # Assuming the first item is the most relevant, often the case for tile searches
            item = items[0]

            if asset_key not in item.assets:
                log.warning(f"Tile {key} missing asset '{asset_key}'. Skipping.")
                not_found_keys.append(key)
                continue

            asset_url = item.assets[asset_key].href

            filename = f"USGS_1_{key}.tif"  # Use the naming scheme from original logic
            out_path = out_dir / filename

            # Note: The URL is UN-signed here, it will be signed just-in-time in _download_job
            jobs.append({
                "url": asset_url,  # Original, unsigned URL
                "out_path": out_path,
                "key": key,
                "source_info": {
                    "stac_url": stac_url,
                    "collection": collection_id,
                    "item_id": item.id,
                    "asset_key": asset_key,
                    "original_href": asset_url
                }
            })
        except Exception as e:
            log.error(f"ERROR: Failed to query STAC for key {key}: {e}", exc_info=True)
            not_found_keys.append(key)

    log.info(f"STAC search completed. Found {len(jobs)} jobs. {len(not_found_keys)} keys were not found.")
    return jobs, not_found_keys