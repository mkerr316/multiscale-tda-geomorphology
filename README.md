# Multiscale TDA Geomorphology Docker Environment

This repository provides a reproducible Docker environment for the multiscale TDA project, built with Mamba for fast and reliable dependency management.

## Quickstart

1.  **Build the Docker Image:**
    This command builds the `tda-geo:latest` image that all services will use. You only need to run this once, or again after you modify the `environment.yml` or `Dockerfile`.
    ```bash
    make build
    ```

## Usage Workflows

This setup supports multiple development workflows. Choose the one that best fits your needs.

### Workflow 1: PyCharm IDE (Recommended)

This workflow is ideal for interactive development, debugging, and using PyCharm's built-in Jupyter features.

1.  **Start the development container:**
    ```bash
    make up-dev
    ```
    *(This starts an idle container named `tda-geo-dev` in the background.)*

2.  **Configure PyCharm Interpreter:**
    * In PyCharm, go to `File > Settings > Project > Python Interpreter`.
    * Click **Add Interpreter** and select **On Docker Compose...**.
    * PyCharm will detect your `docker-compose.yml`. Select the **`dev`** service.
    * Set the interpreter path to `/workspace/bin/python`, which is a repository wrapper that forwards to the environment Python inside the container.
    * PyCharm is now configured. When you open a `.ipynb` file, it will automatically use its "Default (Auto-start)" Jupyter server configuration to launch and manage a server inside the running `dev` container.

### Workflow 2: Standalone Jupyter Lab (Browser-based)

Use this method if you prefer to work directly in Jupyter Lab in your web browser.

1.  **Start the Jupyter service:**
    ```bash
    make up-jupyter
    ```
    *(This starts a container named `tda-geo-jupyter` that immediately runs the Jupyter Lab server.)*

2.  **Access in Browser:**
    * Open your web browser and navigate to: `http://localhost:8888`

### Workflow 3: Command-Line Shell Access

For running scripts or using command-line tools directly inside the container.

1.  **Ensure the dev container is running:**
    ```bash
    make up-dev
    ```

2.  **Get a bash shell:**
    ```bash
    make shell
    ```

## Common Makefile Commands

* `make down`: Stop and remove all containers defined in this project.
* `make gpu`: Check for CUDA availability inside the `dev` container.
* `make prune`: Clean up all unused Docker containers, images, and system resources.