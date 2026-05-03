from setuptools import find_packages, setup

setup(
    name="dagster_dbt_project",
    packages=find_packages(),
    install_requires=[
        "dagster",
        "dagster-dbt", 
        "dbt-clickhouse",
    ],
)
