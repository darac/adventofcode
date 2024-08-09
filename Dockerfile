# syntax=docker/dockerfile:1
# Keep this syntax directive! It's used to enable Docker BuildKit

ARG PYTHON_BASE=3.12-slim

################################
# PYTHON-BASE
# Sets up all our shared environment variables
################################
FROM python:$PYTHON_BASE AS builder

# install PDM
RUN pip install -U pdm

# disable update check
ENV PDM_CHECK_UPDATE=false

# Copy files
COPY pyproject.toml pdm.lock README.md /app/
COPY aoc/ /app/aoc

# Install Dependencies and project into the local packages directory
WORKDIR /app
RUN pdm install --check --prod --no-editable

################################
# PRODUCTION
# Final image used for runtime
################################
FROM python:$PYTHON_BASE

COPY --from=builder /app/.venv/ /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY aoc/ /app/aoc
COPY tests/ /app/tests

# Run the executable
ENTRYPOINT ["pdm", "run", "aoc"]
