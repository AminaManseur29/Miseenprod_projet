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

# ==========================
# Initialisation du logger
# ==========================

logger.add("logs/taux_emploi.log", rotation="1 MB", retention="10 days", level="DEBUG")
logger.info("Début de la page Streamlit : Taux d'emploi")

# ==========================
# Chargement des variables d'environnement
# ==========================

load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)
logger.debug(f"Chemin des données StackOverflow : {stack_users_data_path}")

# ==========================
# Configuration de la page Streamlit
# ==========================

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

# ==========================
# Chargement et prétraitement des données
# ==========================

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


# ==========================
# Génération du graphique
# ==========================

try:
    fig = plot_hist(stack_users_df_fr, "EmployedCat", "Distribution du statut d'emploi")
    logger.info("Graphique du taux d'emploi généré avec succès.")
except Exception as e:
    logger.error(f"Erreur lors de la génération du graphique : {e}")
    st.error("Erreur lors de la génération du graphique.")
    st.stop()

# ==========================
# Affichage du graphique
# ==========================

st.plotly_chart(fig)

# ==========================
# Création et affichage des commentaires automatisés du graphique
# ==========================

# Calcul du taux d'emploi
emploi_counts = stack_users_df_fr["EmployedCat"].value_counts(normalize=True)
pct_employed = round(100 * emploi_counts.get("En emploi", 0), 1)

# Génération du commentaire
if pct_employed < 70:
    COMMENTAIRE = f"""
- 🧑‍💼 Le taux d'emploi moyen sur la base est de **{pct_employed}%**.
C'est relativement faible. Cela suggère que la base des répondants
n’est pas entièrement représentative de la réalité du marché du travail,
où le taux d'emploi est généralement plus élevé.

- Néanmoins, ce déséquilibre relatif est **avantageux pour l’entraînement de nos modèles** :
on dispose d’un échantillon significatif de répondants non-employés,
ce qui permet d'entraîner des modèles robustes sur les deux catégories (employés / non-employés).
"""
else:
    COMMENTAIRE = f"""
- 🧑‍💼 Le taux d'emploi moyen sur la base est de **{pct_employed}%**.
C'est un taux relativement élevé, ce qui reflète une base de répondants
globalement bien intégrés dans le marché du travail.

- Cela peut néanmoins induire un **déséquilibre** dans les classes pour nos modèles,
avec une sous-représentation des répondants non-employés.
Des techniques d’équilibrage (par exemple, sur-échantillonnage ou pondération)
pourront être envisagées pour garantir des performances fiables.
"""

# Affichage dans Streamlit
st.markdown("### Synthèse automatisée")
st.markdown(COMMENTAIRE)

logger.info("Fin de l'exécution de la page Taux d'emploi.")
