#!/usr/bin/env bash
set -Eeuo pipefail
log() { echo "[$(date +'%F %T')] $*"; }

# Seed conda store (unchanged)
if [[ ! -d /opt/conda && -d /opt/conda_image ]]; then
  log "[entrypoint] /opt/conda not found; seeding from /opt/conda_image..."
  mkdir -p /opt/conda
  tar -C /opt/conda_image -c . | tar -C /opt/conda -x
else
  log "[entrypoint] /opt/conda already initialized."
fi

export MAMBA_ROOT_PREFIX=/opt/conda
export PATH="/opt/conda/envs/app/bin:/opt/conda/bin:/opt/conda/condabin:${PATH}"

# Ensure mambauser owns conda directory
if id -u mambauser >/dev/null 2>&1; then
  chown -R mambauser:users /opt/conda 2>/dev/null || true
  # Also ensure mambauser owns their home directory for IDE compatibility
  chown -R mambauser:users /home/mambauser 2>/dev/null || true
fi

run_as_mamba() {
  if [[ "${RUN_AS_ROOT:-0}" = "1" ]] || [[ "$(id -u)" -ne 0 ]] || ! id -u mambauser &>/dev/null; then
    exec "$@"
  else
    # Pass through more environment variables for IDE compatibility
    exec runuser -u mambauser -- env -i \
      HOME="/home/mambauser" \
      USER="mambauser" \
      SHELL="/bin/bash" \
      MAMBA_ROOT_PREFIX="/opt/conda" \
      PATH="/opt/conda/envs/app/bin:/opt/conda/bin:/opt/conda/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
      PYTHONUNBUFFERED="${PYTHONUNBUFFERED:-1}" \
      PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}" \
      JUPYTER_ENABLE_LAB="${JUPYTER_ENABLE_LAB:-yes}" \
      JUPYTER_TOKEN="${JUPYTER_TOKEN:-}" \
      "$@"
  fi
}

# If no args -> start Jupyter Server inside the container
if [[ "$#" -eq 0 ]]; then
  log "[entrypoint] Starting Jupyter Server (JupyterLab=${JUPYTER_ENABLE_LAB:-yes})..."

  # Determine which Jupyter interface to use
  if [[ "${JUPYTER_ENABLE_LAB:-yes}" == "yes" ]]; then
    CMD=(jupyter lab --config=/etc/jupyter/jupyter_server_config.py)
  else
    CMD=(jupyter notebook --config=/etc/jupyter/jupyter_server_config.py)
  fi

  run_as_mamba "${CMD[@]}"
else
  # For IDE compatibility: if first arg is a shell, run it interactively
  case "$1" in
    bash|sh|zsh|/bin/bash|/bin/sh|/bin/zsh)
      log "[entrypoint] Starting interactive shell: $1"
      ;;
    *)
      log "[entrypoint] Executing command: $*"
      ;;
  esac
  run_as_mamba "$@"
fi
