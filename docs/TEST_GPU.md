# GPU Testing Checklist

Quick reference for testing GPU setup after following [SETUP_GPU.md](SETUP_GPU.md).

## Pre-Requisites Test

### 1. NVIDIA Driver (Host Machine)
```bash
nvidia-smi
```

**Expected:** Shows GPU name, driver version, CUDA version.

**If fails:** Install NVIDIA driver ≥ 525 (see SETUP_GPU.md).

---

### 2. Docker GPU Access
```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

**Expected:** Same output as test #1, but inside container.

**If fails:**
- Install nvidia-container-toolkit
- Run: `sudo systemctl restart docker`

---

## Container Tests

### 3. Build Container with GPU Support
```bash
cd /path/to/multiscale_tda_geomorphology
docker-compose build
```

**Expected:** Builds successfully, shows packages installing (pytorch-cuda, cupy, dask-cuda).

**If fails:** Check environment.yml syntax.

---

### 4. Start Container with GPU
```bash
# With GPU support
docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up -d

# Verify container is running
docker ps | grep tda-geo
```

**Expected:** Container running with status "Up".

---

### 5. Test GPU Detection in Python
```bash
# Enter container
docker exec -it tda-geo-dev bash

# Run GPU detection
python -m geo_tda.utils.gpu_detection
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

CuPy is available for GPU-accelerated array operations

Recommended GPU memory limit: 19.2 GB (80% of 24.0 GB total)
```

**If "GPU: Not available":** Check docker-compose.gpu.yml is being used.

---

### 6. Test PyTorch CUDA
```bash
docker exec -it tda-geo-dev python << EOF
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Device count: {torch.cuda.device_count()}")
    print(f"Device name: {torch.cuda.get_device_name(0)}")
EOF
```

**Expected:**
```
PyTorch version: 2.4.x
CUDA available: True
CUDA version: 12.1
Device count: 1
Device name: NVIDIA GeForce RTX 4090
```

---

### 7. Test CuPy Array Operations
```bash
docker exec -it tda-geo-dev python << EOF
import cupy as cp
import numpy as np

# Create array on GPU
x = cp.array([1, 2, 3, 4, 5])
print(f"Array on GPU: {x}")
print(f"Sum: {cp.sum(x)}")

# Matrix multiplication benchmark
size = 5000
a_gpu = cp.random.rand(size, size, dtype=cp.float32)
b_gpu = cp.random.rand(size, size, dtype=cp.float32)

import time
start = time.time()
c_gpu = cp.dot(a_gpu, b_gpu)
cp.cuda.Stream.null.synchronize()  # Wait for GPU to finish
gpu_time = time.time() - start

print(f"\nGPU matrix multiply ({size}x{size}): {gpu_time:.3f}s")
print("✓ CuPy working correctly")
EOF
```

**Expected:** GPU computation completes in <1 second for 5000x5000 matrix.

---

### 8. Test Integration with Project Code
```bash
docker exec -it tda-geo-dev python << EOF
from geo_tda.utils import print_compute_summary
print_compute_summary()
EOF
```

**Expected:** Same output as Test #5.

---

### 9. Test Jupyter Lab Access
```bash
# Container should be running from Test #4
# Open browser to: http://localhost:8888

# In a Jupyter notebook cell:
from geo_tda.utils import detect_gpu_config
gpu = detect_gpu_config()
if gpu:
    print(f"✓ GPU detected: {gpu['device_name']}")
else:
    print("✗ No GPU detected")
```

**Expected:** GPU detected message.

---

### 10. Test Dask Dashboard
```bash
# In container Python or Jupyter:
from dask.distributed import Client, LocalCluster
cluster = LocalCluster(n_workers=4, threads_per_worker=1)
client = Client(cluster)
print(f"Dask dashboard: {client.dashboard_link}")
```

**Expected:** Dashboard accessible at http://localhost:8787

---

## Troubleshooting Quick Reference

| Test Fails | Likely Cause | Fix |
|------------|--------------|-----|
| Test #1 | Driver not installed | Install NVIDIA driver |
| Test #2 | nvidia-container-toolkit missing | Install toolkit, restart Docker |
| Test #3 | Environment.yml syntax error | Check YAML formatting |
| Test #4 | GPU config not loaded | Use `-f docker-compose.gpu.yml` |
| Test #5 | PyTorch/CUDA mismatch | Rebuild container |
| Test #6 | CUDA not found | Check environment.yml has pytorch-cuda=12.1 |
| Test #7 | CuPy not installed | Check environment.yml has cupy |
| Test #8 | Import error | Check __init__.py includes gpu_detection |
| Test #9 | Jupyter not starting | Check port 8888 not in use |
| Test #10 | Dashboard port conflict | Change DASK_DASHBOARD_PORT in .env |

---

## Success Criteria

✅ **All tests pass** → GPU is fully configured and ready for use!

✅ **Tests 1-8 pass, 9-10 fail** → GPU works, Jupyter/Dask issue (non-critical).

⚠️ **Tests 1-4 pass, 5-8 fail** → Container issue, rebuild with `docker-compose build --no-cache`.

❌ **Test 1 fails** → No GPU driver on host (install driver first).

❌ **Test 2 fails** → Docker can't access GPU (install nvidia-container-toolkit).

---

## After Successful Testing

1. **Update README.md** to document GPU is enabled
2. **Run pilot workflow** on small dataset to verify GPU acceleration
3. **Monitor performance** using Dask dashboard during processing
4. **Compare runtimes** (GPU vs CPU) to quantify speedup

---

*For detailed troubleshooting, see [SETUP_GPU.md](SETUP_GPU.md)*
