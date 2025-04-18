 <img src="https://github.com/louiseligonniere/Miseenprod_projet/blob/main/LOGO-ENSAE.png?raw=true" alt="ENSAE logo" width="200"/>


![License](https://github.com/louiseligonniere/Miseenprod_projet/blob/main/LICENSE)

---

# Candidate selection for HR department

## Overview
This project explores models for the selection of applicants in an hiring process, in order to facilitate the work of the HR department of companies. It accounts for ESG requirements, and more specifically gender oriented. 

## Project structure 

```
.
├── data/                    # Folder containing the data used 
├── logs/                    # Folder containing the logs of the different scripts
├── notebooks                # Notebook of the project 
├── output                   # Results of the models   
├── pages/                   # Streamlit pages 
├── pictures/                # Some pictures for the Readme
├── src
   ├── __init__              # Initialisation file
   ├── data_preprocessing    # Cleaning and merging of datasets
   ├── models                # Implemented models
   ├── evaluation            # Evaluation of the models
   └── main                  # Execution file 
├── .env                     # Environment variables stored 
├── .gitignore               # Files to ignore 
├── Accueil                  # Python file for the welcoming page of the project
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies

```


## Installation 

### Step 1 : Clone the repository 

```
git clone 

```
### Step 2 : Create a virtual environment 

```
python -m venv env
source env/bin/activate # On Windows, use `env\Scripts\activate`

```

### Step 3 : Install dependencies 

```
pip install -r requirements.txt 

```
### Step 4 : Launch the app 



# How to use it ? 


Par ailleurs, une application développée via Streamlit présente la distribution des variables d'intérêt et facilite la navigation entre les différents graphiques. Elle présente aussi de façon interactive les modèles réalisés. 

**Nous vous invitons à consulter cette application** (le contenu de ses pages est toutefois reporté dans les sections 4 à 6 du notebook).
à compléter 


*Étapes pour lancer l'application* : 
- il est nécessaire de commencer par exécuter l'intégralité du notebook (sinon, la page présentant les modèles ne charge pas entièrement),
- ouvrir un terminal,
- se placer dans le dossier 'Projet-Python-ENSAE' (qui contient le script de lancement de l'application 'Accueil.py' et le dossier 'pages' contenant les scripts des pages),
- exécuter la commande suivante : streamlit run Accueil.py --server.port 5000 --server.address 0.0.0.0

**Attention** : si vous consultez le Notebook dans un environnement Jupyter via le SSP Cloud, il est nécessaire d'avoir ouvert au préalable un *custom service port* au lancement du service Jupyter. Vous pouvez le faire dans la 'Configuration Jupyter-Python', onglet 'Networking' : cochez 'Enable a custom service port'. Par défaut, le port est 5000. Attention à bien spécifier le même port dans la commande ci-dessus. 


```
blglbllbg
```

- **Data** : Données d’enquête de StackOverflow sur les développeurs web : https://insights.stackoverflow.com/survey. Nous avons enrichi ces données avec des données à la fois webscrappées et tirées directement d’internet sous forme d’Excel.
- **Notebooks** : Il y a un seul Jupyter notebook `Notebook_Project.ipynb`

## License 
This project is licensed under the MIT License. 

## Contributions

Authors : Pierre CLAYTON, Clément DE LARDEMELLE, Louise LIGONNIERE. 
Contributors : Amina MANSEUR, Lila MEKKI. 


# Create a .env file
You need to create a .env file that contains the paths to the databases stored in a cloud environment (such as the SSPCloud) :
- stack_users_data_path
- countries_lang_data_path
- iso_url