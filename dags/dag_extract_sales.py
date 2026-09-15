"""
DAG : extraction des ventes depuis esofa vers le DWH local.
Deux tâches séquentielles : sales_orders puis sales_order_items
(les items dépendent logiquement des commandes, donc on les enchaîne).
"""

import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, "/opt/airflow/extract")

from extract_sales_order_items import main as extract_sales_order_items_main
from extract_sales_orders import main as extract_sales_orders_main

default_args = {
    "owner": "fleuria",
    "retries": 1,
}

with DAG(
    dag_id="esofa_extract_sales",
    description="Extraction des ventes (sales_orders + sales_order_items) depuis esofa",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["esofa", "extract", "ventes"],
) as dag:

    extract_sales_orders_task = PythonOperator(
        task_id="extract_sales_orders",
        python_callable=extract_sales_orders_main,
    )

    extract_sales_order_items_task = PythonOperator(
        task_id="extract_sales_order_items",
        python_callable=extract_sales_order_items_main,
    )

    extract_sales_orders_task >> extract_sales_order_items_task