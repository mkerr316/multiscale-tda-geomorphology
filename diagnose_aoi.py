"""
Diagnostic script to understand the Master AOI extent issue
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import geopandas as gpd
import math

# Load the master AOI
aoi_path = Path(__file__).parent / 'data' / 'processed' / 'master_aoi.gpkg'
master_aoi = gpd.read_file(aoi_path, layer='master_aoi')

print('=' * 70)
print('MASTER AOI DIAGNOSTIC')
print('=' * 70)
print(f'Master AOI CRS: {master_aoi.crs}')
print(f'Master AOI shape: {master_aoi.shape}')
print(f'Geometry type: {master_aoi.geometry.type.unique()}')
print(f'Bounds (native CRS): {master_aoi.total_bounds}')

# Convert to WGS84 to see lat/lon bounds
master_aoi_wgs84 = master_aoi.to_crs('EPSG:4326')
print(f'\nIn WGS84 (EPSG:4326):')
minx, miny, maxx, maxy = master_aoi_wgs84.total_bounds
print(f'  Bounds: {master_aoi_wgs84.total_bounds}')
print(f'  Longitude: [{minx:.6f}, {maxx:.6f}] (span: {maxx-minx:.6f}°)')
print(f'  Latitude:  [{miny:.6f}, {maxy:.6f}] (span: {maxy-miny:.6f}°)')

# Calculate approximate area in km²
avg_lat = (miny + maxy) / 2
km_per_deg_lon = 111.32 * math.cos(math.radians(avg_lat))
km_per_deg_lat = 110.54
bbox_width_km = (maxx - minx) * km_per_deg_lon
bbox_height_km = (maxy - miny) * km_per_deg_lat
approx_bbox_area_km2 = bbox_width_km * bbox_height_km

print(f'\nBounding Box Dimensions:')
print(f'  Width:  {bbox_width_km:,.0f} km')
print(f'  Height: {bbox_height_km:,.0f} km')
print(f'  Bounding box area: {approx_bbox_area_km2:,.0f} km²')

# Calculate actual geometry area
actual_area_m2 = master_aoi.to_crs('EPSG:5070').area.sum()  # Albers equal area
actual_area_km2 = actual_area_m2 / 1e6
print(f'  Actual geometry area: {actual_area_km2:,.0f} km²')
print(f'  Waste factor: {approx_bbox_area_km2 / actual_area_km2:.1f}x')

# Daymet grid resolution is 1km
print(f'\nDaymet Grid Calculations (1km resolution):')
daymet_y_cells = int(bbox_height_km)
daymet_x_cells = int(bbox_width_km)
print(f'  Expected grid cells: y={daymet_y_cells}, x={daymet_x_cells}')
print(f'  Your actual download: y=2505, x=5194')

# Calculate data size
time_steps = 1095  # 3 years
num_vars = 7  # Daymet has 7 daily variables
bytes_per_value = 4  # float32
total_elements = time_steps * 2505 * 5194 * num_vars
total_gb = total_elements * bytes_per_value / (1024**3)
print(f'\nData Volume:')
print(f'  Time steps: {time_steps}')
print(f'  Variables: {num_vars}')
print(f'  Total cells: {time_steps:,} × 2505 × 5194 × {num_vars} = {total_elements:,}')
print(f'  Total size: {total_gb:.1f} GB')

print('\n' + '=' * 70)
print('RECOMMENDATION:')
print('=' * 70)
print(f'Your bounding box is {approx_bbox_area_km2 / actual_area_km2:.1f}x larger than your actual study areas!')
print('This is why you\'re downloading 955 GB instead of a reasonable amount.')
print('\nSuggested fixes:')
print('1. Create a buffered version of your actual study provinces (e.g., 10km buffer)')
print('2. Download climate data for each province separately, then merge')
print('3. Add a max extent check to prevent accidental massive downloads')
print('=' * 70)
