"""
DAG minimal : extraction de la table `customers` depuis esofa
vers le DWH local.
"""

import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, "/opt/airflow/extract")

from extract_customers import main as extract_customers_main

default_args = {
    "owner": "fleuria",
    "retries": 1,
}

with DAG(
    dag_id="esofa_extract_customers",
    description="Extraction de customers depuis esofa vers le DWH local",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["esofa", "extract"],
) as dag:

    extract_customers_task = PythonOperator(
        task_id="extract_customers",
        python_callable=extract_customers_main,
    )