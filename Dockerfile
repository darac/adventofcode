FROM python:3.10-slim AS python

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED true
WORKDIR /app


FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv


FROM python AS runtime

# Copy virtual env from python-deps stage
COPY --from=poetry /app /app
ENV PATH="/app/.venv/bin:$PATH"

# Run the executable
ENTRYPOINT [ "aoc" ]
CMD [ "-y", "2022" ]
