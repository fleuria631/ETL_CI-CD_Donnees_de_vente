#!/usr/bin/env python3
"""
Test de connexion à PostgreSQL DWH
"""
import psycopg2
import sys

try:
    print("🔍 Tentative de connexion à PostgreSQL...")
    conn = psycopg2.connect(
        host='localhost',
        port=5434,
        database='esofa_dwh',
        user='dwh_user',
        password='dwh_password',
        client_encoding='UTF8'
    )
    print('✅ Connexion réussie!')
    
    cursor = conn.cursor()
    
    # Compter les tables
    cursor.execute('''
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    ''')
    result = cursor.fetchone()
    print(f'\n📊 Nombre de tables: {result[0]}')
    
    # Lister les tables
    cursor.execute('''
        SELECT table_schema, table_name FROM information_schema.tables 
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name
    ''')
    tables = cursor.fetchall()
    
    if tables:
        print('\n📋 Tables trouvées:')
        for schema, table in tables:
            cursor.execute(f'''
                SELECT COUNT(*) FROM "{schema}"."{table}"
            ''')
            count = cursor.fetchone()[0]
            print(f'   - {schema}.{table}: {count} lignes')
    else:
        print('\n⚠️  Aucune table trouvée. Vous devez exécuter les DAGs Airflow!')
    
    conn.close()
    print('\n✅ Test terminé avec succès!')
    sys.exit(0)
    
except Exception as e:
    print(f'❌ Erreur: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
