# syntax=docker/dockerfile:1.7
FROM mambaorg/micromamba:1.5.10-jammy AS build
SHELL ["/bin/bash", "-lc"]
ENV MAMBA_NO_BANNER=1 MAMBA_ROOT_PREFIX=/opt/conda

# don't force strict priority; rely on explicit channel selectors
# RUN micromamba config set channel_priority strict

COPY environment.yml /tmp/environment.src
RUN set -e; \
    sed '1s/^\xEF\xBB\xBF//' /tmp/environment.src | tr -d '\r' | expand -t 2 > /tmp/environment.yml; \
    head -n 5 /tmp/environment.yml || true

RUN --mount=type=cache,target=/opt/conda/pkgs \
    micromamba create -y -n app -f /tmp/environment.yml && \
    micromamba clean --all -y

RUN micromamba run -n app python - <<'PY'
mods = ["numpy","pandas","geopandas","pyproj","shapely","pyogrio","sklearn","matplotlib","dask","distributed"]
for m in mods: __import__(m)
print("Imports OK")
try:
    import torch
    print("Torch:", torch.__version__, "CUDA available:", torch.cuda.is_available())
except Exception as e:
    print("Torch check:", e)
PY
