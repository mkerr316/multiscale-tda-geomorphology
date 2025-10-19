"""
Verify the src/ directory structure is correct.

This doesn't import modules (which need dependencies),
it just checks the file structure.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / 'src'

print("=" * 70)
print("VERIFYING SRC/ DIRECTORY STRUCTURE")
print("=" * 70)

expected_structure = {
    'data_acquisition': ['__init__.py', 'climate.py', 'soils.py', 'dem.py', 'download_core.py'],
    'geoio_utils': ['__init__.py', 'provenance.py', 'raster.py'],
    'utils': ['__init__.py', 'logging.py', 'coords.py'],
}

all_good = True

for subdir, files in expected_structure.items():
    print(f"\nChecking {subdir}/...")
    subdir_path = SRC_DIR / subdir

    if not subdir_path.exists():
        print(f"   MISSING: {subdir}/ directory not found")
        all_good = False
        continue

    for file in files:
        file_path = subdir_path / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"   OK {file} ({size:,} bytes)")
        else:
            print(f"   MISSING: {file}")
            all_good = False

# Check main __init__.py
print(f"\nChecking src/__init__.py...")
init_file = SRC_DIR / '__init__.py'
if init_file.exists():
    size = init_file.stat().st_size
    print(f"   OK __init__.py ({size:,} bytes)")
else:
    print(f"   MISSING: src/__init__.py")
    all_good = False

# Check archived files
print(f"\nChecking _archived/...")
archived_dir = SRC_DIR / '_archived'
if archived_dir.exists():
    archived_files = list(archived_dir.glob('*.py'))
    print(f"   OK {len(archived_files)} files archived")
    for f in archived_files:
        print(f"      - {f.name}")
else:
    print(f"   Note: No _archived/ directory (OK)")

print("\n" + "=" * 70)
if all_good:
    print("SUCCESS: All expected files are present!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Restart Jupyter kernel")
    print("2. Run notebook 1.2 cells 1-9")
    print("3. Data will download with validation and atomic writes")
else:
    print("INCOMPLETE: Some expected files are missing")
    print("=" * 70)
