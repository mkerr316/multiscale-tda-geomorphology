# src/geoio.py
# -*- coding: utf-8 -*-
"""
Reusable Geo I/O and geometry utilities for the Multiscale TDA Geomorphology project.

Functions are intentionally generic so they can be reused across notebooks and batch scripts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple, Union

import logging
import warnings

import geopandas as gpd
import numpy as np
import shapely
from shapely import make_valid, set_precision, union_all
from shapely.geometry import base as shapely_base
from pyproj import CRS

log = logging.getLogger("geoio")
if not log.handlers:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

# Public API
__all__ = [
    "read_vector",
    "write_vector",
    "detect_name_column",
    "load_and_standardize",
    "process_provinces",
    "ensure_crs",
    "fix_invalid",
    "safe_union_all",
    "to_singlepart_union",
    "dissolve_by",
    "bounds_center",
    "enforce_partition_by_order",
]

# ---- Basic I/O ----------------------------------------------------------------


def read_vector(path: Union[str, Path], layer: Optional[str] = None, columns: Optional[Sequence[str]] = None) -> gpd.GeoDataFrame:
    """
    Read a vector dataset with geopandas. Supports common drivers (SHP, GPKG, GeoJSON).
    Parameters
    ----------
    path : str | Path
        File path to read.
    layer : str | None
        Optional layer name for multi-layer containers (e.g., GPKG).
    columns : Sequence[str] | None
        Optional list of columns to keep (plus geometry).
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Vector file not found: {path}")
    gdf = gpd.read_file(path, layer=layer) if layer else gpd.read_file(path)
    if columns is not None:
        keep = [c for c in columns if c in gdf.columns]
        missing = sorted(set(columns) - set(keep))
        if missing:
            warnings.warn(f"Requested columns not found and will be ignored: {missing}")
        gdf = gdf[keep + (["geometry"] if "geometry" not in keep else [])]
    return gdf


def write_vector(
    gdf: gpd.GeoDataFrame,
    path: Union[str, Path],
    layer: Optional[str] = None,
    driver: str = "GPKG",
    overwrite: bool = True,
) -> Path:
    """
    Write a GeoDataFrame to disk. Defaults to GeoPackage.
    If overwrite=True and the file exists, it will be unlinked first (simple and reliable for single-layer writes).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite and path.exists():
        path.unlink()
    if layer is None and driver.upper() == "GPKG":
        raise ValueError("For GPKG writes, please provide a 'layer' name.")
    gdf.to_file(path, driver=driver, layer=layer) if layer else gdf.to_file(path, driver=driver)
    log.info("Wrote %s (%s%s)", path, driver, f":{layer}" if layer else "")
    return path


# ---- Schema / naming ----------------------------------------------------------


def detect_name_column(
    gdf: gpd.GeoDataFrame,
    candidates: Optional[Iterable[str]] = None,
) -> str:
    """
    Detect a best-guess name column for administrative / region names.
    Returns the FIRST matching candidate (case-insensitive).
    """
    if candidates is None:
        candidates = ("PROVINCE", "PROV_NAME", "NAME", "PROVINCENM", "STATE_NAME", "REGION")
    ups = {c.upper(): c for c in gdf.columns}
    for want in candidates:
        if want.upper() in ups:
            return ups[want.upper()]
    raise KeyError(f"Could not detect a name column. Available columns: {list(gdf.columns)}")


def load_and_standardize(
    path: Union[str, Path],
    name_field_candidates: Optional[Iterable[str]] = None,
    out_field: str = "PROVINCE",
    drop_empty: bool = True,
) -> gpd.GeoDataFrame:
    """
    Load boundaries and normalize schema → ['PROVINCE','geometry'] by default.
    - Detects a province/name column (or use name_field_candidates)
    - Uppercases/strips names
    - Repairs invalid geometries and optionally drops empty/null geometries
    """
    gdf = read_vector(path)
    name_col = detect_name_column(gdf, candidates=name_field_candidates)
    gdf = gdf[[name_col, "geometry"]].rename(columns={name_col: out_field})
    gdf[out_field] = gdf[out_field].astype(str).str.upper().str.strip()

    # Repair invalids
    if not gdf.is_valid.all():
        warnings.warn("Invalid geometries found; repairing with make_valid().")
        gdf["geometry"] = gdf["geometry"].apply(make_valid)

    if drop_empty:
        gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty].copy()

    return gdf


# ---- CRS handling -------------------------------------------------------------


def ensure_crs(
    gdf: gpd.GeoDataFrame,
    target_crs: Union[int, str, CRS],
    allow_reproject: bool = True,
) -> gpd.GeoDataFrame:
    """
    Ensure a GeoDataFrame is in the target CRS.
    - If gdf.crs is None, raises unless allow_reproject and you provide a sensible assumption (not set here).
    - If different, reprojects when allow_reproject=True.
    """
    if gdf.crs is None:
        raise ValueError("GeoDataFrame has no CRS set. Please set gdf = gdf.set_crs(...) before calling ensure_crs().")
    target = CRS.from_user_input(target_crs)
    if CRS.from_user_input(gdf.crs) == target:
        return gdf
    if not allow_reproject:
        raise ValueError(f"CRS mismatch (have {gdf.crs}, want {target}). Set allow_reproject=True to reproject.")
    return gdf.to_crs(target)


# ---- Geometry repair / union / singlepart ------------------------------------


def fix_invalid(gdf: gpd.GeoDataFrame, buffer_zero: bool = False) -> gpd.GeoDataFrame:
    """
    Repair invalid geometries with shapely.make_valid; optionally apply buffer(0) to nudge topology.
    """
    gdf = gdf.copy()
    gdf["geometry"] = gdf["geometry"].apply(make_valid)
    if buffer_zero:
        gdf["geometry"] = shapely.buffer(gdf["geometry"].values, 0)
    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty]
    return gdf


def safe_union_all(
    gdf: gpd.GeoDataFrame,
    grid_size: float = 1e-6,
    repair: bool = True,
    fallback_unary: bool = True,
) -> shapely_base.BaseGeometry:
    """
    Robust union across many polygons:
    1) shapely.union_all with a small grid_size (snapping)
    2) optional: repair + buffer(0) and try again
    3) final fallback: shapely.ops.unary_union
    """
    geoms = gdf.geometry.values
    try:
        return shapely.union_all(geoms, grid_size=grid_size)
    except Exception as e:
        log.debug("union_all(grid_size=%s) failed: %s", grid_size, e)

    if repair:
        try:
            geoms2 = shapely.buffer(shapely.make_valid(geoms), 0)
            return shapely.union_all(geoms2, grid_size=grid_size)
        except Exception as e:
            log.debug("union_all after repair failed: %s", e)

    if fallback_unary:
        from shapely.ops import unary_union as _uunion

        return _uunion(shapely.make_valid(geoms))

    # If everything fails, re-raise the first error
    raise


def to_singlepart_union(
    geom: Union[shapely_base.BaseGeometry, gpd.GeoSeries, gpd.GeoDataFrame],
    keep: str = "largest",
    crs: Optional[Union[str, CRS]] = None,
) -> shapely_base.BaseGeometry:
    """
    Convert any input (single/multi) into a single polygon:
    explode → keep largest (by area) by default.
    """
    if isinstance(geom, gpd.GeoDataFrame):
        gs = geom.geometry
        crs = geom.crs if crs is None else crs
    elif isinstance(geom, gpd.GeoSeries):
        gs = geom
        crs = geom.crs if crs is None else crs
    else:
        gs = gpd.GeoSeries([geom], crs=crs)

    gs = gs.explode(index_parts=False)
    if len(gs) == 1:
        return make_valid(gs.iloc[0])

    if keep == "largest":
        areas = gs.area.values
        idx = int(np.argmax(areas))
        return make_valid(gs.iloc[idx])

    raise ValueError(f"Unsupported keep policy: {keep!r}")


# ---- Province / region processing --------------------------------------------


def dissolve_by(
    gdf: gpd.GeoDataFrame,
    by: str,
    crs_out: Optional[Union[str, CRS]] = None,
    area_field: Optional[str] = None,
) -> gpd.GeoDataFrame:
    """
    Dissolve features by a field, optionally reproject to crs_out and compute an area column.
    """
    if by not in gdf.columns:
        raise KeyError(f"Column not found for dissolve: {by}")
    out = gdf.copy()
    if crs_out is not None:
        out = out.to_crs(crs_out)
    out = out.dissolve(by=by, as_index=False, aggfunc="first")
    if area_field:
        out[area_field] = out.geometry.area
    return out


def process_provinces(
    gdf_in: gpd.GeoDataFrame,
    province_list: Union[str, Iterable[str]],
    crs_out: Union[int, str, CRS],
    area_field: str = "AREA_SQKM",
    area_divisor: float = 1_000_000.0,
    name_field: str = "PROVINCE",
) -> gpd.GeoDataFrame:
    """
    Filter → project → dissolve by name_field and compute area.
    Parameters
    ----------
    province_list : str | Iterable[str]
        One or more province names (must match after any upstream normalization).
    crs_out : EPSG/code/CRS
        Target CRS for area computations (e.g., EPSG:5070).
    area_field : str
        Output area field name. Defaults to km² with area_divisor=1e6.
    """
    if isinstance(province_list, (str,)):
        province_list = [province_list]

    # Filter
    if name_field not in gdf_in.columns:
        raise KeyError(f"Expected column '{name_field}' not found. Columns: {list(gdf_in.columns)}")
    sel = gdf_in[gdf_in[name_field].isin(province_list)].copy()
    if sel.empty:
        raise ValueError(f"No provinces matched: {province_list}")

    # Project → dissolve
    sel = sel.to_crs(crs_out)
    dissolved = sel.dissolve(by=name_field, as_index=False, aggfunc="first")

    # Area
    dissolved[area_field] = dissolved.geometry.area / area_divisor
    return dissolved[[name_field, area_field, "geometry"]]


# ---- Convenience --------------------------------------------------------------


def bounds_center(gdf: gpd.GeoDataFrame) -> Tuple[float, float]:
    """
    Return (y, x) center of the dataset bounds (useful for Folium center).
    Works in any CRS; commonly used after to_crs(EPSG:4326).
    """
    xmin, ymin, xmax, ymax = gdf.total_bounds
    return (0.5 * (ymin + ymax), 0.5 * (xmin + xmax))

# --- Uncategorized ---

def enforce_partition_by_order(input_gdf: gpd.GeoDataFrame, order: list[str], grid_size: float) -> gpd.GeoDataFrame:
    """
    Force polygons to be a non-overlapping partition by iteratively subtracting
    the accumulated union of earlier provinces from each subsequent province.
    This ensures absolutely no spatial leakage/overlap where provinces meet.
    """
    # NOTE: This uses the modern `union_all` function implicitly via the shapely library.
    work = input_gdf.copy()
    work["geometry"] = work.geometry.apply(lambda g: set_precision(g, grid_size))
    # Assuming fix_invalid is available and robustly handles geometry issues (it is in your file)
    work = fix_invalid(work, buffer_zero=True)
    work = work.dissolve(by="PROVINCE", as_index=False)

    accum = None
    out_geoms = {}
    for prov in order:
        if work.loc[work["PROVINCE"] == prov].empty:
            raise ValueError(f"Province '{prov}' not found in the dissolved GeoDataFrame. Check for name mismatches.")

        # Extract the current geometry
        geom = work.loc[work["PROVINCE"] == prov, "geometry"].values[0]

        # Subtract the accumulated union of previous provinces
        if accum is not None and not accum.is_empty:
            geom = geom.difference(accum)

        # Ensure precision and validity after operation
        geom = make_valid(set_precision(geom, grid_size))
        out_geoms[prov] = geom

        # Update accumulator using the modern shapely.union_all() for all processed geometries
        # Note: We include the just-processed geometry in the accumulation.
        accum = geom if accum is None else make_valid(union_all([accum, geom]))

    out = work.set_index("PROVINCE").copy()
    for prov, geom in out_geoms.items():
        out.at[prov, "geometry"] = geom

    out = out.reset_index()
    # Assuming _sum_area_km2 handles projection correctly for area computation
    out["AREA_SQKM"] = out.geometry.area / 1_000_000.0
    out.set_crs(input_gdf.crs, allow_override=True, inplace=True)
    return out