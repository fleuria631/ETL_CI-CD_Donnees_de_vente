FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système nécessaires pour psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste des fichiers (app.py, db.py, etc.)
COPY . .

# Exposer le port par défaut de Streamlit
EXPOSE 8501

# Commande pour démarrer l'application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
