# Dagster ClickHouse dbt Project

This repository sets up a complete orchestration environment using **Dagster** to manage and schedule a **dbt** project running against a **ClickHouse** database. The entire infrastructure is containerized using Docker and orchestrated via Docker Compose.

## How It Works

The project consists of several components working together to run and monitor dbt models on ClickHouse.

### 1. Docker Compose Architecture (`docker-compose.yml`)
The environment is orchestrated using Docker Compose, which spins up three essential services:
* **`dagster_postgresql`**: A PostgreSQL database (version 13) used by Dagster as its storage backend to keep track of run histories, event logs, schedules, and asset materializations.
* **`dagster_webserver`**: The Dagster UI service. It exposes the web interface on port `3001` (accessible via `localhost:3001`). It uses `workspace.yaml` to discover the data pipelines.
* **`dagster_daemon`**: A background service responsible for executing scheduled jobs, running sensors, and managing the run queue. 

The `docker-compose.yml` file also mounts external directories into the containers, notably mapping the host's dbt project (`../clickhouse-dbt/clickhouse_dbt`) to `/opt/dagster/dbt/clickhouse_dbt` inside the containers.

### 2. Dagster Configuration
* **`dagster.yaml`**: This file configures the Dagster instance to use the PostgreSQL database for storage and sets up the `DagsterDaemonScheduler` to handle cron-based schedules.
* **`workspace.yaml`**: This file tells the Dagster webserver and daemon where to find the pipeline definitions. It points to the `dagster_dbt_project` Python package.
* **`Dockerfile`**: Defines the custom Docker image used by the webserver and daemon. It is based on `python:3.11-slim` and installs necessary dependencies including `dagster`, `dagster-dbt`, `dagster-postgres`, and the `dbt-clickhouse` adapter.

### 3. Pipeline Definitions (`dagster_dbt_project/__init__.py`)
The actual data pipelines and orchestration logic are defined in Python:
* **dbt Integration**: It uses the `dagster-dbt` library to parse the dbt project located at `/opt/dagster/dbt/clickhouse_dbt`. It automatically creates Dagster software-defined assets from the dbt models using the `@dbt_assets` decorator.
* **Jobs & Scheduling**: A job named `dbt_job_incremental` is defined to materialize all the loaded dbt assets. This job is attached to a schedule (`dbt_schedule`) that runs automatically every day at 6:00 AM UTC (`0 6 * * *`).

## Getting Started 

1. Ensure you have Docker and Docker Compose installed.
2. Make sure your ClickHouse dbt project exists at `../clickhouse-dbt/clickhouse_dbt` relative to this directory, or update the volume mapping in `docker-compose.yml`.
3. Start the services:
   ```bash
   docker-compose up --build -d 
   ```
4. Access the Dagster UI by navigating to `http://localhost:3001` in your browser.