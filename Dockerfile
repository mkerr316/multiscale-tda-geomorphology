# syntax=docker/dockerfile:1.7
FROM mambaorg/micromamba:1.5.10-jammy
SHELL ["/bin/bash", "-lc"]

# --- Core env/tuning ---
ENV MAMBA_NO_BANNER=1 MAMBA_ROOT_PREFIX=/opt/conda PIP_NO_CACHE_DIR=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# --- Create env with micromamba (cached package store) ---
COPY environment.yml /tmp/environment.src
RUN --mount=type=cache,target=/opt/conda/pkgs \
    set -e; \
    sed '1s/^\xEF\xBB\BF//' /tmp/environment.src | tr -d '\r' | expand -t 2 > /tmp/environment.yml; \
    micromamba create -y -n app -f /tmp/environment.yml && \
    micromamba clean --all -y

# --- Quick smoke test ---
RUN micromamba run -n app python -c "import sys, numpy; print(f'Python: {sys.version.split()[0]}'); print(f'NumPy: {numpy.__version__}')"

# --- Create workspace and user setup ---
USER root
RUN mkdir -p /workspace && chown -R ${MAMBA_USER}:${MAMBA_USER} /workspace
USER ${MAMBA_USER}
RUN mkdir -p /workspace/bin && \
    ln -s /opt/conda/envs/app/bin/python /workspace/bin/python && \
    ln -s /opt/conda/envs/app/bin/python3 /workspace/bin/python3

# --- Seedable Conda copy (requires root) ---
USER root
RUN cp -a /opt/conda /opt/conda_image && chown -R ${MAMBA_USER}:${MAMBA_USER} /opt/conda_image

# --- Entrypoint and Jupyter Config ---
# ADDED: Copy the server config file to a standard location Jupyter will read
COPY config/jupyter_server_config.py /etc/jupyter/

COPY --chown=${MAMBA_USER}:${MAMBA_USER} --chmod=0755 entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh

USER root
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# The start_jupyter.sh is no longer needed