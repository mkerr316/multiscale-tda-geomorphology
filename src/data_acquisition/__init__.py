"""
Data acquisition module for climate, soil, and DEM data.

This module provides robust, cloud-native acquisition of geospatial data
with atomic writes, authentication handling, and integrity validation.
"""

from .dem import build_dem_download_jobs_stac
from .download_core import execute_downloads

__all__ = [
    'DaymetAcquisition',
    'Gnatsgo',
    'build_dem_download_jobs_stac',
    'execute_downloads',
]
