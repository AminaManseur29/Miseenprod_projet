<img src="pictures/LOGO-ENSAE.png" alt="Logo ENSAE" width="200"/>

<p align="right">
  <img src="https://img.shields.io/badge/Python-3.8-blue.svg" alt="Python 3.8" />
  <img src="https://img.shields.io/badge/Streamlit-1.0-orange.svg" alt="Streamlit" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT" />
  <a href="https://github.com/AminaManseur29/Miseenprod_projet/actions/workflows/prod.yaml">
    <img src="https://github.com/AminaManseur29/Miseenprod_projet/actions/workflows/prod.yaml/badge.svg" alt="Construction image Docker" />
  </a>
</p>

---

# Sélection de candidats pour les départements RH

## 🧠 Présentation du projet

Ce projet explore différents modèles pour accompagner les **ressources humaines** dans le processus de **sélection de candidats** à l’embauche. Il vise à **faciliter la prise de décision** tout en prenant en compte des critères **ESG**, notamment en lien avec **l’égalité de genre**.

Le projet comprend :
- le nettoyage et l’enrichissement de données issues de l’enquête StackOverflow,
- la modélisation du processus de sélection,
- une application interactive développée avec Streamlit.

---

## 🌐 Déploiement de l'application
L’application a été déployée dans deux environnements distincts :
- Streamlit Cloud :
Elle est accessible à l’adresse suivante :
👉 [https://ensae-project-genderequity.streamlit.app/](https://ensae-project-genderequity.streamlit.app/)

- SSPCloud : 
Une seconde version de l’application a été déployée sur le cluster Kubernetes de SSPCloud, à l’adresse :
👉 [https://streamlit-ensae-project-genderequity.lab.sspcloud.fr/](https://streamlit-ensae-project-genderequity.lab.sspcloud.fr/)

Le déploiement sur SSPCloud est automatisé via un dépôt dédié, accessible ici : 
👉 [https://github.com/AminaManseur29/application-deployment/](https://github.com/AminaManseur29/application-deployment/)

---

## 📁 Arborescence du projet

```bash
.
├── data/                                # Données brutes et nettoyées
├── logs/                                # Logs des différents scripts
├── notebooks/                           # Notebook principal du projet
├── output/                              # Résultats des modèles
├── pages/                               # Pages de l'application Streamlit
├── pictures/                            # Images utilisées dans le README
├── src/
│   ├── __init__.py                      # Fichier d'initialisation du package
│   ├── data_preprocessing.py            # Scripts de nettoyage et de préparation des données
│   ├── models_baseline_train_save.py    # Entraînement et sauvegarde des modèles de base
│   ├── models_mitigated_train_save.py   # Entraînement et sauvegarde des modèles atténués
│   ├── models_visualisation_utils.py    # Utilitaires pour la visualisation des modèles
│   └── plot_utils.py                    # Utilitaires pour la création de graphiques
├── .env                                 # Variables d’environnement
├── .gitignore                           # Fichiers et dossiers ignorés par Git
├── Accueil.py                           # Page d'accueil de l'application Streamlit
├── LICENCE                              # Licence du projet
├── README.md                            # Documentation du projet
└── requirements.txt                     # Dépendances Python

```
---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/louiseligonniere/Miseenprod_projet.git
cd Miseenprod_projet
```

### 2. Créer et activer un environnement virtuel

Si vous utilisez le SSPCloud, il faut dans un premier temps désactiver l'environnement virtuel par défaut de la plateforme avec : 
```bash
conda deactivate
```
Ensuite, vous pouvez créer et activer votre environnement avec : 
```bash
python -m venv env
source env/bin/activate        # Sous Windows : env\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 🚀 Lancer l'application Streamlit
Une fois les installations effectuées, vous pouvez lancer l’application en exécutant la commande suivante dans un terminal :
```bash
streamlit run Accueil.py
```

Trois cas peuvent alors se présenter :

✅ Une fenêtre s’ouvre automatiquement avec le message :
"Your application running on port ... is available"
→ Cliquez sur "Open in Browser".

🌐 Trois liens sont affichés (Local / Network / External URL) :
→ Cliquez sur le lien Local URL (ex. http://localhost:8501).

🛠 Si rien ne se lance :
→ Allez dans l’onglet "PORTS" (dans VSCode ou Onyxia),
puis cliquez sur l’icône 🌐 "Open in Browser" dans la colonne "Forwarded Address" pour ouvrir l’app dans le navigateur.

## 📊 Fonctionnalités de l'application
L'application Streamlit permet :
- une visualisation interactive des variables d’intérêt,
- l’exploration des modèles prédictifs utilisés,
- une navigation claire entre plusieurs pages de l’interface.

## 📦 Données
- Source principale : Enquête développeurs StackOverflow
- Données enrichies par : 
      - du web scraping,
      - des fichiers Excel externes (langues, pays, ISO...).

## 🔐 Fichier .env
Le fichier .env, déjà présent à la racine du projet, contient les chemins vers les jeux de données publics utilisés dans l’application. Ces données sont hébergées sur des ressources accessibles librement (comme le SSPCloud).

```bash
stack_users_data_path=...
countries_lang_data_path=...
iso_url=...
```
### Explication :
- **stack_users_data_path** : chemin vers les données de l’enquête StackOverflow utilisées pour analyser les utilisateurs.
- **countries_lang_data_path** : chemin vers les données contenant des informations supplémentaires sur les pays et les langues.
- **iso_url** : URL d’une ressource en ligne contenant notamment les codes ISO des pays.

## 📓 Notebook
Un seul notebook synthétise l’analyse : notebooks/Notebook_Project.ipynb

## 👥 Auteurs et contributrices
Auteurs initiaux : Pierre Clayton, Clément de Lardemelle, Louise Ligonnière

Contributrices : Amina Manseur, Lila Mekki

Ce projet a été repris et adapté par Louise, Lila et Amina dans le but de le déployer sous forme d’application web interactive avec Streamlit.

## 📝 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus d'informations.
