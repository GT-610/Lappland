# For developers
podman run -ti --name atLAs-dev -p 8022:8022 -v ./atLAs:/data/data/com.termux/files/home/atLAs docker.io/termux/termux-docker:x86_64 /bin/bash
podman exec --user system -ti atLAs-dev /bin/bash