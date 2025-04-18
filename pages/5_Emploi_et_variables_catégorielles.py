"""Ce module génère la page de rapport sur les emplois et variables catégorielles."""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from src.plot_utils import (
    plot_bar_orders,
)
from src.data_preprocessing import group_percentage_by, labels_translation


# Initialisation du logger
logger.add(
    "logs/emplois_vars_cat.log",
    rotation="1 MB",
    retention="10 days",
    level="DEBUG",
)
logger.info("Début de la page Streamlit : Emplois et variables catégorielles")


# Chargement des variables d'environnement
load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)
logger.debug(f"Chemin du fichier StackOverflow récupéré : {stack_users_data_path}")

# Configuration de la page
st.set_page_config(
    page_title="Emploi et variables catégorielles",
    page_icon=":chart_with_upwards_trend:",
)

with st.sidebar:
    st.title("Projet Mise en production pour la data-science")
    st.subheader("Louise LIGONNIERE")
    st.subheader("Amina MANSEUR")
    st.subheader("Lila MEKKI")

st.markdown(
    """
    ## Emploi et variables catégorielles

    On étudie ici la distribution des quatre principales variables catégorielles :
    l'âge, le genre, le niveau d'éducation et la branche professionnelle principale,
    selon le statut d'emploi.
    """
)

# Chargement des données depuis le répertoire sspcloud
try:
    stack_users_df = pd.read_csv(stack_users_data_path, index_col="Unnamed: 0")
    logger.success(f"Fichier chargé avec succès : {stack_users_data_path}")
except Exception as e:
    logger.error(f"Erreur lors du chargement du fichier : {e}")
    st.error(
        "Impossible de charger les données. Veuillez vérifier le chemin ou le format du fichier."
    )
    st.stop()

# Traduction des labels
try:
    stack_users_df_fr = labels_translation(stack_users_df)
    logger.info("Traduction des labels effectuée avec succès")
except Exception as e:
    logger.error(f"Erreur lors de la traduction des labels : {e}")
    st.error("Erreur lors du traitement des données.")
    st.stop()


# Calcul des pourcentages pour les différentes colonnes
try:
    age_df = group_percentage_by(stack_users_df_fr, ["Age", "EmployedCat"])
    gender_df = group_percentage_by(stack_users_df_fr, ["Gender", "EmployedCat"])
    edLevel_df = group_percentage_by(stack_users_df_fr, ["EdLevel", "EmployedCat"])
    workbranch_df = group_percentage_by(
        stack_users_df_fr, ["MainBranch", "EmployedCat"]
    )
    logger.info("Génération des données agrégées effectuée avec succès")
except Exception as e:
    logger.error(f"Erreur lors de l'agrégation' : {e}")
    st.error("Erreur lors du traitement des données.")
    st.stop()

# Génération des graphiques
logger.info("Début de la génération des graphiques")

# 1. Graphe Age
fig_age = plot_bar_orders(
    age_df,
    "Age",
    "EmployedCat",
    "Distribution du statut d'emploi selon l'âge",
    {"Age": ["Moins de 35 ans", "Plus de 35 ans"]},
    x_col="percentage",
)

# 2. Graphe Genre
fig_gender = plot_bar_orders(
    gender_df,
    "Gender",
    "EmployedCat",
    "Distribution du statut d'emploi selon le genre",
    {"Gender": ["Homme", "Femme", "Non-Binaire"]},
    x_col="percentage",
)


# 3. Graphe Niveau d'éducation
fig_edLevel = plot_bar_orders(
    edLevel_df,
    "EdLevel",
    "EmployedCat",
    "Distribution du statut d'emploi selon le niveau d'éducation",
    category_orders={
        "EdLevel": [
            "Pas d'éducation supérieure",
            "Licence",
            "Master",
            "Doctorat",
            "Autre",
        ]
    },
    x_col="percentage",
)


# 4. Graphe Branche pro
fig_workbranch = plot_bar_orders(
    workbranch_df,
    "MainBranch",
    "EmployedCat",
    "Distribution du statut d'emploi selon la branche professionnelle",
    {"MainBranch": ["Développement", "Autre"]},
    x_col="percentage",
)


# Choix du graphe
tab_age, tab_genre, tab_ed, tab_branch = st.tabs(
    ["Age", "Genre", "Niveau d'éducation", "Branche professionnelle"]
)

with tab_age:
    st.plotly_chart(fig_age)
with tab_genre:
    st.plotly_chart(fig_gender)
with tab_ed:
    st.plotly_chart(fig_edLevel)
with tab_branch:
    st.plotly_chart(fig_workbranch)

st.markdown(
    """
    **Pour rappel, le taux d'emploi moyen sur l'ensemble de la 
    base est de 54%.**

    Les moins de 35 ans semblent donc légèrement plus employés 
    que les plus de 35%. Les femmes sont beaucoup moins employées, 
    avec près de 10 points d'écart. Le taux d'emploi des personnes
    non-binaires est plus élevé, mais l'échantillon est très faible. 
    
    Le niveau d'éducation semble aussi beaucoup jouer dans l'emploi,
    avec un taux d'emploi plus élevé pour les répondants ayant un niveau
    licence ou inférieur. A l'inverse, il est très faible pour les 
    titulaires d'un doctorat (29%). 

    Enfin, les répondants travaillant dans le développement 
    sont plus employées ici (mais elles constituent 
    l'essentiel de la base).

    La principale source de biais injustifié que l'on relève
    dans cette analyse est donc le genre. C'est la variable sur 
    laquelle on se concentre dans la suite de la modélisation. 
    On vérifiera notamment si le biais qui semble se dessiner
    ici est bien significatif, et s'il n'est pas simplement 
    dû à une corrélation du genre avec d'autres variables qui 
    peuvent expliquer l'employabilité (par exemple, 
    le niveau d'éducation).
    """
)

logger.info("Fin de l'exécution de la page Emplois et variables catégorielles")
