FROM python:3.12-slim

ENV APP_HOME=/app \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y curl && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

VOLUME ["/app/storage/"]

EXPOSE 3000
CMD ["poetry", "run", "python", "main.py"]
