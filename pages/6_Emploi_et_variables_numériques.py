"""Ce module génère la page de rapport sur les emplois et variables numériques."""


import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from src.data_preprocessing import (
    compute_top_languages_count,
    categorize_employment_status,
)
from src.plot_utils import plot_box, make_wordcloud

# Initialisation du logger
logger.add(
    "logs/emplois_vars_num.log",
    rotation="1 MB",
    retention="10 days",
    level="DEBUG",
)
logger.info("Début de la page Streamlit : Emplois et variables numériques")

# Chargement des variables d'environnement
load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)
logger.debug(f"Chemin du fichier StackOverflow récupéré : {stack_users_data_path}")

# Configuration de la page
st.set_page_config(
    page_title="Emploi et variables numériques", page_icon=":chart_with_upwards_trend:"
)

with st.sidebar:
    st.title("Projet Mise en production pour la data-science")
    st.subheader("Louise LIGONNIERE")
    st.subheader("Amina MANSEUR")
    st.subheader("Lila MEKKI")

st.markdown(
    """
    ## Emploi et variables numériques

    On étudie ici la distribution des quatre 
    principales variables numériques selon le statut d'emploi.
    """
)

# Chargement des données depuis le répertoire sspcloud
try:
    stack_users_df = pd.read_csv(stack_users_data_path, index_col="Unnamed: 0")
    stack_users_df = categorize_employment_status(
        stack_users_df
    )  # pour binariser les colonnes d'emploi
    logger.success(f"Fichier chargé avec succès : {stack_users_data_path}")
except Exception as e:
    logger.error(f"Erreur lors du chargement du fichier : {e}")
    st.error(
        "Impossible de charger les données. Veuillez vérifier le chemin ou le format du fichier."
    )
    st.stop()

# Dataframe réduit des 10 langages les plus maîtrisés parmi les 20 plus utilisés
try:
    fig_lang_cloud, lang_count = make_wordcloud(stack_users_df, "HaveWorkedWith")
    count_lang20 = lang_count.most_common(20)
    top_languages = count_lang20.most_common(10)
    top_languages = pd.DataFrame(
        top_languages, columns=["Langage", "Nombre d'occurences"], index=range(1, 11)
    )
    top_lang_alter = compute_top_languages_count(
        stack_users_df, "HaveWorkedWith", top_languages
    )
    logger.info(
        "Dataframe des 10 langages mieux maîtrisés parmi les 20 plus fréquents calculé avec succès"
    )
except Exception as e:
    logger.error(f"Erreur lors de la création du Dataframe : {e}")
    st.error("Erreur lors du traitement des données.")
    st.stop()


# Génération des graphiques
logger.info("Début de la génération des box plots")

# 1. Années de code vs. statut d'emploi
fig_code = plot_box(
    data=stack_users_df,
    x_col="EmployedCat",
    y_col="YearsCode",
    color_col="EmployedCat",
    title="Distribution des années de code selon le statut d'emploi",
    xaxis_title="Statut d'emploi",
    yaxis_title_text="Années de code",
)

# 2. Années de code pro vs. statut d'emploi
fig_codepro = plot_box(
    data=stack_users_df,
    x_col="EmployedCat",
    y_col="YearsCodePro",
    color_col="EmployedCat",
    title="Distribution des années de code professionnel selon le statut d'emploi",
    xaxis_title="Statut d'emploi",
    yaxis_title_text="Années de code professionnel",
)

# 3. Salaire précédent vs. statut d'emploi
fig_salaire = plot_box(
    data=stack_users_df,
    x_col="EmployedCat",
    y_col="PreviousSalary",
    color_col="EmployedCat",
    title="Distribution du salaire précédent selon le statut d'emploi",
    xaxis_title="Statut d'emploi",
    yaxis_title="Salaire précédent",
)

# 4. Compétences en informatique vs. statut d'emploi
fig_comp_info = plot_box(
    data=stack_users_df,
    x_col="EmployedCat",
    y_col="ComputerSkills",
    color_col="EmployedCat",
    title=(
        "Distribution des compétences en informatique "
        "(nombre de langages maîtrisés) selon le statut d'emploi"
    ),
    xaxis_title="Statut d'emploi",
    yaxis_title="Nombre de langages maîtrisés",
)

# 5. Compétences en informatique - mesure alternative vs. statut d'emploi
fig_comp_info_alter = plot_box(
    data=top_lang_alter,
    x_col="EmployedCat",
    y_col="TopLanguagesCount",
    color_col="EmployedCat",
    title=(
        "Distribution des compétences en informatique"
        "(mesure alternative) selon le statut d'emploi"
    ),
    xaxis_title="Statut d'emploi",
    yaxis_title="Nombre de langages maîtrisés parmi les 10 langages les plus présents",
)

# Choix du graphe
tab_code, tab_codepro, tab_salaire, tab_info, tab_info2 = st.tabs(
    [
        "Années de code",
        "Années de code professionnel",
        "Salaire précédent",
        "Compétences en informatique",
        "Compétences en informatique - mesure alternative",
    ]
)

with tab_code:
    st.plotly_chart(fig_code)
with tab_codepro:
    st.plotly_chart(fig_codepro)
with tab_salaire:
    st.plotly_chart(fig_salaire)
with tab_info:
    st.plotly_chart(fig_comp_info)
with tab_info2:
    st.plotly_chart(fig_comp_info_alter)

st.markdown(
    """
    Le nombre d'années de codage, dans le cadre professionnel ou non, 
    et le salaire précédent semblent peu varier selon le statut d'emploi. 
    Ces variables semblent donc peu pertinentes pour expliquer 
    l'employabilité des répondants.
    A l'inverse, les compétences en informatique 
    (qu'elles soient mesurées par le nombre total de langages 
    maîtrisés ou parmi les 10 langages les plus fréquents) semblent 
    plus importantes chez les répondants en emploi. Ainsi, les 3 quarts
    des répondants sans emploi maîtrisent moins de 12 langages, alors que 
    les 3 quarts des répondants en emploi maîtrisent plus de 13 langages. 
    Ce résultat est néanmoins à relier avec la branche professionnelle 
    principale : ainsi, les répondants ne travaillant pas dans le développement,
    même s'ils sont peu dans la base, maîtrisent moins de langages, et sont 
    aussi significativement moins employés.
    """
)

logger.info("Fin de l'exécution de la page Emplois et variables numériques")
