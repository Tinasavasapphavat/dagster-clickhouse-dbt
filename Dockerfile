FROM python:3.11-slim

WORKDIR /opt/dagster/app

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install \
    dagster \
    dagster-webserver \
    dagster-dbt \
    dagster-postgres \
    dbt-clickhouse \
    --no-cache-dir

COPY . .
