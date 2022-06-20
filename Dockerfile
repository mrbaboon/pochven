FROM    python:3.10

ENV     YOUR_ENV=${YOUR_ENV} \
        PYTHONFAULTHANDLER=1 \
        PYTHONUNBUFFERED=1 \
        PYTHONHASHSEED=random \
        PIP_NO_CACHE_DIR=off \
        PIP_DISABLE_PIP_VERSION_CHECK=on \
        PIP_DEFAULT_TIMEOUT=100 \
        POETRY_VERSION=1.1.13

# System deps:
RUN         pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR     /code
COPY        poetry.lock pyproject.toml /code/

RUN         poetry config virtualenvs.create false && \
            poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi



RUN         useradd -ms /bin/bash appuser
WORKDIR     /code
USER        appuser

COPY        --chown=appuser:appuser . /code/


CMD         ["gunicorn", "-b=0.0.0.0:8000", "app.wsgi"]
