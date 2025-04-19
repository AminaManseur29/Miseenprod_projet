# Étape 1 : Image de base
FROM python:3.8-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les dépendances
COPY requirements.txt .

# Étape 4 : Installer les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier le code de l'application
COPY . .

# Étape 6 : Exposer le port utilisé par Streamlit
EXPOSE 8501

# Étape 7 : Lancer l'application Streamlit
CMD ["streamlit", "run", "Accueil.py"]