# Setup Guide: Getting Started with Docker

This guide walks you through setting up this project from scratch on Windows, macOS, or Linux.

## Table of Contents

- [Windows Setup](#windows-setup)
- [macOS Setup](#macos-setup)
- [Linux Setup](#linux-setup)
- [First Run](#first-run)
- [IDE Setup](#ide-setup)
- [Troubleshooting](#troubleshooting)

---

## Windows Setup

### Step 1: Install Docker Desktop

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Run the installer
3. **Important**: Enable WSL 2 backend when prompted
4. Restart your computer when installation completes
5. Launch Docker Desktop and wait for it to start (green icon in system tray)

**System Requirements**:
- Windows 10/11 Pro, Enterprise, or Education (Build 19041+)
- WSL 2 enabled
- Virtualization enabled in BIOS

### Step 2: Verify Installation

Open PowerShell or Command Prompt and run:

```powershell
docker --version
docker compose version
```

You should see version numbers (e.g., `Docker version 24.x.x`).

### Step 3: Configure Docker (Optional but Recommended)

In Docker Desktop:
1. Go to Settings → Resources
2. Increase **Memory** to at least 8GB (16GB recommended for large datasets)
3. Increase **CPUs** to at least 4 cores
4. Click "Apply & Restart"

### Step 4: Clone This Repository

```powershell
# Using Git Bash or PowerShell
cd "D:\OneDrive - University of Georgia"
git clone <your-repo-url>
cd multiscale_tda_geomorphology
```

### Step 5: Start the Environment

```powershell
# Using make (if available)
make up

# OR using Docker Compose directly
docker compose up -d dev
```

**First run will take 5-10 minutes** to download images and build the environment.

---

## macOS Setup

### Step 1: Install Docker Desktop

1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
   - Choose **Apple Silicon** for M1/M2/M3 Macs
   - Choose **Intel** for older Macs
2. Drag Docker.app to Applications folder
3. Launch Docker Desktop from Applications
4. Follow the setup wizard
5. Wait for Docker to start (whale icon in menu bar)

### Step 2: Verify Installation

Open Terminal and run:

```bash
docker --version
docker compose version
```

### Step 3: Configure Docker

In Docker Desktop:
1. Go to Preferences → Resources
2. Increase **Memory** to at least 8GB
3. Increase **CPUs** to at least 4 cores
4. Click "Apply & Restart"

### Step 4: Clone and Start

```bash
cd ~/Documents  # or wherever you keep projects
git clone <your-repo-url>
cd multiscale_tda_geomorphology
make up
```

---

## Linux Setup

### Step 1: Install Docker Engine

**Ubuntu/Debian**:
```bash
# Update package index
sudo apt-get update

# Install dependencies
sudo apt-get install ca-certificates curl gnupg lsb-release

# Add Docker's GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

**Fedora/RHEL**:
```bash
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### Step 2: Post-Installation Setup

```bash
# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (avoid using sudo)
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
# Or run: newgrp docker
```

### Step 3: Verify Installation

```bash
docker --version
docker compose version
```

### Step 4: Clone and Start

```bash
cd ~/projects  # or wherever you keep code
git clone <your-repo-url>
cd multiscale_tda_geomorphology
make up
```

---

## First Run

After running `make up` for the first time:

1. **Wait for build** (5-10 minutes):
   - Docker downloads base image (~500MB)
   - Creates conda environment with all packages
   - Seeds persistent volume

2. **Verify container is running**:
   ```bash
   make status
   # Should show "tda-geo-dev" as "Up"
   ```

3. **Check logs**:
   ```bash
   make logs
   # Should see: "[entrypoint] Starting Jupyter Server..."
   ```

4. **Access Jupyter Lab**:
   - Open browser to http://localhost:8888
   - No token required (local dev setup)
   - You should see the JupyterLab interface with `/workspace` directory

5. **Test Python**:
   ```bash
   make python
   # Should see Python 3.11.x REPL
   >>> import numpy, pandas, geopandas
   >>> print("Success!")
   ```

---

## IDE Setup

### VS Code (Easiest)

**Prerequisites**:
- Install [VS Code](https://code.visualstudio.com/)
- Install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

**Steps**:
1. Open project folder in VS Code
2. You'll see a notification: "Reopen in Container"
3. Click "Reopen in Container"
4. Wait 1-2 minutes for container to start and extensions to install
5. Done! Python interpreter and Jupyter are automatically configured

**Manual Method**:
1. Press `F1` or `Ctrl+Shift+P`
2. Type "Dev Containers: Reopen in Container"
3. Select it and wait

### PyCharm Professional / DataSpell

**Prerequisites**:
- PyCharm Professional or DataSpell (Community edition doesn't support Docker interpreters)

**Steps**:
1. Open project folder
2. Go to: File → Settings → Project → Python Interpreter
3. Click gear icon (⚙️) → Add Interpreter → On Docker Compose
4. Configuration:
   - **Server**: Docker (select from dropdown)
   - **Configuration files**: `./docker-compose.yml`
   - **Service**: `dev`
   - **Python interpreter path**: `/opt/conda/envs/app/bin/python`
5. Click "OK" and wait for indexing

**Jupyter Setup in PyCharm**:
1. Open any `.ipynb` file
2. Click "Configure Jupyter Server" in top-right
3. Select "Configured Server"
4. URL: `http://localhost:8888`
5. Token: leave empty
6. Click "OK"

### JupyterLab (Browser)

**Steps**:
1. Ensure container is running: `make up`
2. Open browser to http://localhost:8888
3. Start working in notebooks

**To get URL with token**:
```bash
make jupyter-url
```

---

## Troubleshooting

### "Docker daemon not running"

**Windows/Mac**:
- Open Docker Desktop
- Wait for it to fully start (icon in system tray/menu bar)

**Linux**:
```bash
sudo systemctl start docker
```

### "Port 8888 already in use"

Another application is using port 8888.

**Solution 1: Find and stop the other application**
```bash
# Windows
netstat -ano | findstr :8888

# Mac/Linux
lsof -i :8888
```

**Solution 2: Change Jupyter port**
1. Edit `.env`:
   ```bash
   JUPYTER_PORT=8889
   ```
2. Restart container: `make restart`
3. Access Jupyter at http://localhost:8889

### "Cannot connect to Docker daemon"

**Windows/Mac**: Docker Desktop not running - launch it

**Linux**:
```bash
# Check if Docker is running
sudo systemctl status docker

# If not, start it
sudo systemctl start docker

# If permission denied
sudo usermod -aG docker $USER
# Then log out and back in
```

### Container builds but immediately exits

Check logs:
```bash
make logs
```

Common causes:
- Syntax error in `entrypoint.sh` (should have Unix line endings)
- Missing dependencies in `environment.yml`
- Out of disk space

### "No space left on device"

Docker images and volumes take up space.

**Check Docker disk usage**:
```bash
docker system df
```

**Clean up**:
```bash
# Remove stopped containers and unused images
make prune

# Remove project volumes (safe - rebuilds on next start)
make clean-volumes

# Nuclear option (removes ALL Docker data)
docker system prune -a --volumes
```

### Python packages not found

The conda environment might not be activated.

**Verify**:
```bash
make shell
which python
# Should show: /opt/conda/envs/app/bin/python
```

If not, rebuild:
```bash
make rebuild
```

### Jupyter kernel dies immediately

**Cause**: Out of memory or shared memory too small

**Solution**: Increase Docker memory allocation
- Docker Desktop → Settings → Resources → Memory
- Increase to at least 8GB
- Restart Docker Desktop

### VS Code can't connect to container

1. Ensure container is running: `make status`
2. Restart VS Code
3. Try: F1 → "Dev Containers: Rebuild Container"
4. Check Docker Desktop is running

### PyCharm indexing stuck

1. File → Invalidate Caches and Restart
2. If still stuck: delete `.idea/` folder and reopen project
3. Reconfigure Python interpreter

---

## Next Steps

Once everything is working:

1. **Explore the notebooks**: `notebooks/Section 1/`
2. **Read the main README**: [README.md](README.md)
3. **Run `make help`**: See all available commands
4. **Check environment**: `make env-info`

---

## Getting Help

If you're still stuck:

1. Check container logs: `make logs`
2. Check container health: `make health`
3. Try a fresh rebuild: `make deep-clean && make rebuild`
4. Check Docker Desktop dashboard for errors
5. Search [Docker documentation](https://docs.docker.com/)
6. Ask for help with the error message from `make logs`

---

**Remember**: First run takes 5-10 minutes. Subsequent starts take ~10 seconds!
