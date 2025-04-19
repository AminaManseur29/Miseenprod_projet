"""Ce module génère la page de rapport sur les langages utilisés."""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from src.plot_utils import plot_hist, make_wordcloud, plot_bar
from src.data_preprocessing import compute_top_languages_count

# ==========================
# Initialisation du logger
# ==========================

logger.add(
    "logs/langages_utilises.log",
    rotation="1 MB",
    retention="10 days",
    level="DEBUG",
)
logger.info("Début de la page Streamlit : Langages utilisés")

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
    page_title="Langages utilisés", page_icon=":chart_with_upwards_trend:"
)

with st.sidebar:
    st.title("Projet Mise en production pour la data-science")
    st.subheader("Louise LIGONNIERE")
    st.subheader("Amina MANSEUR")
    st.subheader("Lila MEKKI")

st.markdown(
    """
    ## Langages utilisés par les répondants

    Les langages les plus employés par les répondants sont les suivants : 

    """
)

# ==========================
# Chargement et prétraitemet des données
# ==========================

try:
    stack_users_df = pd.read_csv(stack_users_data_path, index_col="Unnamed: 0")
    logger.success(f"Fichier chargé avec succès : {stack_users_data_path}")
except Exception as e:
    logger.error(f"Erreur lors du chargement du fichier : {e}")
    st.error(
        "Impossible de charger les données. Veuillez vérifier le chemin ou le format du fichier."
    )
    st.stop()


# ==========================
# Analyse des langages utilisés
# ==========================

# Génération nuage de mots pour vue globale
fig_lang_cloud, lang_count = make_wordcloud(stack_users_df, "HaveWorkedWith")
st.markdown(
    """☁️ **Nuage de mots** : vue d'ensemble des langages mentionnés par les répondants."""
)
st.pyplot(fig_lang_cloud)

# Dataframe réduit des 20 langages les plus utilisés
try:
    top_languages20 = pd.DataFrame(
        lang_count.most_common(20), columns=["Langage", "Count"], index=range(1, 21)
    )
    logger.info("Dataframe des 20 langages les plus utilisés calculé avec succès")

except Exception as e:
    logger.error(f"Erreur lors de la création du Dataframe : {e}")
    st.error("Erreur lors du traitement des données.")
    st.stop()

# Dataframe réduit des 10 langages les plus maîtrisés parmi les 20 plus utilisés
try:
    top_languages = pd.DataFrame(
        lang_count.most_common(10),
        columns=["Langage", "Nombre d'occurences"],
        index=range(1, 11),
    )
    top_lang_alter = compute_top_languages_count(
        stack_users_df, "HaveWorkedWith", top_languages["Langage"].tolist()
    )
    logger.info(
        "Dataframe des 10 langages mieux maîtrisés parmi les 20 plus fréquents calculé avec succès"
    )

except Exception as e:
    logger.error(f"Erreur lors de la création du Dataframe : {e}")
    st.error("Erreur lors du traitement des données.")
    st.stop()

# ==========================
# Génération des graphiques
# ==========================

logger.info("Début de la génération des graphiques")

# 1. Graphe Langages les plus employés
fig_lang = plot_bar(top_languages20, "Langage", "Les 20 langages les plus employés")
st.plotly_chart(fig_lang)

# Statistiques descriptives sur les plus fréquents
most_used_langs = top_languages20.head(4)
max_usage = most_used_langs.iloc[0]["Count"] / stack_users_df.shape[0] * 100
st.markdown(
    f"""- 🔝 **Top 20 langages** : {', '.join(most_used_langs['Langage'])}
    sont les plus cités. Le plus populaire ({most_used_langs.iloc[0]['Langage']}) est utilisé
    par environ {max_usage:.1f}% des répondants."""
)

# Mesure alternative des compétences en informatique
st.markdown(
    """
    ### Une mesure alternative des compétences en informatique

    Jusqu'ici, les compétences en informatique étaient mesurées via la variable `ComputerSkills`
    qui comptait le nombre de langages maîtrisés par chaque développeur. Ici, on crée une mesure
    alternative des compétences en informatique grâce à un décompte des langages maîtrisés parmi
    les 10 langages les plus courants dans la base.

    On obtient la distribution suivante :
    """
)

# 2. Graphe Langages les plus employés parmi les top 10 langages
fig_lang_alter = plot_hist(
    top_lang_alter,
    "TopLanguagesCount",
    "Distribution des compétences en informatique - mesure alternative",
    xaxis_title="Nombre de langages maîtrisés parmi les 10 les plus présents",
)
st.plotly_chart(fig_lang_alter)

# Statistiques
competence_mean = top_lang_alter["TopLanguagesCount"].mean()
competence_pct = (top_lang_alter["TopLanguagesCount"] >= 1).mean() * 100
st.markdown(
    f"""- 🧠 **Compétence informatique (alternative)** : en moyenne, les répondants
    maîtrisent {competence_mean:.1f} langages parmi les 10 principaux. {competence_pct:.1f}% en
    connaissent au moins un."""
)

# ==========================
# Conclusion automatisée
# ==========================

conclusion = f"""
Les langages de programmation sont très concentrés.
{most_used_langs.iloc[0]['Langage']} domine avec un usage par environ {max_usage:.1f}%
des répondants. Presque {competence_pct:.1f}% des participants maîtrisent au moins un des
10 langages principaux, avec une moyenne de {competence_mean:.1f} langages par répondant.
"""
st.markdown("**Conclusion automatisée**")
st.markdown(conclusion)
logger.info("Fin de l'exécution de la page Langages utilisés")
