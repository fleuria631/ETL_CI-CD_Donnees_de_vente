"""
DAG minimal : extraction de la table `categories` depuis esofa
vers le DWH local. Une seule tâche pour valider le pattern
avant de l'étendre aux autres tables (products, customers, sales_orders, ...).
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

import sys
sys.path.insert(0, "/opt/airflow/extract")

from extract_categories import main as extract_categories_main


default_args = {
    "owner": "fleuria",
    "retries": 1,
}

with DAG(
    dag_id="esofa_extract_categories",
    description="Extraction de categories depuis esofa vers le DWH local",
    default_args=default_args,
    schedule=None,  # déclenchement manuel pour l'instant, pas de planification auto
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["esofa", "extract"],
) as dag:

    extract_categories_task = PythonOperator(
        task_id="extract_categories",
        python_callable=extract_categories_main,
    )