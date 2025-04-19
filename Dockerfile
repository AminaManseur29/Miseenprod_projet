# Étape 1 : Base officielle
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers dans le conteneur
COPY . /app

# Étape 4 : Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Étape 5 : Exposer le port utilisé par Streamlit
EXPOSE 8501

# Étape 6 : Lancer l'application Streamlit
CMD ["streamlit", "run", "Accueil.py", "--server.port=8501", "--server.address=0.0.0.0"]