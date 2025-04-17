"""
Ce module génère la distribution des variables principales
"""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from src.data_preprocessing import labels_translation
from src.plot_utils import plot_hist, plot_hist_orders

# Initialisation du logger
logger.add(
    "logs/distribution_variables.log",
    rotation="1 MB",
    retention="10 days",
    level="DEBUG",
)
logger.info("Début de la page Streamlit : Distribution des variables principales")

# Chargement des variables d'environnement
load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)
logger.debug(f"Chemin du fichier StackOverflow récupéré : {stack_users_data_path}")

# Configuration de la page
st.set_page_config(
    page_title="Distribution des variables principales",
    page_icon=":chart_with_upwards_trend:",
)

with st.sidebar:
    st.title("Projet Mise en production pour la data-science")
    st.subheader("Louise LIGONNIERE")
    st.subheader("Amina MANSEUR")
    st.subheader("Lila MEKKI")

st.markdown(
    """
    ## Distribution des variables principales

    On étudie ici la distribution des variables d'intérêt sur les répondants :
    l'âge, le genre, le niveau d'éducation, la branche professionnelle, le nombre d'années de code,
    le nombre d'années de code dans le cadre professionnel, le salaire précédent,
    et les compétences en informatique.

    Vous pouvez utiliser les flèches pour naviguer entre les graphiques.
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

# Génération des graphiques
logger.info("Début de la génération des graphiques")

# 1. Graphe Age
fig_age = plot_hist(stack_users_df_fr, "Age", "Distribution de l'âge")

# 2. Graphe Genre
fig_genre = plot_hist(stack_users_df_fr, "Gender", "Distribution du genre")

# 3. Graphe Niveau d'éducation
fig_ed = plot_hist_orders(
    stack_users_df_fr,
    "EdLevel",
    "Distribution du niveau d'éducation",
    {
        "EdLevel": [
            "Pas d'éducation supérieure",
            "Licence",
            "Master",
            "Doctorat",
            "Autre",
        ]
    },
)

# 4. Graphe Branche pro
fig_branch = plot_hist(
    stack_users_df_fr, "MainBranch", "Distribution de la branche professionnelle"
)

# 5. Graphe Années de code
fig_code = plot_hist(stack_users_df_fr, "YearsCode", "Distribution des années de code")

# 6. Graphe Années de code pro
fig_codepro = plot_hist(
    stack_users_df_fr, "YearsCodePro", "Distribution des années de code professionnel"
)

# 7. Graphe Salaire précédent
fig_salaire = plot_hist(
    stack_users_df_fr, "PreviousSalary", "Distribution du salaire précédent"
)

# 8. Graphe Compétences en informatique
fig_info = plot_hist(
    stack_users_df_fr,
    "ComputerSkills",
    "Distribution des compétences en informatique",
)

logger.success("Tous les graphiques ont été générés avec succès")

# Choix du graphe
tab_age, tab_genre, tab_ed, tab_branch, tab_code, tab_codepro, tab_salaire, tab_info = (
    st.tabs(
        [
            "Age",
            "Genre",
            "Niveau d'éducation",
            "Branche professionnelle",
            "Années de code",
            "Années de code professionnel",
            "Salaire précédent",
            "Compétences en informatique",
        ]
    )
)

with tab_age:
    st.plotly_chart(fig_age)
with tab_genre:
    st.plotly_chart(fig_genre)
with tab_ed:
    st.plotly_chart(fig_ed)
with tab_branch:
    st.plotly_chart(fig_branch)

with tab_code:
    st.plotly_chart(fig_code)
with tab_codepro:
    st.plotly_chart(fig_codepro)
with tab_salaire:
    st.plotly_chart(fig_salaire)
with tab_info:
    st.plotly_chart(fig_info)

st.markdown(
    """
    Les répondants sont majoritairement jeunes (65% ont moins de 35 ans).
    Plus de 93% sont des hommes, ce qui est le défaut principal de notre base.
    Environ 50% des répondants ont un niveau licence, et 25% un master.
    La plus grande partie de la base travaille dans le développement (plus de 91%).

    Le nombre d'années de codage est très dispersé,
    atteignant jusqu'à 50 ans pour les répondants ayant le plus d'ancienneté de codage.
    On remarque toutefois un pic autour de 10 années de codage
    (ce qui est cohérent avec l'âge plutôt jeune des répondants).
    Le nombre d'années de codage dans le cadre professionnel est légèrement moins élevé et moins
    dispersé, avec un pic plutôt autour de 4 ans de codage.

    Le salaire précédent est aussi extrêmement dispersé.

    Enfin, les compétences en informatique, mesurées ici par le nombre de langages maîtrisés,
    semble suivre une gaussienne avec en moyenne une dizaine de langages. On remarque quelques
    valeurs extrêmes de répondants maitrisant plus de 50 langages.
    """
)

logger.info("Fin de l'exécution de la page Distribution des variables principales")
