FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.2.1


WORKDIR /app

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock ./

RUN poetry install \
    --only main \
    --no-interaction \
    --no-ansi \
    --no-root

COPY src/ src/
COPY templates/ templates/


RUN chmod +x  \
    src/scripts/entrypoint.dev.sh \
    src/scripts/entrypoint.prod.sh

CMD ["poetry", "run", "sh", "src/scripts/entrypoint.dev.sh"]