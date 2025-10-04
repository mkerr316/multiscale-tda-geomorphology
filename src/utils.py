import math
import json
import re
import datetime
import subprocess
import logging
import sys
from pathlib import Path

class ColoredFormatter(logging.Formatter):
    """A custom formatter to add colors to log levels."""

    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    # The format string for the log message
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + log_format + RESET,
        logging.INFO: GREY + log_format + RESET,
        logging.WARNING: YELLOW + log_format + RESET,
        logging.ERROR: RED + log_format + RESET,
        logging.CRITICAL: BOLD_RED + log_format + RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_colored_logging(level=logging.INFO):
    """
    Configures the root logger to output colored logs to the console.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove any existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create a new stream handler for stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColoredFormatter())

    # Add the new handler to the root logger
    root_logger.addHandler(handler)
    logging.basicConfig(level=level, handlers=[handler], force=True)

def get_git_commit() -> str:
    """Gets the current git commit hash."""
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except Exception:
        return "not-a-git-repo"

def write_provenance(artifact_path: Path, source_info: dict, parameters: dict):
    """Writes a metadata sidecar file for a generated artifact."""
    meta = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "code_version": {
            "git_commit": get_git_commit()
        },
        "source_data": source_info,
        "processing_parameters": parameters,
    }
    meta_path = artifact_path.with_suffix(artifact_path.suffix + ".meta.json")
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)

    logging.getLogger("provenance").info(f"Wrote provenance to {meta_path.name}")

def get_key_from_sw_corner(lon: int, lat: int) -> str:
    """
    Generates the standard USGS 1x1 degree DEM tile key from its south-west corner integer coordinates.
    Example: (lon=-85, lat=33) -> 'n34w085'
    """
    ns = 'n' if lat >= 0 else 's'
    ew = 'w' if lon < 0 else 'e'
    # The key uses the northern latitude and western longitude bounds.
    lat_key = abs(lat) + 1 if ns == 'n' else abs(lat)
    lon_key = abs(lon) if ew == 'w' else abs(lon) - 1

    return f"{ns}{int(lat_key):02d}{ew}{int(lon_key):03d}"

def get_bbox_from_key(key: str) -> tuple[float, float, float, float]:
    """
    Calculates the bounding box from a standard USGS 1x1 degree DEM tile key.
    The key represents the NW corner of the tile.
    Example: 'n34w085' -> (-85.0, 33.0, -84.0, 34.0)
    """
    match = re.match(r"(n|s)(\d{2})(w|e)(\d{3})", key)
    if not match:
        raise ValueError(f"Invalid DEM key format: {key}")

    ns, lat_str, ew, lon_str = match.groups()
    lat_bound = int(lat_str)
    lon_bound = int(lon_str)

    if ns == 'n':
        max_lat = float(lat_bound)
        min_lat = float(lat_bound - 1)
    else: # ns == 's'
        max_lat = float(-lat_bound + 1)
        min_lat = float(-lat_bound)

    if ew == 'w':
        min_lon = float(-lon_bound)
        max_lon = float(-lon_bound + 1)
    else: # ew == 'e'
        min_lon = float(lon_bound)
        max_lon = float(lon_bound + 1)

    return (min_lon, min_lat, max_lon, max_lat)
