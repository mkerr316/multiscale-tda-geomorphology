# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Your Machine (Host)                       │
│                                                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │  VS Code   │  │  PyCharm   │  │  Browser   │  │  Terminal │ │
│  │            │  │            │  │            │  │           │ │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬─────┘ │
│        │               │               │               │        │
│        └───────────────┴───────────────┴───────────────┘        │
│                            │                                     │
│                            ↓                                     │
│        ┌───────────────────────────────────────────┐            │
│        │      Docker Port Mapping                  │            │
│        │  localhost:8888  → container:8888         │            │
│        │  localhost:8787  → container:8787         │            │
│        └───────────────────┬───────────────────────┘            │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Container                              │
│                   (tda-geo-dev)                                  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  entrypoint.sh (Auto-starts on container boot)          │   │
│  │  • Seeds conda environment (first run)                  │   │
│  │  • Sets up paths and permissions                        │   │
│  │  • Launches Jupyter Lab on 0.0.0.0:8888                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Jupyter Lab Server                                      │   │
│  │  • Running on port 8888                                  │   │
│  │  • Kernels using /opt/conda/envs/app/bin/python        │   │
│  │  • Root dir: /workspace                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Python Environment                                       │   │
│  │  /opt/conda/envs/app/                                    │   │
│  │  • Python 3.11                                           │   │
│  │  • NumPy, Pandas, GeoPandas                             │   │
│  │  • PyTorch, GDAL, Jupyter                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  /workspace (Mounted from host)                          │   │
│  │  ├── src/           ← Your Python code                   │   │
│  │  ├── notebooks/     ← Your Jupyter notebooks             │   │
│  │  ├── data/          ← Your data files                    │   │
│  │  └── outputs/       ← Generated outputs                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Persistent Volumes (survive container restarts)         │   │
│  │  • conda_store      ← Conda packages cached here        │   │
│  │  • pip_cache        ← Pip packages cached here          │   │
│  │  • jupyter_runtime  ← Jupyter settings                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## Startup Sequence

```
User runs: make up
    │
    ↓
Docker Compose starts container (if needed, builds image first)
    │
    ↓
entrypoint.sh executes
    │
    ├─→ Check if /opt/conda exists
    │   ├─ No → Seed from /opt/conda_image (first run, ~30 seconds)
    │   └─ Yes → Use existing environment (~instant)
    │
    ├─→ Set environment variables
    │   ├─ MAMBA_ROOT_PREFIX=/opt/conda
    │   ├─ JUPYTER_ENABLE_LAB=yes (from .env)
    │   └─ JUPYTER_TOKEN= (from .env)
    │
    ├─→ Fix permissions
    │   └─ chown mambauser:users /opt/conda /home/mambauser
    │
    └─→ Start Jupyter Lab
        └─ jupyter lab --config=/etc/jupyter/jupyter_server_config.py
              │
              ├─→ Binds to 0.0.0.0:8888 (inside container)
              ├─→ Root directory: /workspace
              ├─→ Token: empty (no auth for local dev)
              └─→ Ready! ✓
                    │
                    ↓
                  User connects:
                  • Browser: http://localhost:8888
                  • VS Code: Auto-detects kernel
                  • PyCharm: Connects to http://localhost:8888
```

## IDE Integration Paths

### VS Code Dev Container
```
VS Code
  │
  ├─→ Reads .devcontainer/devcontainer.json
  │   ├─ Uses docker-compose.yml
  │   ├─ Service: dev
  │   └─ Installs extensions automatically
  │
  ├─→ Connects to container over Docker API
  │   ├─ Python interpreter: /opt/conda/envs/app/bin/python
  │   └─ Terminal: bash in container
  │
  └─→ Jupyter integration
      └─ Detects kernels automatically from Python environment
```

### PyCharm/DataSpell
```
PyCharm
  │
  ├─→ Docker Compose interpreter configuration
  │   ├─ Service: dev
  │   ├─ Python path: /opt/conda/envs/app/bin/python
  │   └─ Syncs files via Docker volumes
  │
  ├─→ Runs code in container
  │   └─ Executes: docker exec tda-geo-dev python script.py
  │
  └─→ Jupyter integration
      └─ Connects to http://localhost:8888 (Jupyter server in container)
```

## File Synchronization

```
┌────────────────────────────────┐
│ Host (Your Computer)           │
│                                │
│ d:\OneDrive...\project\        │
│ ├── src/                       │
│ ├── notebooks/                 │
│ ├── data/                      │
│ └── ...                        │
└────────────┬───────────────────┘
             │
             │ Docker bind mount (real-time sync)
             │
             ↓
┌────────────────────────────────┐
│ Container                      │
│                                │
│ /workspace/                    │
│ ├── src/        ← Same files!  │
│ ├── notebooks/  ← Same files!  │
│ ├── data/       ← Same files!  │
│ └── ...                        │
└────────────────────────────────┘
```

**Key Point**: Files are NOT copied - they're the same files! Changes in VS Code/PyCharm instantly appear in the container and vice versa.

## Network Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Your Machine                         │
│                                                           │
│  Browser/IDE → localhost:8888                           │
│                     │                                     │
│                     ↓                                     │
│  Docker networking maps to container:8888               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│               Docker Container                          │
│                                                           │
│  Jupyter Lab listening on 0.0.0.0:8888                 │
│  (0.0.0.0 = all interfaces inside container)            │
│                                                           │
│  Security:                                               │
│  • Port only exposed to localhost (127.0.0.1)          │
│  • Not accessible from network                          │
│  • Token optional (empty by default)                    │
└─────────────────────────────────────────────────────────┘
```

## Why This Works Everywhere

### ✅ **Windows**
- Docker Desktop provides Linux VM
- Bind mounts work via VM
- Line endings normalized in Dockerfile

### ✅ **macOS**
- Docker Desktop provides Linux VM
- `platform: linux/amd64` ensures consistency on ARM Macs
- Bind mounts work via VM

### ✅ **Linux**
- Docker runs natively (no VM)
- Bind mounts are direct
- Better performance than Windows/Mac

### ✅ **Any IDE**
All IDEs just need to:
1. Connect to Docker container
2. Use Python at `/opt/conda/envs/app/bin/python`
3. (Optional) Connect Jupyter to `http://localhost:8888`

The container provides a **consistent environment** regardless of:
- Host OS
- IDE choice
- Local Python installation
- User preferences

## Security Layers

```
Internet ─X→ Blocked (ports bound to 127.0.0.1)
             │
Local Network ─X→ Blocked (ports bound to 127.0.0.1)
             │
Your Machine ─✓→ Allowed
             │
             ↓
         localhost:8888
             │
             ↓
         Container:8888
             │
             ├─ Token check (if JUPYTER_TOKEN set in .env)
             │
             └─ Jupyter Lab ✓
```

**For local dev**: Safe to use empty token (default)
**For remote access**: Set `JUPYTER_TOKEN` in `.env`

## Data Persistence

```
Container Restart (docker compose restart)
    │
    ├─→ Conda environment ✓ Persists (conda_store volume)
    ├─→ Pip cache ✓ Persists (pip_cache volume)
    ├─→ Jupyter settings ✓ Persists (jupyter_runtime volume)
    └─→ Your code/data ✓ Persists (bind mount to host)

Container Rebuild (make rebuild)
    │
    ├─→ Conda environment ✓ Persists (volume reused)
    ├─→ Pip cache ✓ Persists (volume reused)
    ├─→ Jupyter settings ✓ Persists (volume reused)
    └─→ Your code/data ✓ Persists (bind mount to host)

Volume Reset (make seed-reset)
    │
    ├─→ Conda environment ✗ Deleted (reseeded from image)
    ├─→ Pip cache ✓ Persists
    ├─→ Jupyter settings ✓ Persists
    └─→ Your code/data ✓ Persists (never deleted)
```

**Bottom line**: Your code and data are always safe. Only conda environment can be reset if needed.

---

## Summary

**Your project now has**:
- ✅ Automatic Jupyter Lab startup
- ✅ Cross-platform compatibility (Windows/Mac/Linux)
- ✅ Multi-IDE support (VS Code/PyCharm/Browser)
- ✅ Persistent environments (fast restarts)
- ✅ Secure by default (localhost-only)
- ✅ Production-ready configuration
- ✅ Fully documented setup

**To use**: Just run `make up` and everything starts automatically!
