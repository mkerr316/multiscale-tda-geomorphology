# Testing Your Setup

Quick verification that everything works correctly.

## Test 1: Container Starts Automatically

```bash
# Start the container
make up

# You should see:
# ✓ Container started!
#   - Jupyter Lab: http://localhost:8888
#   - Dask Dashboard: http://localhost:8787
```

**Expected**: Container starts in 5-15 seconds (first time: 5-10 minutes to build)

## Test 2: Jupyter Auto-Starts

```bash
# Check logs for Jupyter startup
make logs

# You should see:
# [entrypoint] Starting Jupyter Server (JupyterLab=yes)...
# [ServerApp] Jupyter Server is running at:
# [ServerApp] http://0.0.0.0:8888/lab
```

**Expected**: Jupyter Lab starts automatically, no manual intervention needed

## Test 3: Jupyter Is Accessible

Open browser to: http://localhost:8888

**Expected**:
- ✅ JupyterLab interface loads
- ✅ No token prompt (local dev)
- ✅ You see `/workspace` directory
- ✅ Can open notebooks in `notebooks/` folder

## Test 4: Python Interpreter Works

```bash
make shell
python -c "import numpy, pandas, geopandas; print('✓ All imports work!')"
```

**Expected**: Prints `✓ All imports work!` with no errors

## Test 5: VS Code Integration (if using VS Code)

1. Open project folder in VS Code
2. Click "Reopen in Container" when prompted
3. Wait ~30 seconds for setup
4. Open any `.py` file

**Expected**:
- ✅ Python interpreter auto-detected: `/opt/conda/envs/app/bin/python`
- ✅ IntelliSense/autocomplete works
- ✅ Can run Python files
- ✅ Can open `.ipynb` files with kernel selection

## Test 6: PyCharm Integration (if using PyCharm)

1. Open project folder
2. Go to: Settings → Project → Python Interpreter
3. You should see: `Remote Python 3.11.x Docker Compose (dev at ./docker-compose.yml)`

**Expected**:
- ✅ Interpreter connected
- ✅ Can see installed packages
- ✅ Can run Python files
- ✅ Can open notebooks with kernel

## Test 7: Cross-Platform (if you have access to another machine)

1. Clone repo on different OS
2. Run `make up`
3. Everything should work identically

**Expected**: Same behavior on Windows/Mac/Linux

## Test 8: Configuration Changes Work

```bash
# Edit .env
echo "JUPYTER_PORT=8889" >> .env

# Restart
make restart

# Check new port
curl http://localhost:8889
```

**Expected**: Jupyter now on port 8889 instead of 8888

## Test 9: Environment Updates Work

```bash
# Add package to environment.yml (e.g., add "- seaborn" under dependencies)
# Then update
make update-deps

# OR rebuild from scratch
make rebuild

# Verify
make shell
python -c "import seaborn; print('✓ New package works!')"
```

**Expected**: New packages available after rebuild

## Test 10: Makefile Commands Work

```bash
make help           # Shows help
make status         # Shows container status
make env-info       # Shows Python/package versions
make jupyter-url    # Shows Jupyter URL
make logs-tail      # Shows last 50 log lines
```

**Expected**: All commands work without errors

---

## ✅ All Tests Pass?

Your setup is fully functional! You can now:
- Develop on any machine
- Switch between IDEs freely
- Share with collaborators (they just need Docker)
- Reproduce your environment anywhere

## ❌ Something Failed?

Check the troubleshooting section in:
- [README.md](README.md#troubleshooting)
- [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting)

Or run:
```bash
make logs       # See what went wrong
make status     # Check container state
make rebuild    # Nuclear option: rebuild everything
```
