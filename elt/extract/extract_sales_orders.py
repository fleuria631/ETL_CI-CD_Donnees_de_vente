"""
Extraction de la table `sales_orders` depuis la base source `esofa`
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
            CREATE TABLE IF NOT EXISTS raw.sales_orders (
                id INTEGER PRIMARY KEY,
                code TEXT,
                customer_id INTEGER,
                quotation_id INTEGER,
                status TEXT,
                customer_po_ref TEXT,
                total_amount NUMERIC,
                notes TEXT,
                confirmed_at TIMESTAMP,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                currency TEXT,
                extracted_at TIMESTAMP DEFAULT now()
            );
        """)
    dwh_conn.commit()
    logger.info("Table raw.sales_orders prête.")


def extract_sales_orders(source_conn):
    with source_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT id, code, customer_id, quotation_id, status, customer_po_ref,
                   total_amount, notes, confirmed_at, created_at, updated_at, currency
            FROM sales_orders;
        """)
        rows = cur.fetchall()
    logger.info(f"{len(rows)} lignes extraites depuis la source.")
    return rows


def load_sales_orders(dwh_conn, rows):
    with dwh_conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE raw.sales_orders;")
        for row in rows:
            cur.execute(
                """
                INSERT INTO raw.sales_orders (
                    id, code, customer_id, quotation_id, status, customer_po_ref,
                    total_amount, notes, confirmed_at, created_at, updated_at, currency
                )
                VALUES (
                    %(id)s, %(code)s, %(customer_id)s, %(quotation_id)s, %(status)s,
                    %(customer_po_ref)s, %(total_amount)s, %(notes)s, %(confirmed_at)s,
                    %(created_at)s, %(updated_at)s, %(currency)s
                );
                """,
                row,
            )
    dwh_conn.commit()
    logger.info(f"{len(rows)} lignes chargées dans raw.sales_orders.")


def main():
    logger.info("=== Début extraction sales_orders ===")
    source_conn = get_source_connection()
    dwh_conn = get_dwh_connection()

    try:
        create_staging_table(dwh_conn)
        rows = extract_sales_orders(source_conn)
        load_sales_orders(dwh_conn, rows)
    finally:
        source_conn.close()
        dwh_conn.close()

    logger.info("=== Fin extraction sales_orders ===")


if __name__ == "__main__":
    main()