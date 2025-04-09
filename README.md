# README

# Objectif du Projet
Le projet vise à mettre en place un modèle de sélection de candidats pour les départements de Ressources Humaines des entreprises. Ce modèle vise à intégrer les nouvelles nécessités ESG, et en particulier les considérations éthiques sur le genre. 

# Structure du Projet
- **Data** : Données d’enquête de StackOverflow sur les développeurs web : https://insights.stackoverflow.com/survey. Nous avons enrichi ces données avec des données à la fois webscrappées et tirées directement d’internet sous forme d’Excel.
- **Notebooks** : Il y a un seul Jupyter notebook `Notebook_Project.ipynb`

# Comment Utiliser
Toutes les analyses sont présentées dans le notebook. 

Par ailleurs, une application développée via Streamlit présente la distribution des variables d'intérêt et facilite la navigation entre les différents graphiques. Elle présente aussi de façon interactive les modèles réalisés. 

**Nous vous invitons à consulter cette application** (le contenu de ses pages est toutefois reporté dans les sections 4 à 6 du notebook).

*Étapes pour lancer l'application* : 
- il est nécessaire de commencer par exécuter l'intégralité du notebook (sinon, la page présentant les modèles ne charge pas entièrement),
- ouvrir un terminal,
- se placer dans le dossier 'Projet-Python-ENSAE' (qui contient le script de lancement de l'application 'Accueil.py' et le dossier 'pages' contenant les scripts des pages),
- exécuter la commande suivante : streamlit run Accueil.py --server.port 5000 --server.address 0.0.0.0

**Attention** : si vous consultez le Notebook dans un environnement Jupyter via le SSP Cloud, il est nécessaire d'avoir ouvert au préalable un *custom service port* au lancement du service Jupyter. Vous pouvez le faire dans la 'Configuration Jupyter-Python', onglet 'Networking' : cochez 'Enable a custom service port'. Par défaut, le port est 5000. Attention à bien spécifier le même port dans la commande ci-dessus. 

# Contributions et Remerciements
Le projet a été réalisé par le groupe de 3 suivant : Pierre CLAYTON, Clément DE LARDEMELLE, Louise LIGONNIERE.


# Créer un fichier .env
Créer un fichier .env qui contient les chemins vers les bases de données stockées dans un environnement cloud (comme le SSPCloud):
- stack_users_data_path
- countries_lang_data_path
- iso_url