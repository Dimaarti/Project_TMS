FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.2.1


WORKDIR /app
RUN pip install "poetry==${POETRY_VERSION}"
COPY pyproject.toml poetry.lock ./
RUN poetry install \
    --no-root

COPY src/ src/
COPY templates/ templates/


RUN chmod +x src/scripts/entrypoint.dev.sh
CMD ["poetry", "run", "sh", "src/scripts/entrypoint.dev.sh"]