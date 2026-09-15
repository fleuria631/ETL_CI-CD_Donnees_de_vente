"""
Extraction de la table `categories` depuis la base source `esofa`
vers le Data Warehouse local (staging), en mode full-refresh
(on vide et on recharge à chaque exécution — le plus simple pour démarrer).
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
            CREATE TABLE IF NOT EXISTS raw.categories (
                id INTEGER PRIMARY KEY,
                name TEXT,
                slug TEXT,
                parent_id INTEGER,
                active BOOLEAN,
                extracted_at TIMESTAMP DEFAULT now()
            );
        """)
    dwh_conn.commit()
    logger.info("Table raw.categories prête.")


def extract_categories(source_conn):
    with source_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT id, name, slug, parent_id, active FROM categories;")
        rows = cur.fetchall()
    logger.info(f"{len(rows)} lignes extraites depuis la source.")
    return rows


def load_categories(dwh_conn, rows):
    with dwh_conn.cursor() as cur:
        # Full-refresh simple : on vide puis on réinsère
        cur.execute("TRUNCATE TABLE raw.categories;")
        for row in rows:
            cur.execute(
                """
                INSERT INTO raw.categories (id, name, slug, parent_id, active)
                VALUES (%(id)s, %(name)s, %(slug)s, %(parent_id)s, %(active)s);
                """,
                row,
            )
    dwh_conn.commit()
    logger.info(f"{len(rows)} lignes chargées dans raw.categories.")


def main():
    logger.info("=== Début extraction categories ===")
    source_conn = get_source_connection()
    dwh_conn = get_dwh_connection()

    try:
        create_staging_table(dwh_conn)
        rows = extract_categories(source_conn)
        load_categories(dwh_conn, rows)
    finally:
        source_conn.close()
        dwh_conn.close()

    logger.info("=== Fin extraction categories ===")


if __name__ == "__main__":
    main()