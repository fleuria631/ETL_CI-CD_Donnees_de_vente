"""
Extraction de la table `customers` depuis la base source `esofa`
vers le Data Warehouse local (staging), en mode full-refresh.
"""

import os
import logging
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
    """Crée le schéma raw et la table staging si elles n'existent pas."""
    with dwh_conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.customers (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                customer_type TEXT,
                address TEXT,
                company_name TEXT,
                nif TEXT,
                rcs TEXT,
                stat TEXT,
                vat_number TEXT,
                company_number TEXT,
                utr_number TEXT,
                extracted_at TIMESTAMP DEFAULT now()
            );
        """)
    dwh_conn.commit()
    logger.info("Table raw.customers prête.")


def extract_customers(source_conn):
    with source_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT id, user_id, first_name, last_name, phone, created_at, updated_at,
                   customer_type, address, company_name, nif, rcs, stat,
                   vat_number, company_number, utr_number
            FROM customers;
        """)
        rows = cur.fetchall()
    logger.info(f"{len(rows)} lignes extraites depuis la source.")
    return rows


def load_customers(dwh_conn, rows):
    with dwh_conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE raw.customers;")
        for row in rows:
            cur.execute(
                """
                INSERT INTO raw.customers (
                    id, user_id, first_name, last_name, phone, created_at, updated_at,
                    customer_type, address, company_name, nif, rcs, stat,
                    vat_number, company_number, utr_number
                )
                VALUES (
                    %(id)s, %(user_id)s, %(first_name)s, %(last_name)s, %(phone)s,
                    %(created_at)s, %(updated_at)s, %(customer_type)s, %(address)s,
                    %(company_name)s, %(nif)s, %(rcs)s, %(stat)s,
                    %(vat_number)s, %(company_number)s, %(utr_number)s
                );
                """,
                row,
            )
    dwh_conn.commit()
    logger.info(f"{len(rows)} lignes chargées dans raw.customers.")


def main():
    logger.info("=== Début extraction customers ===")
    source_conn = get_source_connection()
    dwh_conn = get_dwh_connection()

    try:
        create_staging_table(dwh_conn)
        rows = extract_customers(source_conn)
        load_customers(dwh_conn, rows)
    finally:
        source_conn.close()
        dwh_conn.close()

    logger.info("=== Fin extraction customers ===")


if __name__ == "__main__":
    main()