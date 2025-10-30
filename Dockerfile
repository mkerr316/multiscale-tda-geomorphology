# syntax=docker/dockerfile:1.7
FROM mambaorg/micromamba:1.5.10-jammy

# Use BuildKit features for better caching and parallel builds
SHELL ["/bin/bash", "-lc"]

# --- Build Arguments ---
ARG MAMBA_USER=mambauser
ARG MAMBA_UID=1000
ARG MAMBA_GID=1000

# --- Core environment variables ---
ENV MAMBA_NO_BANNER=1 \
    MAMBA_ROOT_PREFIX=/opt/conda \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# --- Install system dependencies (for IDE debugging, git, etc.) ---
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Version control
    git \
    git-lfs \
    # Build tools (sometimes needed for pip packages)
    build-essential \
    gcc \
    g++ \
    # Network tools
    curl \
    wget \
    ca-certificates \
    # Debugging tools
    gdb \
    strace \
    # Text editors (useful for container debugging)
    vim \
    nano \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Create conda environment with caching ---
COPY environment.yml /tmp/environment.src

# Clean and normalize environment.yml (handle BOM, line endings, tabs)
RUN --mount=type=cache,target=/opt/conda/pkgs \
    set -e; \
    sed '1s/^\xEF\xBB\BF//' /tmp/environment.src | tr -d '\r' | expand -t 2 > /tmp/environment.yml; \
    micromamba create -y -n app -f /tmp/environment.yml && \
    micromamba clean --all -y

# --- Smoke test: verify Python and key packages ---
RUN micromamba run -n app python -c "\
import sys, numpy, pandas, geopandas; \
print(f'Python: {sys.version.split()[0]}'); \
print(f'NumPy: {numpy.__version__}'); \
print(f'Pandas: {pandas.__version__}'); \
print(f'GeoPandas: {geopandas.__version__}'); \
"

# --- Setup workspace and user directories ---
USER root
RUN mkdir -p /workspace && \
    chown -R ${MAMBA_USER}:${MAMBA_USER} /workspace && \
    # Ensure home directory exists with correct permissions
    mkdir -p /home/${MAMBA_USER}/.local/share/jupyter && \
    mkdir -p /home/${MAMBA_USER}/.cache/pip && \
    chown -R ${MAMBA_USER}:${MAMBA_USER} /home/${MAMBA_USER}

# Create stable Python symlinks for IDE interpreter detection
USER ${MAMBA_USER}
RUN mkdir -p /workspace/bin && \
    ln -s /opt/conda/envs/app/bin/python /workspace/bin/python && \
    ln -s /opt/conda/envs/app/bin/python3 /workspace/bin/python3 && \
    ln -s /opt/conda/envs/app/bin/pip /workspace/bin/pip && \
    ln -s /opt/conda/envs/app/bin/jupyter /workspace/bin/jupyter

# Create conda symlink to micromamba for Jupyter %conda magic compatibility
USER root
RUN ln -s /usr/bin/micromamba /opt/conda/envs/app/bin/conda

# --- Seedable conda copy (for volume persistence) ---
USER root
RUN cp -a /opt/conda /opt/conda_image && \
    chown -R ${MAMBA_USER}:${MAMBA_USER} /opt/conda_image

# --- Copy Jupyter configuration ---
COPY config/jupyter_server_config.py /etc/jupyter/
RUN chmod 644 /etc/jupyter/jupyter_server_config.py

# --- Copy and configure entrypoint ---
COPY --chown=${MAMBA_USER}:${MAMBA_USER} --chmod=0755 entrypoint.sh /usr/local/bin/entrypoint.sh
# Normalize line endings (Windows -> Unix)
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh

# --- Set working directory ---
WORKDIR /workspace

# --- Configure user and entrypoint ---
USER root
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD []

# --- Labels for metadata ---
LABEL maintainer="Your Name <your.email@uga.edu>"
LABEL description="Containerized geospatial TDA research environment"
LABEL version="0.1.0"
