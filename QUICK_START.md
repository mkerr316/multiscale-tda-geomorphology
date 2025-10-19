# Quick Start: Data Acquisition

**Status**: ✅ Ready to use (all import conflicts resolved)

## What Was Fixed

### Issue: Python Built-in `io` Module Conflict
The package name `io` conflicted with Python's built-in `io` module, causing:
```
ModuleNotFoundError: No module named 'io.provenance'; 'io' is not a package
```

### Solution: Renamed to `geoio_utils`
```
src/io/          →  src/geoio_utils/
```

All imports updated throughout the codebase.

## Current Structure

```
src/
├── data_acquisition/          ✅ DEM, Daymet, gNATSGO
│   ├── climate.py            # DaymetAcquisition
│   ├── soils.py              # Gnatsgo
│   ├── dem.py                # build_dem_download_jobs_stac
│   └── download_core.py      # execute_downloads + validation
│
├── geoio_utils/              ✅ I/O utilities (renamed from 'io')
│   ├── provenance.py         # write_provenance, get_git_commit
│   └── raster.py             # safe_union_all, ensure_crs
│
└── utils/                    ✅ General utilities
    ├── logging.py            # setup_colored_logging
    └── coords.py             # get_key_from_sw_corner, get_bbox_from_key
```

## How to Run Notebook 1.2

### 1. Verify Structure
```bash
python verify_structure.py
```

Should show:
```
✅ SUCCESS: All expected files are present!
```

### 2. Restart Jupyter Kernel

**IMPORTANT**: Click `Kernel → Restart Kernel` to clear cached imports

### 3. Run Cells 1-9

**Cell 1** - Imports (should work now):
```python
from data_acquisition import DaymetAcquisition, Gnatsgo, ...
from geoio_utils import write_provenance, safe_union_all, ...
from utils import setup_colored_logging, ...
```

**Expected output**:
```
======================================================================
DATA ACQUISITION SETUP
======================================================================
✅ Setup complete.
```

**Cells 2-7** - DEM acquisition
**Cell 8** - Daymet acquisition
**Cell 9** - gNATSGO acquisition

## Key Features

### ✅ File Validation
- DEM files validated before acceptance
- Corrupt files automatically re-downloaded
- Valid files skipped (no unnecessary downloads)

### ✅ Atomic Downloads
- Downloads to `.part` files
- Validates before renaming
- Auto-cleanup on failure

### ✅ Token Management
- Daymet data computed before writing
- Prevents Azure auth token expiration

### ✅ Comprehensive Logging
```
======================================================================
Download Summary for DEM Tiles:
  Downloaded: 45
  Skipped:    337 (valid files already exist)
  Failed:     0
======================================================================
```

## Troubleshooting

### Still seeing import errors?

1. **Restart kernel** (cached imports from old structure)
2. **Check sys.path**:
   ```python
   import sys
   print(PROJECT_ROOT / 'src' in sys.path)  # Should be True
   ```

### Validation failures?

- **Re-run cell**: Atomic downloads will retry
- **Check disk space**: Low space causes partial writes
- **Check network**: Intermittent connections cause corruption

## Documentation

- **[SRC_RESTRUCTURE_COMPLETE.md](docs/SRC_RESTRUCTURE_COMPLETE.md)** - Full details
- **[PROPOSED_SRC_STRUCTURE.md](docs/PROPOSED_SRC_STRUCTURE.md)** - Future structure
- **[Project Proposal Fall 2025.md](docs/Project Proposal Fall 2025.md)** - 15-week plan

## Success Checklist

When notebook 1.2 completes successfully:

✅ **382 DEM tiles** validated (or documented as unavailable)
✅ **Daymet .zarr** with all variables (2018-2022)
✅ **gNATSGO CSV** with merged component+horizon data
✅ **Provenance files** (.meta.json) for all artifacts
✅ **No corrupt files** in output directories

---

**Ready?** Restart your kernel and run notebook 1.2! 🚀
