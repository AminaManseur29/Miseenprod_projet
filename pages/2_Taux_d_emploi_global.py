"""
Ce module génère le graphique représentant le taux d'emploi
"""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from src.data_preprocessing import labels_translation
from src.plot_utils import plot_hist

# Initialisation du logger
logger.add("logs/taux_emploi.log", rotation="1 MB", retention="10 days", level="DEBUG")
logger.info("Début de la page Streamlit : Taux d'emploi")

# Chargement des variables d'environnement
load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)
logger.debug(f"Chemin des données StackOverflow : {stack_users_data_path}")

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Taux d'emploi global", page_icon=":chart_with_upwards_trend:"
)

with st.sidebar:
    st.title("Projet Mise en production pour la data-science")
    st.subheader("Louise LIGONNIERE")
    st.subheader("Amina MANSEUR")
    st.subheader("Lila MEKKI")

st.markdown(
    """
    ## Taux d'emploi global

    """
)

# Chargement des données
try:
    stack_users_df = pd.read_csv(stack_users_data_path, index_col="Unnamed: 0")
    logger.success("Fichier de données chargé avec succès.")
except Exception as e:
    logger.error(f"Erreur lors du chargement des données : {e}")
    st.error("Erreur lors du chargement des données.")
    st.stop()

# Traduction des labels
try:
    stack_users_df_fr = labels_translation(stack_users_df)
    logger.info("Traduction des labels effectuée.")
except Exception as e:
    logger.error(f"Erreur lors de la traduction des labels : {e}")
    st.error("Erreur lors du traitement des données.")
    st.stop()

# Création du graphique
try:
    fig = plot_hist(stack_users_df_fr, "EmployedCat", "Distribution du statut d'emploi")
    logger.info("Graphique du taux d'emploi généré avec succès.")
except Exception as e:
    logger.error(f"Erreur lors de la génération du graphique : {e}")
    st.error("Erreur lors de la génération du graphique.")
    st.stop()

# Affichage du graphique
st.plotly_chart(fig)

st.markdown(
    """
    Le taux d'emploi moyen sur la base est donc de 54%.
    C'est relativement faible. Sur ce point, la base des répondants
    à l'enquête ne semble pas représentative de la réalité du marché du travail.
    Néanmoins, l'avantage pour notre étude est qu'on dispose d'un échantillon de répondants
    non-employés de taille similaire à celui de répondants employés,
    permettant des analyses fiables sur ces deux sous-échantillons.

    """
)

logger.info("Fin de l'exécution de la page Taux d'emploi.")
