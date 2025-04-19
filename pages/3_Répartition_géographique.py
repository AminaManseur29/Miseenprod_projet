"""
Ce module génère la répartition géographique des répondants
"""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from src.data_preprocessing import (
    get_iso_country_codes,
    add_iso_codes,
    add_continent_info,
)
from src.plot_utils import plot_choropleth_map

# ==========================
# Initialisation du logger
# ==========================

logger.add(
    "logs/repartition_geographique.log",
    rotation="1 MB",
    retention="10 days",
    level="DEBUG",
)
logger.info("Début de la page Streamlit : Répartition géographique")

# ==========================
# Chargement des variables d'environnement
# ==========================

load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)
countries_lang_data_path = os.environ.get(
    "countries_lang_data_path", "data/CountryLanguageStats.xls"
)
iso_url = os.environ.get("iso_url", "https://www.iban.com/country-codes")

logger.debug(f"Chemin des données StackOverflow : {stack_users_data_path}")
logger.debug(f"Chemin des données pays/langue : {countries_lang_data_path}")
logger.debug(f"URL des codes ISO : {iso_url}")

# ==========================
# Configuration de la page Streamlit
# ==========================

st.set_page_config(
    page_title="Répartition géographique", page_icon=":chart_with_upwards_trend:"
)

with st.sidebar:
    st.title("Projet Mise en production pour la data-science")
    st.subheader("Louise LIGONNIERE")
    st.subheader("Amina MANSEUR")
    st.subheader("Lila MEKKI")

st.markdown(
    """
    ## Répartition géographique des répondants

    On étudie ici la répartition géographique de deux variables : le nombre de développeurs ayant
    répondu à l'enquête, et le taux d'emploi.

    """
)

# ==========================
# Chargement et prétraitement des données
# ==========================

# Chargement des données
try:
    stack_users_df = pd.read_csv(stack_users_data_path, index_col="Unnamed: 0")
    logger.success("Données StackOverflow chargées avec succès.")
except Exception as e:
    logger.error(f"Erreur lors du chargement des données : {e}")
    st.error("Erreur lors du chargement des données.")
    st.stop()

# Ajout des codes ISO
try:
    iso_df = get_iso_country_codes(iso_url)
    stack_users_df = add_iso_codes(stack_users_df, iso_df)
    logger.info("Ajout des codes ISO réussi.")
except Exception as e:
    logger.error(f"Erreur lors de l'ajout des codes ISO : {e}")
    st.error("Erreur lors de la récupération des codes ISO.")
    st.stop()

# Création du DataFrame pour la carte
try:
    df_carto = (
        stack_users_df.groupby(["Country", "ISO"])["Employed"]
        .agg(["count", "mean"])
        .reset_index()
    )
    df_carto.columns = ["Country", "ISO", "count", "percentage"]
    df_carto["percentage"] *= 100
    logger.info("Tableau de base pour les cartes généré.")
except Exception as e:
    logger.error(f"Erreur lors de l'agrégation des données : {e}")
    st.error("Erreur lors de la préparation des données pour les cartes.")
    st.stop()

# ==========================
# Création des cartes
# ==========================

# 1. Carte du nb de développeurs par pays
fig_nb = plot_choropleth_map(
    df=df_carto,
    location_col="ISO",
    value_col="count",
    hover_col="Country",
    title="Nombre de répondants par pays",
    colorbar_title="Effectif",
)

# 2. Carte du taux d'emploi par pays
fig_taux = plot_choropleth_map(
    df=df_carto,
    location_col="ISO",
    value_col="percentage",
    hover_col="Country",
    filter_col="count",
    min_value=100,
    title="Taux d'emploi par pays (≥ 100 répondants)",
    colorbar_title="Taux d'emploi",
)

# Ajout des infos continentales
try:
    stack_users_df = add_continent_info(stack_users_df, countries_lang_data_path)
    logger.info("Ajout des informations de continent effectué.")
except Exception as e:
    logger.error(f"Erreur lors de l'ajout des continents : {e}")
    st.error("Erreur lors de l'ajout des données continentales.")
    st.stop()

# Agrégation continentale
try:
    df_carto_cont = stack_users_df.groupby(["Continent"])["Employed"].agg(
        ["count", "mean"]
    )
    df_carto_cont = df_carto_cont.sort_values(by="count", ascending=False).reset_index()
    df_carto_cont["mean"] = (df_carto_cont["mean"] * 100).round(2)
    df_carto_cont.columns = ["Continent", "Nombre de répondants", "Taux d'emploi"]
    logger.info("Tableau des continents généré.")
except Exception as e:
    logger.error(f"Erreur lors de l'agrégation continentale : {e}")
    st.error("Erreur lors de la préparation des données par continent.")
    st.stop()

# Choix du graphe
tab_nb, tab_taux, tab_cont = st.tabs(
    [
        "Nombre de répondants par pays",
        "Taux d'emploi par pays",
        "Nombre de répondants et taux d'emploi par continent",
    ]
)

# ==========================
# Affichage des cartes
# ==========================

with tab_nb:
    st.plotly_chart(fig_nb)
with tab_taux:
    st.plotly_chart(fig_taux)
with tab_cont:
    st.dataframe(df_carto_cont)


# ==========================
# Création et affichage des commentaires automatisés des cartes
# ==========================

# Calcul du pourcentage de répondants par continent
total_repondants = df_carto_cont["Nombre de répondants"].sum()
df_carto_cont["Part en %"] = (
    100 * df_carto_cont["Nombre de répondants"] / total_repondants
).round(1)

top_continents = df_carto_cont[df_carto_cont["Part en %"] > 10]
low_continents = df_carto_cont[df_carto_cont["Part en %"] < 5]

COMMENTAIRE = """- 🌍 **Répartition des répondants par continent** :"""

# Continents bien représentés
for _, row in top_continents.iterrows():
    COMMENTAIRE += (
        f"\n  - {row['Continent']} : {row['Part en %']}% des répondants",
        f"(Taux d'emploi : {row['Taux d\'emploi']}%)"
    )

# Continents sous-représentés
if not low_continents.empty:
    COMMENTAIRE += (
        "\n\n- ⚠️ **Sous-représentation** observée dans : "
        + ", ".join(low_continents["Continent"])
        + ". Cela peut limiter les analyses régionales dans ces zones."
    )

# Commentaire sur le taux d’emploi global
mean_employment_rate = df_carto_cont["Taux d'emploi"].mean().round(1)
if mean_employment_rate < 60:
    COMMENTAIRE += f"""

- 📉 **Taux d'emploi moyen** : {mean_employment_rate}% sur l'ensemble des continents.
Cela reflète un accès à l'emploi modéré parmi les répondants.
"""
else:
    COMMENTAIRE += f"""

- 📈 **Taux d'emploi moyen** : {mean_employment_rate}% sur l'ensemble des continents.
Cela montre une population majoritairement en emploi, avec toutefois des disparités régionales.
"""

# Affichage dans Streamlit
st.markdown("### Synthèse automatisée")
st.markdown(COMMENTAIRE)

logger.info("Fin de l'exécution de la page Répartition géographique.")
