# Multiscale TDA Geomorphology Research Environment

[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)](https://www.docker.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626?logo=jupyter)](https://jupyter.org/)

A fully containerized, IDE-agnostic research environment for geospatial topological data analysis.

## Features

- **Fully Containerized**: Works on any machine with Docker - no local Python setup needed
- **IDE Agnostic**: Seamless integration with VS Code, PyCharm, DataSpell, and more
- **Fast Builds**: Conda environment cached in volumes; BuildKit layer caching
- **Portable**: Auto-seeded volumes work immediately on new machines
- **Modern Stack**: Python 3.11, NumPy 2.x, PyTorch, GDAL, GeoPandas, and geospatial tools
- **Jupyter Integration**: Built-in JupyterLab server accessible from any browser or IDE
- **GPU Support**: CUDA-enabled PyTorch for accelerated computing

## Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) or Docker Engine (Linux)
- [Docker Compose](https://docs.docker.com/compose/install/) v2.0+
- (Optional) [VS Code](https://code.visualstudio.com/) with [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### 1. Clone and Start

```bash
# Clone the repository
git clone <your-repo-url>
cd multiscale_tda_geomorphology

# Start the environment
make up
```

That's it! The container will:
1. Build the Docker image (first time only, ~5-10 minutes)
2. Seed the conda environment into a persistent volume
3. Start Jupyter Lab on http://localhost:8888

### 2. Access Your Environment

**Option A: Jupyter Lab (Browser)**
```bash
# Open http://localhost:8888 in your browser
make jupyter-url  # Get the URL with token
```

**Option B: VS Code Dev Container**
1. Open this folder in VS Code
2. Click "Reopen in Container" when prompted
3. VS Code will automatically connect to the running container

**Option C: PyCharm / DataSpell**
1. Go to Settings → Project → Python Interpreter
2. Add Interpreter → On Docker Compose
3. Select service: `dev`
4. Python interpreter path: `/opt/conda/envs/app/bin/python`

**Option D: Terminal / Shell**
```bash
make shell        # Open bash in container
make python       # Start Python REPL
make ipython      # Start IPython REPL
```

## Common Commands

Run `make` or `make help` to see all available commands:

```bash
# Development
make up           # Start containers
make down         # Stop containers
make restart      # Restart containers
make status       # Show container status

# Building
make build        # Build Docker image
make rebuild      # Rebuild from scratch (no cache)

# Shell Access
make shell        # Bash shell in container
make python       # Python REPL
make ipython      # IPython REPL

# Jupyter
make jupyter-url  # Show Jupyter URL
make jupyter-logs # Follow Jupyter logs

# Logs & Debugging
make logs         # Follow container logs
make health       # Check container health

# Maintenance
make seed-reset   # Reset conda environment
make clean-volumes # Remove Docker volumes
make prune        # Clean Docker system

# Code Quality (if configured)
make lint         # Run linter
make format       # Format code
make test         # Run tests
```

## Project Structure

```
multiscale_tda_geomorphology/
├── .devcontainer/          # VS Code Dev Container config
├── .vscode/                # VS Code workspace settings
├── config/                 # Configuration files
│   └── jupyter_server_config.py
├── data/                   # Data directory (gitignored)
│   ├── raw/                # Raw input data
│   └── processed/          # Processed outputs
├── notebooks/              # Jupyter notebooks
│   └── Section 1/          # Organized by section
├── outputs/                # Analysis outputs (gitignored)
├── src/                    # Python source code
│   └── geo_tda/            # Main package
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── entrypoint.sh           # Container entrypoint script
├── environment.yml         # Conda environment specification
├── Makefile                # Development commands
├── .env                    # Environment variables
└── README.md               # This file
```

## IDE Setup Details

### VS Code (Recommended for Beginners)

1. Install [VS Code](https://code.visualstudio.com/) and [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open this folder in VS Code
3. Click "Reopen in Container" (or press F1 → "Dev Containers: Reopen in Container")
4. VS Code will automatically:
   - Start the Docker container
   - Install recommended extensions
   - Configure Python interpreter
   - Set up Jupyter integration

**Pros**: Zero configuration, works out of the box
**Cons**: None for most users

### PyCharm Professional / DataSpell

1. Open this folder in PyCharm/DataSpell
2. Go to Settings → Project → Python Interpreter
3. Click ⚙️ → Add Interpreter → On Docker Compose
4. Configuration:
   - Server: Docker
   - Configuration files: `./docker-compose.yml`
   - Service: `dev`
   - Python interpreter path: `/opt/conda/envs/app/bin/python`
5. Apply and wait for indexing to complete

**Jupyter Configuration**:
- In a `.ipynb` file, select kernel from the bottom-right
- Choose "Existing Jupyter Server"
- Enter: `http://localhost:8888`
- No token required (for local dev)

**Pros**: Powerful IDE features, excellent debugging
**Cons**: Requires Professional edition for Docker support

### PyCharm Community Edition

PyCharm CE doesn't support Docker interpreters directly. Workarounds:

1. **Use Jupyter from Browser**: Run notebooks in browser, develop Python files locally
2. **Use `make shell`**: Run scripts via `make shell`, then `python script.py`
3. **Upgrade to Professional**: Best long-term solution

## Configuration

### Environment Variables (`.env`)

```bash
# Project name
COMPOSE_PROJECT_NAME=tda-geo

# Jupyter settings
JUPYTER_TOKEN=              # Empty = no auth (local dev)
JUPYTER_ENABLE_LAB=yes      # Use JupyterLab (vs classic notebook)

# Port mappings (change if conflicts)
JUPYTER_PORT=8888
DASK_DASHBOARD_PORT=8787
TENSORBOARD_PORT=6006
```

### Python Packages (`environment.yml`)

To add new packages:

1. Edit [environment.yml](environment.yml)
2. Rebuild the image: `make rebuild`
3. Or update running container: `make update-deps`

**Important**: Always use `environment.yml` for package management. Don't use `pip install` directly in the container (changes won't persist).

## Updating the Environment

When you modify `environment.yml`:

```bash
# Option 1: Rebuild everything (safest)
make rebuild

# Option 2: Update existing environment (faster, but may have conflicts)
make update-deps
```

## Troubleshooting

### Container won't start

```bash
# Check logs
make logs

# Check container status
make status

# Nuclear option: rebuild from scratch
make deep-clean
make rebuild
```

### Jupyter Lab not accessible

```bash
# Get the URL with token
make jupyter-url

# Check if port 8888 is already in use
# On Windows: netstat -ano | findstr :8888
# On Mac/Linux: lsof -i :8888

# Change port in .env if needed:
# JUPYTER_PORT=8889
```

### PyCharm can't find interpreter

1. Ensure container is running: `make status`
2. Verify Python path in container: `make shell`, then `which python`
3. Use exact path: `/opt/conda/envs/app/bin/python`

### Permission errors (Linux)

Docker volumes may have permission issues on Linux:

```bash
# Option 1: Run as root in container (not recommended)
make shell-root

# Option 2: Match UID/GID (advanced - edit Dockerfile)
# Set ARG MAMBA_UID=<your-uid> and ARG MAMBA_GID=<your-gid>
```

### Out of disk space

```bash
# Remove unused Docker resources
make prune

# Remove project volumes (your code is safe)
make clean-volumes

# Nuclear option (removes everything)
make deep-clean
```

## Development Workflow

### Typical Workflow

1. **Start environment**: `make up`
2. **Open in IDE**: VS Code (dev container) or PyCharm (Docker Compose interpreter)
3. **Develop**: Edit code in `src/`, run notebooks in `notebooks/`
4. **Test**: `make test` (if tests configured)
5. **Stop**: `make down` (or leave running for next session)

### Running Notebooks

**In Browser**:
```bash
make up
# Open http://localhost:8888
```

**In VS Code**:
- Open `.ipynb` file
- Select kernel: "Python 3.11 (app)" from bottom-right

**In PyCharm/DataSpell**:
- Open `.ipynb` file
- Select "Managed Server" or configure Jupyter server (http://localhost:8888)

### Running Python Scripts

**From IDE**: Run normally - IDE will execute in container

**From terminal**:
```bash
# Option 1: Via make shell
make shell
python src/geo_tda/script.py

# Option 2: Direct execution
docker exec tda-geo-dev python src/geo_tda/script.py
```

## Why This Setup?

### The Problem

Research code often breaks when:
- Moving between machines (Windows ↔ Mac ↔ Linux)
- Python versions differ
- Conda environments drift
- IDEs have different Python integration methods

### The Solution

**Docker + Volume-Based Conda**:
- ✅ Same environment on all machines
- ✅ Fast startup (volumes persist conda packages)
- ✅ Works with any IDE
- ✅ No local Python installation needed
- ✅ Jupyter server built-in
- ✅ Reproducible builds

## Contributing

When adding new features:

1. Update `environment.yml` for new dependencies
2. Document changes in commit messages
3. Test in a fresh build: `make rebuild`

## License

[Your License Here]

## Contact

[Your Contact Info]

---

**Tip**: Run `make help` to see all available commands!
