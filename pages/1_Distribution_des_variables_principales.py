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

# ==========================
# Initialisation du logger
# ==========================

logger.add(
    "logs/distribution_variables.log",
    rotation="1 MB",
    retention="10 days",
    level="DEBUG",
)
logger.info("Début de la page Streamlit : Distribution des variables principales")

# ==========================
# Chargement des variables d'environnement
# ==========================

load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)
logger.debug(f"Chemin du fichier StackOverflow récupéré : {stack_users_data_path}")

# ==========================
# Configuration de la page Streamlit
# ==========================

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

    Vous pouvez naviguer entre les graphiques via les différents onglets.
    """
)

# ==========================
# Chargement et prétraitement des données
# ==========================

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

# ==========================
# Génération des graphiques
# ==========================

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

# ==========================
# Affichage des graphiques
# ==========================

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


# ==========================
# Création et affichage des commentaires automatisés des graphiques
# ==========================

# Initialisation des commentaires
COMMENTAIRE = ""

# 1. Âge
age_counts = stack_users_df_fr["Age"].value_counts(normalize=True)
if "Moins de 35 ans" in age_counts:
    pct_jeunes = round(100 * age_counts["Moins de 35 ans"], 1)
    COMMENTAIRE += f"- 👶 **{pct_jeunes}%** des répondants ont moins de 35 ans.\n"
if "Plus de 35 ans" in age_counts:
    pct_plus_35 = round(100 * age_counts["Plus de 35 ans"], 1)
    COMMENTAIRE += f"- 👴 **{pct_plus_35}%** des répondants ont 35 ans ou plus.\n"

# 2. Genre
genre_counts = stack_users_df_fr["Gender"].value_counts(normalize=True)
if "Homme" in genre_counts:
    pct_hommes = round(100 * genre_counts["Homme"], 1)
    COMMENTAIRE += (
        f"- 👨‍💻 Les hommes représentent environ **{pct_hommes}%** des répondants.\n"
    )
if "Femme" in genre_counts:
    pct_femmes = round(100 * genre_counts["Femme"], 1)
    COMMENTAIRE += (
        f"- 👩‍💻 Les femmes représentent environ **{pct_femmes}%** des répondants.\n"
    )
if "Autre" in genre_counts:
    pct_autre = round(100 * genre_counts["Autre"], 1)
    COMMENTAIRE += f"- 🚻 **{pct_autre}%** des répondants se considèrent dans une autre catégorie.\n"

# 3. Niveau d'éducation
ed_counts = stack_users_df_fr["EdLevel"].value_counts(normalize=True)
licence_pct = round(100 * ed_counts.get("Licence", 0), 1)
master_pct = round(100 * ed_counts.get("Master", 0), 1)
doctorat_pct = round(100 * ed_counts.get("Doctorat", 0), 1)
COMMENTAIRE += (
    f"- 🎓 Environ **{licence_pct}%** ont une licence, "
    f"**{master_pct}%** un master et **{doctorat_pct}%** un doctorat.\n"
)

# 4. Branche professionnelle
branch_counts = stack_users_df_fr["MainBranch"].value_counts(normalize=True)
dev_pct = round(100 * branch_counts.iloc[0], 1)
branche_dev = branch_counts.index[0]
COMMENTAIRE += (
    f"- 🧑‍💼 **{branche_dev}** est la branche la plus représentée (**{dev_pct}%**).\n"
)

# 5. Langages (Compétences en informatique)
skills_series = pd.to_numeric(stack_users_df_fr["ComputerSkills"], errors="coerce")
skill_mean = round(skills_series.mean(), 1)
COMMENTAIRE += (
    f"- 💡 Les répondants connaissent en moyenne **{skill_mean} langages** informatiques.\n"
)

# 6. Années de code
years_code_series = pd.to_numeric(stack_users_df_fr["YearsCode"], errors="coerce")
years_code_mean = round(years_code_series.mean(), 1)
COMMENTAIRE += (
    f"- 💻 Les répondants ont en moyenne **{years_code_mean} années de code**.\n"
)

# 7. Années de code professionnel
years_codepro_series = pd.to_numeric(stack_users_df_fr["YearsCodePro"], errors="coerce")
years_codepro_mean = round(years_codepro_series.mean(), 1)
COMMENTAIRE += (
    f"- 💼 Les répondants ont en moyenne **{years_codepro_mean} années "
    f"d'expérience professionnelle**.\n"
)

# 8. Salaire précédent
salary_series = pd.to_numeric(stack_users_df_fr["PreviousSalary"], errors="coerce")
salary_mean = round(salary_series.mean(), 1)
COMMENTAIRE += (
    f"- 💸 Le salaire précédent moyen des répondants est de **{salary_mean}**$.\n"
)

# 🔽 Affichage
st.markdown("### Synthèse automatisée")
st.markdown(COMMENTAIRE)

logger.info("Fin de l'exécution de la page Distribution des variables principales")
