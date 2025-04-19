FROM ubuntu:22.04

# Étape 1 : Installer Python
RUN apt-get -y update && \
    apt-get install -y python3-pip

# Étape 2 : Définir le dossier de travail
WORKDIR /app

# Étape 3 : Copier les fichiers dans le conteneur
COPY . /app

# Étape 4 : Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Étape 5 : Exposer le port utilisé par Streamlit
EXPOSE 8501

# Étape 6 : Lancer l'application Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]