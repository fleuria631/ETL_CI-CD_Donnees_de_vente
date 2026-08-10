"""
DAG minimal : extraction de la table `products` depuis esofa
vers le DWH local.
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

import sys
sys.path.insert(0, "/opt/airflow/extract")

from extract_products import main as extract_products_main


default_args = {
    "owner": "fleuria",
    "retries": 1,
}

with DAG(
    dag_id="esofa_extract_products",
    description="Extraction de products depuis esofa vers le DWH local",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["esofa", "extract"],
) as dag:

    extract_products_task = PythonOperator(
        task_id="extract_products",
        python_callable=extract_products_main,
    )