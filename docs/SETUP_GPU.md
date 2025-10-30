# GPU Setup Guide for TDA Geomorphology Project

This guide explains how to enable GPU acceleration for the multiscale TDA geomorphology project. GPU acceleration can provide **5-10x speedups** for DEM processing, rasterization, and mosaicking operations.

## Table of Contents
- [Do I Need GPU Support?](#do-i-need-gpu-support)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Testing GPU Access](#testing-gpu-access)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Performance Expectations](#performance-expectations)

---

## Do I Need GPU Support?

**GPU acceleration is OPTIONAL.** The project works perfectly fine on CPU-only systems.

**You might want GPU if:**
- You're processing CONUS-scale datasets (10,000+ HUC12 watersheds)
- You're doing intensive raster operations (mosaicking, resampling)
- You have an NVIDIA GPU with at least 8 GB VRAM

**You DON'T need GPU if:**
- You're working with pilot datasets (<100 watersheds)
- You only have CPU hardware (project auto-detects and uses CPU)
- You're on macOS (Apple GPUs not supported by CUDA)

---

## Prerequisites

### Hardware Requirements
- **NVIDIA GPU** with Compute Capability 6.0+ (Pascal architecture or newer)
  - Examples: GTX 1060, RTX 2060/3060/4060, Tesla T4, A100
- **Minimum 8 GB VRAM** (16+ GB recommended for CONUS-scale processing)
- Check your GPU: https://developer.nvidia.com/cuda-gpus

### Software Requirements (Host Machine)

#### Linux (Ubuntu/Debian)
```bash
# 1. NVIDIA Driver (version >= 525 for CUDA 12.1)
nvidia-smi  # Should show driver version

# If not installed:
sudo apt update
sudo apt install nvidia-driver-525  # Or latest version
sudo reboot

# 2. NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update
sudo apt install nvidia-container-toolkit
sudo systemctl restart docker
```

#### Windows 11 (WSL2)
```powershell
# 1. Install WSL2 with Ubuntu
wsl --install

# 2. Install NVIDIA Driver for Windows (NOT inside WSL)
# Download from: https://www.nvidia.com/Download/index.aspx
# Choose: Windows 11, Your GPU model

# 3. Inside WSL2 Ubuntu, install nvidia-container-toolkit
# (Same commands as Linux above)
```

#### macOS
**NVIDIA CUDA is NOT supported on macOS.** The project will automatically use CPU mode.
- Apple Silicon Macs (M1/M2/M3) cannot use NVIDIA CUDA
- Intel Macs with AMD GPUs cannot use CUDA
- For Mac users: All workflows run on CPU (still fast with M1/M2/M3!)

---

## Installation

### Step 1: Verify NVIDIA Driver
```bash
nvidia-smi
```

**Expected Output:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.xx.xx    Driver Version: 525.xx.xx    CUDA Version: 12.1    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0  On |                  N/A |
|  0%   45C    P8    10W / 350W |    500MiB / 24576MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
```

**If this fails:**
- Driver not installed → Install NVIDIA driver (see Prerequisites)
- `nvidia-smi: command not found` → Check PATH or reinstall driver

### Step 2: Verify Docker GPU Access
```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

**Expected:** Same output as Step 1, but running inside Docker container.

**If this fails:**
- `could not select device driver` → Install nvidia-container-toolkit
- `unknown flag: --gpus` → Update Docker to version 19.03+

### Step 3: Rebuild Docker Image with GPU Support
```bash
# Navigate to project root
cd /path/to/multiscale_tda_geomorphology

# Build image (environment.yml includes GPU packages)
docker-compose build

# This installs: PyTorch with CUDA 12.1, CuPy, dask-cuda
```

---

## Testing GPU Access

### Quick Test: GPU Detection in Python
```bash
# Start container with GPU access
docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up -d

# Open Python shell
docker exec -it tda-geo-dev python

# In Python:
>>> from geo_tda.utils.gpu_detection import print_compute_summary
>>> print_compute_summary()
```

**Expected Output:**
```
============================================================
Compute Resources
============================================================
CPU: 16 physical cores (32 logical)
RAM: 64.0 GB total, 48.2 GB available
GPU: NVIDIA GeForce RTX 4090 (24.0 GB VRAM)
     23.5 GB VRAM available
     CUDA 12.1, Compute Capability 8.9
============================================================
```

### Test GPU Computation with CuPy
```python
import cupy as cp
import numpy as np

# Create array on GPU
x_gpu = cp.array([1, 2, 3, 4, 5])
print(f"Array on GPU: {x_gpu}")

# GPU computation
result = cp.sum(x_gpu ** 2)
print(f"Sum of squares (GPU): {result}")

# Benchmark: GPU vs CPU
size = 10000
x_cpu = np.random.rand(size, size)
x_gpu = cp.random.rand(size, size)

%timeit np.linalg.svd(x_cpu, full_matrices=False)  # CPU
%timeit cp.linalg.svd(x_gpu, full_matrices=False)  # GPU
```

**Expected:** GPU should be 5-50x faster for matrix operations.

---

## Usage

### Option 1: Using docker-compose (Recommended)

**With GPU:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up
```

**Without GPU (CPU-only):**
```bash
docker-compose up
```

### Option 2: Configuration in Code

The project **auto-detects** GPU availability. No code changes needed!

```python
# In your notebooks/scripts:
from geo_tda.utils.gpu_detection import detect_gpu_config

gpu_info = detect_gpu_config()
if gpu_info:
    print(f"Using GPU: {gpu_info['device_name']}")
    # GPU-accelerated code paths will be used automatically
else:
    print("Using CPU (no GPU detected)")
    # CPU code paths will be used
```

### Option 3: Force CPU Mode (Even if GPU Available)

Edit `config.yml`:
```yaml
computational:
  use_gpu: "never"  # Options: auto | force | never
```

---

## Troubleshooting

### GPU Not Detected Inside Container

**Problem:** `nvidia-smi` works on host, but not in container.

**Solution:**
```bash
# Check docker daemon config
cat /etc/docker/daemon.json

# Should contain:
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}

# If missing, add it and restart Docker:
sudo systemctl restart docker
```

### CUDA Out of Memory

**Problem:** `RuntimeError: CUDA out of memory`

**Solution 1: Reduce Chunk Size**
Edit your code or config:
```python
# Reduce chunk size for GPU operations
chunks = {"x": 1024, "y": 1024}  # Instead of 2048x2048
```

**Solution 2: Clear GPU Cache**
```python
import cupy as cp
cp.get_default_memory_pool().free_all_blocks()
```

**Solution 3: Reduce Safety Factor**
Edit config.yml:
```yaml
computational:
  gpu_memory_fraction: 0.6  # Use only 60% of VRAM instead of 80%
```

### Slow GPU Performance

**Problem:** GPU is slower than CPU.

**Possible Causes:**
1. **Small data:** GPU overhead dominates for tiny datasets (<1 GB)
   - Solution: Only use GPU for large rasters (>5 GB)

2. **CPU↔GPU transfer bottleneck:** Too much data movement
   - Solution: Keep data on GPU longer, minimize `.get()` calls

3. **Wrong data type:** Using float64 instead of float32
   - Solution: Cast to float32 before GPU operations

```python
# Good: Minimize transfers
dem_gpu = cp.asarray(dem_cpu)  # Once
slope = compute_slope(dem_gpu)
aspect = compute_aspect(dem_gpu)
result_cpu = slope.get()  # Once at the end

# Bad: Multiple transfers
for i in range(100):
    chunk_gpu = cp.asarray(chunk_cpu[i])  # Transfer!
    result = process(chunk_gpu)
    result_cpu = result.get()  # Transfer back!
```

### WSL2-Specific Issues

**Problem:** `WSLg: DRM_IOCTL_I915_GEM_MMAP_GTT failed: Permission denied`

**Solution:** Ignore this warning (cosmetic). Add to `.bashrc`:
```bash
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
```

**Problem:** GPU memory appears as 0 MB.

**Solution:** Update WSL:
```powershell
# In PowerShell (as Administrator)
wsl --update
wsl --shutdown
# Restart WSL
```

---

## Performance Expectations

### What GPU Accelerates in This Project

| Operation | CPU Time (est) | GPU Time (est) | Speedup |
|-----------|----------------|----------------|---------|
| DEM flow direction (1000x1000 km, 10m) | 30 min | 3-5 min | 6-10x |
| Slope/aspect calculation (CONUS) | 20 min | 2-4 min | 5-10x |
| Rasterization (5000 HUC12s) | 15 min | 2-3 min | 5-7x |
| Mosaicking (1000 tiles) | 40 min | 5-8 min | 5-8x |
| **Total CONUS DEM pre-processing** | **~2 hours** | **~15-20 min** | **6-8x** |

### What GPU Does NOT Accelerate

| Operation | Reason |
|-----------|--------|
| WEPP binary execution | Fortran code, not GPU-compatible |
| API calls (SSURGO, PRISM) | Network I/O bound |
| Small rasters (<1 GB) | GPU overhead > benefit |
| File I/O operations | Disk speed is the bottleneck |

### Recommended GPU Specs by Use Case

| Use Case | Min GPU | Recommended GPU | VRAM |
|----------|---------|-----------------|------|
| Pilot (100 HUC12s) | GTX 1660 | RTX 3060 | 8 GB |
| Regional (1000 HUC12s) | RTX 3060 | RTX 4070 | 12 GB |
| CONUS (5000+ HUC12s) | RTX 4070 | RTX 4090 / A6000 | 24+ GB |

---

## Additional Resources

### Documentation
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
- CuPy User Guide: https://docs.cupy.dev/en/stable/user_guide/
- Dask-CUDA: https://docs.rapids.ai/api/dask-cuda/stable/

### Checking GPU Compatibility
- CUDA GPUs List: https://developer.nvidia.com/cuda-gpus
- Check Compute Capability: https://developer.nvidia.com/cuda-gpus

### Getting Help
- Project Issues: https://github.com/your-username/multiscale_tda_geomorphology/issues
- NVIDIA Forums: https://forums.developer.nvidia.com/

---

## Summary Checklist

- [ ] NVIDIA driver installed (version >= 525)
- [ ] `nvidia-smi` works on host
- [ ] `nvidia-container-toolkit` installed
- [ ] Docker test passes: `docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi`
- [ ] Container built with GPU support: `docker-compose build`
- [ ] Python GPU detection works: `from geo_tda.utils.gpu_detection import print_compute_summary`
- [ ] Started with GPU config: `docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up`

**If all checkboxes pass → You're ready to use GPU acceleration!**

**If any fail → See Troubleshooting section above**

---

*Last Updated: 2025-10-21*
*For issues or questions, open a GitHub issue or consult the project documentation.*
