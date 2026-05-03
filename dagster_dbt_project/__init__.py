from dagster import Definitions, ScheduleDefinition, define_asset_job, AssetSelection
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject
from pathlib import Path

DBT_PROJECT_DIR = Path("/opt/dagster/dbt/clickhouse_dbt")

dbt_project = DbtProject(project_dir=DBT_PROJECT_DIR)
dbt_project.prepare_if_dev()

@dbt_assets(manifest=dbt_project.manifest_path)
def clickhouse_dbt_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["run", "-s", "+int_trades+"], context=context).stream()

dbt_job = define_asset_job(
    name="dbt_job_incremental",
    selection=AssetSelection.all()
)

dbt_schedule = ScheduleDefinition(
    job=dbt_job,
    cron_schedule="0 6 * * *",
)

defs = Definitions(
    assets=[clickhouse_dbt_assets],
    schedules=[dbt_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR)
    }
)