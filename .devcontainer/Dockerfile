# Pull rocker-org container
ARG VARIANT="4.4"
FROM ghcr.io/rocker-org/devcontainer/geospatial:${VARIANT}

# Install python & packages
COPY requirements.txt /tmp/pip-tmp/
RUN python3 -m pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt
