import os
os.environ["LC_ALL"] = "C"
os.environ["LANG"] = "C"

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool
import pandas as pd
import streamlit as st

# .env est à la racine du projet, un niveau au-dessus de dashboard/
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


@st.cache_resource
def get_engine():
    """
    Crée et met en cache l'engine SQLAlchemy pour toute la durée de vie
    de la session Streamlit (au lieu d'en recréer un à chaque requête).
    """
    host = os.getenv('DWH_DB_HOST')
    port = os.getenv('DWH_DB_PORT')

    # Le dashboard tourne sur Windows (hors Docker) : il faut réécrire
    # le host/port internes au réseau Docker vers ceux exposés sur l'hôte.
    if host == 'dwh_postgres':
        host = 'localhost'
        port = '5434'  # port exposé côté hôte (mapping "5434:5432" dans docker-compose)

    user = os.getenv('DWH_DB_USER')
    password = os.getenv('DWH_DB_PASSWORD')
    dbname = os.getenv('DWH_DB_NAME')

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    engine = create_engine(
        url,
        poolclass=QueuePool,
        connect_args={
            'client_encoding': 'utf8',
            'options': '-c lc_messages=C'  # force les messages d'erreur serveur en ASCII
        }
    )

    @event.listens_for(engine, "connect")
    def set_encoding(dbapi_conn, connection_record):
        dbapi_conn.set_client_encoding('UTF8')

    return engine


def run_query(query: str) -> pd.DataFrame:
    engine = get_engine()
    return pd.read_sql(query, engine)