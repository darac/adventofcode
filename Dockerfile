# syntax=docker/dockerfile:1.16
# Keep this syntax directive! It's used to enable Docker BuildKit

FROM ubuntu:noble AS build

SHELL ["sh", "-exc"]

## Start Build Prep
RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    build-essential \
    ca-certificates \
    python3-setuptools \
    python3.12-dev
apt-get clean
EOT

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

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

FROM ubuntu:noble
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

# Note how the runtime dependencies differ from build-time ones.
# Notably, there is no uv either!
RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    python3.12 \
    libpython3.12 \
    ca-certificates \
    libpcre3 \
    libxml2

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
