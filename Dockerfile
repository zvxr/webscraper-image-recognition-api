FROM python:3.11-slim AS base

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# Install dependencies
FROM base AS deps
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install dev dependencies and tests for development image
FROM deps AS development
COPY ./requirements-dev.txt /code/requirements-dev.txt
COPY ./tests /code/tests
RUN pip install -r /code/requirements-dev.txt

# app must be discoverable
ENV PYTHONPATH=/code
