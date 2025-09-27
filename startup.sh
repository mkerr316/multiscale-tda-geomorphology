#!/bin/bash

# Activate the micromamba environment
eval "$(micromamba shell hook -s bash)"
micromamba activate app

# Start Jupyter Lab in the background
# The server will be accessible from your host machine on port 8888
# --ip=0.0.0.0 makes it accessible outside the container
# --allow-root is necessary as docker often runs as root
# --no-browser prevents it from trying to open a browser inside the container
# --NotebookApp.token='' disables the need for a login token
jupyter lab --ip=0.0.0.0 --port=8888 --allow-root --no-browser --NotebookApp.token='' &

# Keep the container running by tailing a log file or using another long-running process
# This is a common pattern to keep a container alive after a background process starts
tail -f /dev/null
