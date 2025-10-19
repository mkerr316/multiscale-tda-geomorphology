"""
Quick test script to verify the restructured src/ directory works correctly.

Run this from the project root:
    python test_imports.py
"""

import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

print("=" * 70)
print("TESTING RESTRUCTURED SRC/ IMPORTS")
print("=" * 70)

# Test data_acquisition imports
print("\n1. Testing data_acquisition module...")
try:
    from data_acquisition import (
        DaymetAcquisition,
        Gnatsgo,
        build_dem_download_jobs_stac,
        execute_downloads
    )
    print("   OK data_acquisition imports successful")
    print(f"      - DaymetAcquisition: {DaymetAcquisition}")
    print(f"      - Gnatsgo: {Gnatsgo}")
except ImportError as e:
    print(f"   FAILED: {e}")
    sys.exit(1)

# Test io imports
print("\n2. Testing io module...")
try:
    from io import write_provenance, get_git_commit, safe_union_all, ensure_crs
    print("   ✅ io imports successful")
    print(f"      - write_provenance: {write_provenance}")
    print(f"      - safe_union_all: {safe_union_all}")
except ImportError as e:
    print(f"   ❌ FAILED: {e}")
    sys.exit(1)

# Test utils imports
print("\n3. Testing utils module...")
try:
    from utils import (
        setup_colored_logging,
        get_key_from_sw_corner,
        get_bbox_from_key
    )
    print("   ✅ utils imports successful")
    print(f"      - setup_colored_logging: {setup_colored_logging}")
    print(f"      - get_key_from_sw_corner: {get_key_from_sw_corner}")
except ImportError as e:
    print(f"   ❌ FAILED: {e}")
    sys.exit(1)

# Test backward compatibility
print("\n4. Testing backward compatibility (top-level imports)...")
try:
    # These should work via src/__init__.py
    import src
    assert hasattr(src, 'DaymetAcquisition')
    assert hasattr(src, 'write_provenance')
    assert hasattr(src, 'setup_colored_logging')
    print("   ✅ Backward compatibility successful")
    print(f"      - src.DaymetAcquisition: {src.DaymetAcquisition}")
except (ImportError, AssertionError) as e:
    print(f"   ❌ FAILED: {e}")
    sys.exit(1)

# Test coordinate utilities
print("\n5. Testing coordinate utilities...")
try:
    key = get_key_from_sw_corner(-85, 33)
    bbox = get_bbox_from_key(key)
    assert key == "n34w085"
    assert bbox == (-85.0, 33.0, -84.0, 34.0)
    print(f"   ✅ Coordinate utilities work correctly")
    print(f"      - get_key_from_sw_corner(-85, 33) = '{key}'")
    print(f"      - get_bbox_from_key('{key}') = {bbox}")
except Exception as e:
    print(f"   ❌ FAILED: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print("\nThe restructured src/ directory is working correctly.")
print("You can now run notebook 1.2 to download data.")
