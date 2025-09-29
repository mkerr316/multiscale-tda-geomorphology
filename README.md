# TDA Geo Dev — Portable, Fast, and PyCharm-Friendly

## Why this layout?

* **Fast**: Conda env cached in a named volume.
* **Portable**: Volume is **auto-seeded** on first run from the baked image; new machines work immediately.
* **PyCharm-friendly**: Stable interpreter path `/opt/conda/envs/app/bin/python`; symlink at `/workspace/bin/python` also available.
* **No shadowing**: Your code is mounted at `/workspace/src`, so `/workspace/bin` remains intact.

## Quickstart

```bash
make rebuild           # clean build + start dev
```

In PyCharm:

* Interpreter: **Docker Compose** → service **`dev`** → Python path: **`/opt/conda/envs/app/bin/python`**
* Jupyter: In a notebook, choose **Default (Managed/Auto-start)**

Optional external Jupyter:

```bash
make up-jupyter
# open http://localhost:8888
```

## Common tasks

```bash
make shell        # shell into dev
make logs-dev     # follow dev logs (shows initial seeding message on first run)
make seed-reset   # drop conda volume; next start reseeds from image
make prune        # cleanup
```

## When environment.yml changes

* Rebuild the image: `make rebuild` (or `docker compose build --no-cache`)
* If you want the persisted volume to reflect the new env, run `make seed-reset` to force a fresh seed on next start.
