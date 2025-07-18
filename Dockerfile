# syntax=docker/dockerfile:1.17@sha256:38387523653efa0039f8e1c89bb74a30504e76ee9f565e25c9a09841f9427b05
# Keep this syntax directive! It's used to enable Docker BuildKit

FROM ubuntu:noble@sha256:440dcf6a5640b2ae5c77724e68787a906afb8ddee98bf86db94eea8528c2c076 AS build

SHELL ["sh", "-exc"]

# renovate: suite=noble depName=build-essential
ARG BUILD_ESSENTIAL_VERSION="12.10ubuntu1"
# renovate: suite=noble depName=ca-certificates
ARG CA_CERTIFICATES_VERSION="20240203"
# renovate: suite=noble depName=python3-setuptools
ARG PYTHON3_SETUPTOOLS_VERSION="68.1.2-2ubuntu1.2"
# renovate: suite=noble depName=python3.12-dev
ARG PYTHON3_12_DEV_VERSION="3.12.3-1ubuntu0.5"

## Start Build Prep
RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    build-essential="${BUILD_ESSENTIAL_VERSION}" \
    ca-certificates="${CA_CERTIFICATES_VERSION}" \
    python3-setuptools="${PYTHON3_SETUPTOOLS_VERSION}" \
    python3.12-dev="${PYTHON3_12_DEV_VERSION}"
apt-get clean
EOT

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:5778d479c0fd7995fedd44614570f38a9d849256851f2786c451c220d7bd8ccd /uv /usr/local/bin/uv

# - Silence uv complaining about not being able to use hard links,
# - tell uv to byte-compile packages for faster application startups,
# - prevent uv from accidentally downloading isolated Python builds,
# - pick a Python,
# - and finally declare `/app` as the target for `uv sync`.
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.12 \
    UV_PROJECT_ENVIRONMENT=/app

### End Build Prep -- this is where your Dockerfile should start.

# Since there's no point in shipping lock files, we move them
# into a directory that is NOT copied into the runtime image.
# The trailing slash makes COPY create `/_lock/` automagically.
COPY pyproject.toml /_lock/
COPY uv.lock /_lock/

# Synchronize DEPENDENCIES without the application itself.
# This layer is cached until uv.lock or pyproject.toml change.
# You can create `/app` using `uv venv` in a separate `RUN`
# step to have it cached, but with uv it's so fast, it's not worth
# it and we let `uv sync` create it for us automagically.
RUN --mount=type=cache,target=/root/.cache <<EOT
cd /_lock
uv sync \
    --frozen \
    --no-dev \
    --no-install-project
EOT

# Now install the APPLICATION from `/src` without any dependencies.
# `/src` will NOT be copied into the runtime container.
# LEAVE THIS OUT if your application is NOT a proper Python package.
# We can’t use `uv sync` here because that only does editable installs:
# <https://github.com/astral-sh/uv/issues/5792>
COPY . /src
RUN --mount=type=cache,target=/root/.cache \
    uv pip install \
    --python="$UV_PROJECT_ENVIRONMENT" \
    --no-deps \
    /src

##########################################################################

FROM ubuntu:noble@sha256:440dcf6a5640b2ae5c77724e68787a906afb8ddee98bf86db94eea8528c2c076
SHELL ["sh", "-exc"]

# Optional: add the application virtualenv to search path.
ENV PATH=/app/bin:$PATH

# Don't run your app as root.
RUN <<EOT
groupadd -r app
useradd -r -d /app -g app -N app
EOT

ENTRYPOINT ["aoc"]
# See <https://hynek.me/articles/docker-signals/>.
STOPSIGNAL SIGINT

# renovate: suite=noble depName=python3.12
ARG PYTHON3_12_VERSION="3.12.3-1ubuntu0.5"
# renovate: suite=noble depName=libpython3.12t64
ARG LIBPYTHON3_12_VERSION="3.12.3-1ubuntu0.5"
# renovate: suite=noble depName=ca-certificates
ARG CA_CERTIFICATES_VERSION="20240203"
# renovate: suite=noble depName=libpcre3
ARG LIBPCRE3_VERSION="2:8.39-15build1"
# renovate: suite=noble depName=libxml2
ARG LIBXML2_VERSION="2.9.14+dfsg-1.3ubuntu3.3"

# Note how the runtime dependencies differ from build-time ones.
# Notably, there is no uv either!
RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    python3.12="${PYTHON3_12_VERSION}" \
    libpython3.12="${LIBPYTHON3_12_VERSION}" \
    ca-certificates="${CA_CERTIFICATES_VERSION}" \
    libpcre3="${LIBPCRE3_VERSION}" \
    libxml2="${LIBXML2_VERSION}"

apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

# Copy the pre-built `/app` directory to the runtime container
# and change the ownership to user app and group app in one step.
COPY --from=build --chown=app:app /app /app

# If your application is NOT a proper Python package that got
# pip-installed above, you need to copy your application into
# the container HERE:
# COPY . /app/whereever-your-entrypoint-finds-it

USER app
WORKDIR /app

# Strictly optional, but I like it for introspection of what I've built
# and run a smoke test that the application can, in fact, be imported.
RUN <<EOT
python -V
python -Im site
python -Ic 'import aoc'
EOT
