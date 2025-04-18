"""
Ce module génère la page Modélisation de l'emploi de l'application de visualisation Streamlit.
"""

import streamlit as st
from src.models_visualisation_utils import (
    get_data_log_regression,
    get_model_performance,
)

# ==========================
# User interface
# ==========================

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

list_col = tab_logistic_regression.multiselect(
    "Sélectionner les variables explicatives pour la régression de la variable 'Employed' : ",
    VAR_NUM + VAR_CAT,
    default=VAR_NUM[1:] + VAR_CAT,
)
result_df, score, X, delta_prob = get_data_log_regression(parameters=list_col)
tab_logistic_regression.subheader(f"Le R2 du modèle est : {round(score * 100, 2)}%")
tab_logistic_regression.table(result_df)

# ==========================
# Models performance
# ==========================

tab_models_performance.subheader("Random Forest performance")
result_df_exp2 = get_model_performance("Random Forest")
tab_models_performance.table(result_df_exp2)

tab_models_performance.subheader("Logistic Regression performance")
result_df_exp3 = get_model_performance("Logistic Regression")
tab_models_performance.table(result_df_exp3)

tab_models_performance.subheader("Gradient Boosting performance")
result_df_exp4 = get_model_performance("Gradient Boosting")
tab_models_performance.table(result_df_exp4)
