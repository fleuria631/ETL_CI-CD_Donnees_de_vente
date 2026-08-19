#!/usr/bin/env python3
"""
Script de diagnostic complet pour l'erreur Unicode
"""
import os
import sys

print("=" * 60)
print("🔍 DIAGNOSTIC COMPLET - ERREUR UNICODE")
print("=" * 60)

# 1. Vérifier l'encodage Python
print("\n1️⃣  ENCODAGE PYTHON:")
print(f"   Encoding par défaut: {sys.getdefaultencoding()}")
print(f"   File encoding: {sys.getfilesystemencoding()}")
print(f"   LC_ALL: {os.environ.get('LC_ALL', 'non défini')}")
print(f"   LANG: {os.environ.get('LANG', 'non défini')}")

# 2. Vérifier le chargement des variables d'env
print("\n2️⃣  VARIABLES D'ENVIRONNEMENT:")
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
print(f"   Chemin .env: {env_path}")
print(f"   Fichier existe: {env_path.exists()}")

if env_path.exists():
    # Lire le .env directement
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"   Contenu du .env (premieres lignes):")
    for line in lines[:10]:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            print(f"      {key} = {repr(value)}")

# 3. Charger les variables avec dotenv
load_dotenv(dotenv_path=env_path)

print("\n3️⃣  VARIABLES CHARGÉES PAR DOTENV:")
host = os.getenv('DWH_DB_HOST')
user = os.getenv('DWH_DB_USER')
password = os.getenv('DWH_DB_PASSWORD')
port = os.getenv('DWH_DB_PORT')
dbname = os.getenv('DWH_DB_NAME')

print(f"   DWH_DB_HOST: {repr(host)} (type: {type(host).__name__})")
print(f"   DWH_DB_USER: {repr(user)} (type: {type(user).__name__})")
print(f"   DWH_DB_PASSWORD: {repr(password)} (type: {type(password).__name__})")
print(f"   DWH_DB_PORT: {repr(port)} (type: {type(port).__name__})")
print(f"   DWH_DB_NAME: {repr(dbname)} (type: {type(dbname).__name__})")

# 4. Construire l'URL et vérifier l'encodage
print("\n4️⃣  CONSTRUCTION URL DE CONNEXION:")
if host == 'dwh_postgres':
    host = 'localhost'

url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
print(f"   URL brute: {url}")
print(f"   Encodage URL: {url.encode('utf-8')}")
print(f"   Longueur: {len(url)} caractères")

# 5. Essayer de décoder les bytes
print("\n5️⃣  TEST DE DÉCODAGE:")
try:
    url_bytes = url.encode('utf-8')
    url_decoded = url_bytes.decode('utf-8')
    print(f"   ✅ URL peut être encodée/décodée en UTF-8")
    print(f"   Byte à position 103: {repr(url_bytes[103:110] if len(url_bytes) > 103 else 'N/A')}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 6. Tester la connexion avec SQLAlchemy
print("\n6️⃣  TEST CONNEXION SQLALCHEMY:")
try:
    from sqlalchemy import create_engine
    from sqlalchemy.pool import QueuePool
    
    engine = create_engine(
        url,
        poolclass=QueuePool,
        connect_args={'client_encoding': 'utf8'},
        echo=False
    )
    
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print(f"   ✅ Connexion SQLAlchemy réussie!")
except Exception as e:
    print(f"   ❌ Erreur SQLAlchemy: {e}")
    import traceback
    traceback.print_exc()

# 7. Tester avec psycopg2 directement
print("\n7️⃣  TEST CONNEXION PSYCOPG2 DIRECT:")
try:
    import psycopg2
    
    conn = psycopg2.connect(
        host=host,
        port=int(port),
        database=dbname,
        user=user,
        password=password,
        client_encoding='UTF8'
    )
    print(f"   ✅ Connexion psycopg2 réussie!")
    conn.close()
except Exception as e:
    print(f"   ❌ Erreur psycopg2: {e}")

print("\n" + "=" * 60)
print("✅ Diagnostic terminé!")
print("=" * 60)
