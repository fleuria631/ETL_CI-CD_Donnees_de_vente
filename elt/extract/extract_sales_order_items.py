"""
Extraction de la table `sales_order_items` depuis la base source `esofa`
vers le Data Warehouse local (staging), en mode full-refresh.
"""

import logging
import os

import psycopg2
import psycopg2.extras

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_source_connection():
    return psycopg2.connect(
        host=os.environ["SOURCE_DB_HOST"],
        port=os.environ["SOURCE_DB_PORT"],
        dbname=os.environ["SOURCE_DB_NAME"],
        user=os.environ["SOURCE_DB_USER"],
        password=os.environ["SOURCE_DB_PASSWORD"],
    )


def get_dwh_connection():
    return psycopg2.connect(
        host=os.environ["DWH_DB_HOST"],
        port=os.environ["DWH_DB_PORT"],
        dbname=os.environ["DWH_DB_NAME"],
        user=os.environ["DWH_DB_USER"],
        password=os.environ["DWH_DB_PASSWORD"],
    )


def create_staging_table(dwh_conn):
    with dwh_conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.sales_order_items (
                id INTEGER PRIMARY KEY,
                sales_order_id INTEGER,
                product_id INTEGER,
                variant_id INTEGER,
                quotation_item_id INTEGER,
                quantity NUMERIC,
                quantity_delivered NUMERIC,
                unit_price NUMERIC,
                discount_percent NUMERIC,
                line_total NUMERIC,
                description TEXT,
                extracted_at TIMESTAMP DEFAULT now()
            );
        """)
    dwh_conn.commit()
    logger.info("Table raw.sales_order_items prête.")


def extract_sales_order_items(source_conn):
    with source_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT id, sales_order_id, product_id, variant_id, quotation_item_id,
                   quantity, quantity_delivered, unit_price, discount_percent,
                   line_total, description
            FROM sales_order_items;
        """)
        rows = cur.fetchall()
    logger.info(f"{len(rows)} lignes extraites depuis la source.")
    return rows


def load_sales_order_items(dwh_conn, rows):
    with dwh_conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE raw.sales_order_items;")
        for row in rows:
            cur.execute(
                """
                INSERT INTO raw.sales_order_items (
                    id, sales_order_id, product_id, variant_id, quotation_item_id,
                    quantity, quantity_delivered, unit_price, discount_percent,
                    line_total, description
                )
                VALUES (
                    %(id)s, %(sales_order_id)s, %(product_id)s, %(variant_id)s,
                    %(quotation_item_id)s, %(quantity)s, %(quantity_delivered)s,
                    %(unit_price)s, %(discount_percent)s, %(line_total)s, %(description)s
                );
                """,
                row,
            )
    dwh_conn.commit()
    logger.info(f"{len(rows)} lignes chargées dans raw.sales_order_items.")


def main():
    logger.info("=== Début extraction sales_order_items ===")
    source_conn = get_source_connection()
    dwh_conn = get_dwh_connection()

    try:
        create_staging_table(dwh_conn)
        rows = extract_sales_order_items(source_conn)
        load_sales_order_items(dwh_conn, rows)
    finally:
        source_conn.close()
        dwh_conn.close()

    logger.info("=== Fin extraction sales_order_items ===")


if __name__ == "__main__":
    main()