# Quick Start Guide

**5-Minute Setup for Experienced Users**

## Prerequisites

- Docker Desktop installed and running
- Git installed

## Setup

```bash
# 1. Clone and enter project
git clone <repo-url>
cd multiscale_tda_geomorphology

# 2. Start container
make up

# 3. Access Jupyter
# Open browser to: http://localhost:8888
```

## Daily Usage

```bash
# Start
make up

# Stop
make down

# Shell access
make shell

# View logs
make logs

# Rebuild (after changing environment.yml)
make rebuild
```

## IDE Setup

### VS Code
1. Install "Dev Containers" extension
2. Open folder → Click "Reopen in Container"
3. Done!

### PyCharm/DataSpell
1. Settings → Python Interpreter
2. Add → Docker Compose
3. Service: `dev`
4. Python path: `/opt/conda/envs/app/bin/python`

## Key Paths

- **Python interpreter**: `/opt/conda/envs/app/bin/python`
- **Jupyter URL**: `http://localhost:8888`
- **Dask Dashboard**: `http://localhost:8787`
- **Workspace**: `/workspace` (mounted to project root)

## Help

```bash
make help          # See all commands
make env-info      # Check Python/package versions
make jupyter-url   # Get Jupyter URL with token
```

## Troubleshooting

```bash
make logs          # Check logs
make status        # Container status
make rebuild       # Nuclear option: rebuild everything
```

**Full documentation**: See [README.md](README.md) and [SETUP_GUIDE.md](SETUP_GUIDE.md)
