"""
Ce module génère le taux d'emploi
"""

import streamlit as st
import pandas as pd

from src.data_preprocessing import labels_translation
from src.plot_utils import plot_hist

st.set_page_config(
    page_title="Taux d'emploi global", page_icon=":chart_with_upwards_trend:"
)

with st.sidebar:
    st.title("Projet Python pour la Data Science")
    st.subheader("Pierre CLAYTON")
    st.subheader("Clément DE LARDEMELLE")
    st.subheader("Louise LIGONNIERE")

st.markdown(
    """
    ## Taux d'emploi global

    """
)

# Chargement des données
stack_users_data = pd.read_csv("stackoverflow_full.csv", index_col="Unnamed: 0")

# Recodage des variables catégorielles (ENG -> FR)
stack_users_data_fr = labels_translation(stack_users_data)

# Graphe Emploi
fig = plot_hist(stack_users_data_fr, "EmployedCat", "Distribution du statut d'emploi")

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
