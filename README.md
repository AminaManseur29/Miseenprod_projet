<img src="pictures/LOGO-ENSAE.png" alt="Logo ENSAE" width="200"/>

<p align="right">
  <img src="https://img.shields.io/badge/Python-3.8-blue.svg" alt="Python 3.8" />
  <img src="https://img.shields.io/badge/Streamlit-1.0-orange.svg" alt="Streamlit" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT" />
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

## 🌐 Accéder à l'application déployée

L'application est déployée et accessible à l'adresse suivante :  
[https://miseenappprojet-zrcijatvpprbtfrd46xevu.streamlit.app/](https://miseenappprojet-zrcijatvpprbtfrd46xevu.streamlit.app/)

Vous pouvez tester l'application en temps réel en suivant ce lien.

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
Ensuite, vous pouvez créer votre environnement avec : 
```bash
python -m venv env
source env/bin/activate        # Sous Windows : env\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 🔐 Fichier .env
Créer un fichier .env à la racine du projet contenant les chemins vers les jeux de données hébergés sur le cloud (par ex. SSPCloud) :

```bash
stack_users_data_path=...
countries_lang_data_path=...
iso_url=...
```
### Explication :
- **stack_users_data_path** : Cette variable pointe vers les données d'enquête StackOverflow, qui sont utilisées pour analyser les utilisateurs.
- **countries_lang_data_path** : Elle est utilisée pour localiser un fichier avec des informations supplémentaires sur les pays et les langues.
- **iso_url** : L'URL de cette variable sert à accéder à une ressource en ligne contenant des données ISO, utiles pour l'analyse.

## 🚀 Lancer l'application Streamlit
Après avoir effectué les installations nécessaires, l'application Streamlit peut être lancée directement depuis un terminal via :
```bash
streamlit run Accueil.py
```
Suite à cette commande, une fenêtre devrait s'ouvrir indiquant "Your application running on port ... is available". Il suffit alors de cliquer sur "Open in Browser" pour l'ouvrir. 

Si la fenêtre ne s'affiche pas, il faut aller dans l'onglet "PORTS" et cliquer sur l'icône 🌐 dans "Forwarded Address" pour accéder à l'application. 

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

## 📓 Notebook
Un seul notebook synthétise l’analyse : notebooks/Notebook_Project.ipynb

## 👥 Auteurs et contributrices
Auteurs initiaux : Pierre Clayton, Clément de Lardemelle, Louise Ligonnière

Contributrices : Amina Manseur, Lila Mekki

Ce projet a été repris et adapté par Louise, Lila et Amina dans le but de le déployer sous forme d’application web interactive avec Streamlit.

## 📝 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus d'informations.
