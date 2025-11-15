# syntax=docker/dockerfile:1.20@sha256:26147acbda4f14c5add9946e2fd2ed543fc402884fd75146bd342a7f6271dc1d
# Keep this syntax directive! It's used to enable Docker BuildKit

FROM debian:trixie-slim@sha256:a347fd7510ee31a84387619a492ad6c8eb0af2f2682b916ff3e643eb076f925a AS build

SHELL ["sh", "-exc"]

# renovate: suite=trixie depName=build-essential
ARG BUILD_ESSENTIAL_VERSION="12.12"
# renovate: suite=trixie depName=ca-certificates
ARG CA_CERTIFICATES_VERSION="20250419"
# renovate: suite=trixie depName=python3-setuptools
ARG PYTHON3_SETUPTOOLS_VERSION="78.1.1-0.1"
# renovate: suite=trixie depName=python3-dev
ARG PYTHON3_DEV_VERSION="3.13.5-1"

## Start Build Prep
RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    build-essential="${BUILD_ESSENTIAL_VERSION}" \
    ca-certificates="${CA_CERTIFICATES_VERSION}" \
    python3-dev="${PYTHON3_DEV_VERSION}" \
    python3-setuptools="${PYTHON3_SETUPTOOLS_VERSION}"
apt-get clean
EOT

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:08f409e1d53e77dfb5b65c788491f8ca70fe1d2d459f41c89afa2fcbef998abe /uv /usr/local/bin/uv

# - Silence uv complaining about not being able to use hard links,
# - tell uv to byte-compile packages for faster application startups,
# - prevent uv from accidentally downloading isolated Python builds,
# - pick a Python,
# - and finally declare `/app` as the target for `uv sync`.
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.13 \
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

FROM debian:trixie-slim@sha256:a347fd7510ee31a84387619a492ad6c8eb0af2f2682b916ff3e643eb076f925a
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

# renovate: suite=trixie depName=python3
ARG PYTHON3_VERSION="3.13.5-1"
# renovate: suite=trixie depName=libpython3.13
ARG LIBPYTHON3_VERSION="3.13.5-2"
# renovate: suite=trixie depName=python-is-python3
ARG PYTHON_IS_PYTHON3_VERSION="3.13.3-1"
# renovate: suite=trixie depName=ca-certificates
ARG CA_CERTIFICATES_VERSION="20250419"
# # renovate: suite=trixie depName=libpcre3
# ARG LIBPCRE3_VERSION="2:8.39-15build1"
# renovate: suite=trixie depName=libxml2
ARG LIBXML2_VERSION="2.12.7+dfsg+really2.9.14-2.1+deb13u2"

# Note how the runtime dependencies differ from build-time ones.
# Notably, there is no uv either!
RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    ca-certificates="${CA_CERTIFICATES_VERSION}" \
    libpython3.13="${LIBPYTHON3_VERSION}" \
    libxml2="${LIBXML2_VERSION}" \
    python3="${PYTHON3_VERSION}" \
    python-is-python3="${PYTHON_IS_PYTHON3_VERSION}"

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
