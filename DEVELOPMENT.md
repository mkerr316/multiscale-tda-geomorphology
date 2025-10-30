# Development Environment Setup

This project uses Docker to provide a consistent development environment across all platforms (Windows, macOS, Linux).

## Quick Start

```bash
# Start the environment
make up  # or: docker-compose up -d

# Stop the environment
make down  # or: docker-compose down
```

## Access Methods

### 1. Jupyter Lab (Recommended for Data Science)

**Best for:** Interactive notebooks, data exploration, visualization

```
http://localhost:8888
```

- Full scientific Python stack
- No additional setup required
- Works immediately after `make up`

### 2. VS Code with Terminal Execution (Recommended if Dev Containers Blocked)

**Best for:** Code editing, debugging, Git integration when network restricts Dev Containers

**Setup:**
1. Open this folder in VS Code (on Windows)
2. Open integrated terminal (`Ctrl+` `)
3. Connect to the running container:
   ```powershell
   docker exec -it tda-geo-dev bash
   ```
4. Execute Python code:
   ```bash
   # Run a script
   micromamba run -n app python scripts/your_script.py

   # Or start interactive Python
   micromamba run -n app ipython

   # Or start Jupyter from terminal
   micromamba run -n app jupyter lab --no-browser
   ```

**Benefits:**
- Edit files with VS Code's full IDE features
- Execute in container with all packages available
- No network dependencies or special setup required

### 3. VS Code Dev Containers (If Network Allows)

**Best for:** Fully integrated container development

**Prerequisites:**
- Install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Network access to `update.code.visualstudio.com`

**Setup:**
1. Open this folder in VS Code
2. Press `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

**Note:** If download fails due to network restrictions, use Option 2 (Terminal Execution) instead.

### 3. Direct Terminal Access

**Best for:** Running scripts, command-line tools, debugging

```bash
# Execute commands in the running container
docker exec -it tda-geo-dev bash

# Activate the conda environment (if needed)
micromamba run -n app python your_script.py
```

### 4. VS Code Remote - WSL (Windows Alternative)

**Best for:** Windows users with network restrictions

If you're on Windows and VS Code Dev Containers don't work:

1. Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)
2. Install Docker Desktop with WSL2 backend
3. In VS Code: `Ctrl+Shift+P` → "WSL: Connect to WSL"
4. Open project from WSL filesystem
5. Docker commands run in WSL, avoiding Windows network issues

## Environment Details

- **Python:** 3.11+ (via Micromamba)
- **Key Libraries:** GDAL, GeoPandas, GUDHI, Scikit-learn, Dask
- **Ports:**
  - `8888` - Jupyter Lab
  - `8787` - Dask Dashboard
  - `6006` - TensorBoard

## GPU Support

```bash
# Start with GPU support
make up-gpu
# or: docker-compose -f docker-compose.yml -f docker-compose.gpu.yml up -d
```

## Best Practices

1. **Use the container for all computation** - Don't install packages on your host
2. **Commit environment.yml changes** - Keep dependencies version-controlled
3. **Use Jupyter for exploration** - Use VS Code/scripts for production code
4. **Mount data as volumes** - Don't copy large datasets into the image

## Portability

This environment is designed to work on:
- ✅ Windows (WSL2 + Docker Desktop)
- ✅ macOS (Docker Desktop)
- ✅ Linux (Docker Engine)
- ✅ HPC clusters (Singularity/Apptainer conversion possible)

The container is self-contained - the only requirement is Docker.
