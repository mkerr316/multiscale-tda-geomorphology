#!/usr/bin/env bash
set -Eeuo pipefail

log() { echo "[$(date +'%F %T')] $*"; }

# Seed /opt/conda from the baked-in image on first run (fast boot)
if [[ ! -d /opt/conda && -d /opt/conda_image ]]; then
  log "[entrypoint] /opt/conda not found; seeding from /opt/conda_image..."
  mkdir -p /opt/conda
  tar -C /opt/conda_image -c . | tar -C /opt/conda -x
else
  log "[entrypoint] /opt/conda already initialized."
fi

# Ensure conda paths are available for both root and mambauser
export MAMBA_ROOT_PREFIX=/opt/conda
export PATH="/opt/conda/envs/app/bin:/opt/conda/bin:/opt/conda/condabin:${PATH}"

# Optional: keep writes working for the unprivileged user (best-effort)
if id -u mambauser >/dev/null 2>&1; then
  chown -R mambauser:users /opt/conda 2>/dev/null || true
fi

# Allow opting out of privilege drop with RUN_AS_ROOT=1
if [[ "${RUN_AS_ROOT:-0}" = "1" ]] || [[ "$(id -u)" -ne 0 ]] || ! id -u mambauser &>/dev/null; then
  exec "$@"
else
  # Pass a clean but complete environment so 'jupyter' resolves for mambauser
  exec runuser -u mambauser -- env -i \
    HOME="/home/mambauser" \
    USER="mambauser" \
    SHELL="/bin/bash" \
    MAMBA_ROOT_PREFIX="/opt/conda" \
    PATH="/opt/conda/envs/app/bin:/opt/conda/bin:/opt/conda/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    "$@"
fi
