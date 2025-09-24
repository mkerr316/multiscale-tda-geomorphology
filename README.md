# multiscale-tda — Enthusiast-grade, locked Docker/Conda

## One-time (refresh locks)
make lock

## Build
make build   # or: docker build -t multiscale-tda .

## Run your code
make run     # or open a shell: make shell

### Notes
- `environment.yml` is human-readable; `conda-linux-64.lock` is explicit & deterministic.
- If you use pip, manage top deps in `requirements.in` and commit hashed `requirements.txt`.
- The image is multi-stage: reproducible builder → tiny runtime (non-root, `tini`).
