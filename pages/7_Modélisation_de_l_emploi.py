"""
Ce module génère la page Modélisation de l'emploi de l'application de visualisation Streamlit.
"""

import streamlit as st
from loguru import logger
from src.models_visualisation_utils import (
    get_data_log_regression,
    get_model_performance,
)

# Initialisation du logger
logger.add(
    "logs/modelisation_emploi.log",
    rotation="1 MB",
    retention="10 days",
    level="DEBUG",
)
logger.info("Début de la page Streamlit : Modélisation de l'emploi")

# Configuration de la page
st.set_page_config(
    page_title="Modélisation de l'emploi",
    page_icon=":chart_with_upwards_trend:",
)

with st.sidebar:
    st.title("Projet Mise en production pour la data-science")
    st.subheader("Louise LIGONNIERE")
    st.subheader("Amina MANSEUR")
    st.subheader("Lila MEKKI")

st.markdown(
    """
    ## Modélisation de l'emploi
    """
)

(tab_logistic_regression, tab_models_performance) = st.tabs(
    ["Régression logistique", "Performance des modèles"]
)

# ==========================
# Logistic Regression
# ==========================

VAR_NUM = ["PreviousSalary", "YearsCode", "YearsCodePro", "ComputerSkills"]
VAR_CAT = ["Age", "EdLevel", "Gender", "MentalHealth", "MainBranch"]

# Log de la sélection des variables
logger.info("Demande de sélection des variables pour la régression logistique.")
list_col = tab_logistic_regression.multiselect(
    "Sélectionner les variables explicatives pour la régression de la variable 'Employed' : ",
    VAR_NUM + VAR_CAT,
    default=VAR_NUM[1:] + VAR_CAT,
)

# Log des paramètres sélectionnés
logger.debug(f"Variables sélectionnées : {list_col}")

# Obtenir les données et les résultats de la régression logistique
result_df, score, X, delta_prob = get_data_log_regression(parameters=list_col)

# Log de la performance du modèle
logger.info(f"Modèle de régression logistique : R2 = {round(score * 100, 2)}%")

tab_logistic_regression.subheader(f"Le R2 du modèle est : {round(score * 100, 2)}%")
tab_logistic_regression.table(result_df)

# ==========================
# Models performance
# ==========================

tab_models_performance.subheader("Random Forest performance")
result_df_exp2 = get_model_performance("Random Forest")
logger.info("Affichage des résultats de performance pour le modèle Random Forest.")
tab_models_performance.table(result_df_exp2)

tab_models_performance.subheader("Logistic Regression performance")
result_df_exp3 = get_model_performance("Logistic Regression")
logger.info("Affichage des résultats de performance pour le modèle Logistic Regression.")
tab_models_performance.table(result_df_exp3)

tab_models_performance.subheader("Gradient Boosting performance")
result_df_exp4 = get_model_performance("Gradient Boosting")
logger.info("Affichage des résultats de performance pour le modèle Gradient Boosting.")
tab_models_performance.table(result_df_exp4)

logger.info("Fin de l'exécution de la page Modélisation de l'emploi")
