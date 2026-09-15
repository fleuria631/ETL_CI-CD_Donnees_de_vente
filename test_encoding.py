#!/usr/bin/env python3
"""
Test rapide de la connexion SQLAlchemy avec URL encoding
"""
import os

os.environ["LC_ALL"] = "C.UTF-8"
os.environ["LANG"] = "C.UTF-8"

from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Charger les variables d'env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

print("🔍 Test de connexion SQLAlchemy avec URL encoding...")

# Récupérer les variables
host = os.getenv('DWH_DB_HOST')
if host == 'dwh_postgres':
    host = 'localhost'

user = os.getenv('DWH_DB_USER')
password = os.getenv('DWH_DB_PASSWORD')
port = os.getenv('DWH_DB_PORT')
dbname = os.getenv('DWH_DB_NAME')

# URL-encoder
user_encoded = quote_plus(user)
password_encoded = quote_plus(password)
dbname_encoded = quote_plus(dbname)

url = f"postgresql+psycopg2://{user_encoded}:{password_encoded}@{host}:{port}/{dbname_encoded}"

print("\n📌 Infos de connexion:")
print(f"   Host: {host}")
print(f"   User: {user}")
print(f"   Database: {dbname}")
print(f"   URL: {url}")

try:
    print("\n🔗 Création de l'engine...")
    engine = create_engine(url, connect_args={'client_encoding': 'utf8'})
    
    print("✅ Engine créé avec succès!")
    
    print("\n📊 Test de requête...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) as nb_tables FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog', 'information_schema')"))
        count = result.fetchone()[0]
        print(f"✅ Connexion réussie! {count} tables trouvées")
        
        # Tester une requête avec accents
        result = conn.execute(text("SELECT 'Café' as test"))
        test_result = result.fetchone()[0]
        print(f"✅ Données avec accents OK: {test_result!r}")
    
    print("\n✅✅✅ TEST RÉUSSI! ✅✅✅")
    
except Exception as e:
    print(f"❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
