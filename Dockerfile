FROM python:3.12-slim

WORKDIR /app

ENV POETRY_VERSION=1.8.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1
RUN pip install "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev --no-interaction --no-root

COPY src ./src

RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# health check for k8s / docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/sanity-app/v1/health')" || exit 1

CMD ["uvicorn", "main.app:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
