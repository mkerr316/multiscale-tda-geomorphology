"""
Multiscale TDA Geomorphology Analysis Package

This package provides tools for:
- Data acquisition (climate, soil, DEM)
- Topological data analysis (TDA) on DEMs
- Geomorphometric feature extraction
- Statistical modeling and interpretation
"""

# Backward compatibility: Import commonly used functions at top level
from .data_acquisition import (
    DaymetAcquisition,
    Gnatsgo,
    build_dem_download_jobs_stac,
    execute_downloads,
)
from .geoio_utils import (
    write_provenance,
    get_git_commit,
    safe_union_all,
    ensure_crs,
)
from .utils import (
    setup_colored_logging,
    get_key_from_sw_corner,
    get_bbox_from_key,
)

__all__ = [
    'DaymetAcquisition',
    'Gnatsgo',
    'build_dem_download_jobs_stac',
    'execute_downloads',
    'write_provenance',
    'get_git_commit',
    'safe_union_all',
    'ensure_crs',
    'setup_colored_logging',
    'get_key_from_sw_corner',
    'get_bbox_from_key',
]

__version__ = '0.1.0'
