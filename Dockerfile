# syntax=docker/dockerfile:1.23@sha256:2780b5c3bab67f1f76c781860de469442999ed1a0d7992a5efdf2cffc0e3d769
# Keep this syntax directive! It's used to enable Docker BuildKit

FROM ghcr.io/prefix-dev/pixi@sha256:dcbd578e3cd2ab21bb16ddb872704c41f7bd1b49a02be5a8a5c062ada14b12f8 AS build

SHELL ["sh", "-exc"]
WORKDIR /app

# Copy only lock + manifest first (cache key layer)
COPY pyproject.toml pixi.lock README.md ./
COPY src/aoc src/aoc

# Synchronize DEPENDENCIES without the application itself.
# This layer is cached until pixi.lock or pyproject.toml change.
# You can create `/app` using `uv venv` in a separate `RUN`
# step to have it cached, but with pixi it's so fast, it's not worth
# it and we let `pixi install` create it for us automagically.
RUN --mount=type=cache,target=/root/.cache \
    pixi install --frozen

# Copy Application code
COPY . .

##########################################################################

FROM debian:13.4-slim@sha256:cedb1ef40439206b673ee8b33a46a03a0c9fa90bf3732f54704f99cb061d2c5a

SHELL ["sh", "-exc"]
WORKDIR /app

# renovate: suite=trixie depName=python3
ARG PYTHON3_VERSION="3.13.5-1"
# renovate: suite=trixie depName=libpython3.13
ARG LIBPYTHON3_VERSION="3.13.5-2"
# renovate: suite=trixie depName=python-is-python3
ARG PYTHON_IS_PYTHON3_VERSION="3.13.3-1"
# renovate: suite=trixie depName=ca-certificates
ARG CA_CERTIFICATES_VERSION="20250419"
# renovate: suite=trixie depName=libxml2
ARG LIBXML2_VERSION="2.12.7+dfsg+really2.9.14-2.1+deb13u2"
# renovate: suite=trixie depName=libstdc++6
ARG LIBSTDCXX6_VERSION="14.2.0-19"
# renovate: suite=trixie depName=libgl1
ARG LIBGL1_VERSION="1.7.0-1+b2"
# renovate: suite=trixie depName=libx11-6
ARG LIBX11_6_VERSION="2:1.8.12-1"
# renovate: suite=trixie depName=libxext6
ARG LIBXEXT6_VERSION="2:1.3.4-1+b3"
# renovate: suite=trixie depName=libxrender1
ARG LIBXRENDER1_VERSION="1:0.9.12-1"


# Note how the runtime dependencies differ from build-time ones.
# Notably, there is no uv either!
RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    ca-certificates="${CA_CERTIFICATES_VERSION}" \
    libstdc++6="${LIBSTDCXX6_VERSION}" \
    libgl1="${LIBGL1_VERSION}" \
    libx11-6="${LIBX11_6_VERSION}" \
    libxext6="${LIBXEXT6_VERSION}" \
    libxrender1="${LIBXRENDER1_VERSION}"
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

groupadd --system app
useradd --system --home-dir /app --gid app app
EOT


# Optional: add the application virtualenv to search path.
ENV PATH="/app/.pixi/envs/default/bin:$PATH"

# Copy the pre-built `/app` directory to the runtime container
# and change the ownership to user app and group app in one step.
COPY --from=build --chown=app:app /app /app

USER app

# Strictly optional, but I like it for introspection of what I've built
# and run a smoke test that the application can, in fact, be imported.
RUN <<EOT
python -V
python -Im site
python -Ic 'import aoc'
EOT

ENTRYPOINT ["/app/.pixi/envs/default/bin/aoc"]
# See <https://hynek.me/articles/docker-signals/>.
STOPSIGNAL SIGINT
