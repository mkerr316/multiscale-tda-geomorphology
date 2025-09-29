# config/jupyter_server_config.py

# Allow the server to run as the root user (as is common in Docker)
c.ServerApp.allow_root = True

# Listen on all network interfaces
c.ServerApp.ip = '0.0.0.0'

# Disable browser auto-opening
c.ServerApp.open_browser = False

# Allow requests from any origin to support IDEs
c.ServerApp.allow_origin = '*'

# Set the default working directory
c.ServerApp.root_dir = '/workspace'

# REMOVED: Let PyCharm/Jupyter manage the token dynamically for managed servers.
# c.ServerApp.token = 'tda-geo-secret-token'