"""
Extraction de la table `products` depuis la base source `esofa`
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
    """Crée le schéma raw et la table staging si elles n'existent pas."""
    with dwh_conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.products (
                id INTEGER PRIMARY KEY,
                category_id INTEGER,
                name TEXT,
                description TEXT,
                image_url TEXT,
                active BOOLEAN,
                code TEXT,
                license_duration_type TEXT,
                license_duration_days INTEGER,
                install_guide_pdf_url TEXT,
                video_url TEXT,
                long_description TEXT,
                delivery_type TEXT,
                extracted_at TIMESTAMP DEFAULT now()
            );
        """)
    dwh_conn.commit()
    logger.info("Table raw.products prête.")


def extract_products(source_conn):
    with source_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT id, category_id, name, description, image_url, active, code,
                   license_duration_type, license_duration_days, install_guide_pdf_url,
                   video_url, long_description, delivery_type
            FROM products;
        """)
        rows = cur.fetchall()
    logger.info(f"{len(rows)} lignes extraites depuis la source.")
    return rows


def load_products(dwh_conn, rows):
    with dwh_conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE raw.products;")
        for row in rows:
            cur.execute(
                """
                INSERT INTO raw.products (
                    id, category_id, name, description, image_url, active, code,
                    license_duration_type, license_duration_days, install_guide_pdf_url,
                    video_url, long_description, delivery_type
                )
                VALUES (
                    %(id)s, %(category_id)s, %(name)s, %(description)s, %(image_url)s,
                    %(active)s, %(code)s, %(license_duration_type)s, %(license_duration_days)s,
                    %(install_guide_pdf_url)s, %(video_url)s, %(long_description)s, %(delivery_type)s
                );
                """,
                row,
            )
    dwh_conn.commit()
    logger.info(f"{len(rows)} lignes chargées dans raw.products.")


def main():
    logger.info("=== Début extraction products ===")
    source_conn = get_source_connection()
    dwh_conn = get_dwh_connection()

    try:
        create_staging_table(dwh_conn)
        rows = extract_products(source_conn)
        load_products(dwh_conn, rows)
    finally:
        source_conn.close()
        dwh_conn.close()

    logger.info("=== Fin extraction products ===")


if __name__ == "__main__":
    main()