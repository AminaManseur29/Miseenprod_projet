"""Ce module génère la page de rapport sur les langages utilisés."""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from loguru import logger

from src.plot_utils import plot_hist, make_wordcloud, plot_bar
from src.data_preprocessing import compute_top_languages_count

# Initialisation du logger
logger.add(
    "logs/langages_utilises.log",
    rotation="1 MB",
    retention="10 days",
    level="DEBUG",
)
logger.info("Début de la page Streamlit : Langages utilisés")

# Chargement des variables d'environnement
load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)
logger.debug(f"Chemin du fichier StackOverflow récupéré : {stack_users_data_path}")

# Configuration de la page
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

# Chargement des données depuis le répertoire ssp cloud
try:
    stack_users_df = pd.read_csv(stack_users_data_path, index_col="Unnamed: 0")
    logger.success(f"Fichier chargé avec succès : {stack_users_data_path}")
except Exception as e:
    logger.error(f"Erreur lors du chargement du fichier : {e}")
    st.error(
        "Impossible de charger les données. Veuillez vérifier le chemin ou le format du fichier."
    )
    st.stop()

# Génération nuage de mots pour vue globale
fig_lang_cloud, lang_count = make_wordcloud(stack_users_df, "HaveWorkedWith")
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
        lang_count.most_common(10), columns=["Langage", "Nombre d'occurences"], index=range(1, 11)
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
logger.info("Début de la génération des graphiques")

# 1. Graphe Langages les plus employés
fig_lang = plot_bar(top_languages20, "Langage", "Les 20 langages les plus employés")
st.plotly_chart(fig_lang)

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


# Conclusion finale
st.markdown(
    """
    Les langages utilisés sont donc très concentrés. Les 4 premiers langages 
    (JavaScript, Docker, HTML/CSS et SQL) sont tous utilisés par plus de 50% des répondants,
    et jusqu'à 67% pour JavaScript.

    Lorsque l'on compte le nombre de langages maîtrisés parmi les 10 langages les plus cités
    dans la base, on trouve des résultats cohérents. Ainsi, presque l'intégralité (98%) 
    des répondants maîtrisent au moins 1 de ces 10 langages. En moyenne, les répondants 
    en maîtrisent 5. 
    """
)

logger.info("Fin de l'exécution de la page Langages utilisés")