"""
Ce module génère la page Modèles de l'application de visualisation Streamlit.
"""

import dalex as dx
import pandas as pd
import streamlit as st
import joblib
from src.models_visualisation_utils import get_data_linear_regression, get_data_log_regression
from src.models_visualisation_utils import get_fairness_test, get_fairness_check, get_fairness_check_after_mitigation

# ==========================
# User interface
# ==========================

with st.sidebar:
    st.title("Projet Python pour la Data Science")
    st.subheader("Pierre CLAYTON")
    st.subheader("Clément DE LARDEMELLE")
    st.subheader("Louise LIGONNIERE")

(
    tab_linear_regression,
    tab_logistic_regression,
    tab_fairness_test,
    tab_bias_mitigation,
) = st.tabs(
    [
        "Linear Regression",
        "Logistic Regression",
        "Fairness Test",
        "Bias Mitigation",
    ]
)

# ==========================
# Set up data
# ==========================

# Est-ce que c'est vraiment nécessaire de charger les données ici ? 
# Possible de passer tout ce qui est calcul dans des fonctions src?
"""
# Chargement des variables d'environnement
load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)
logger.debug(f"Chemin du fichier StackOverflow récupéré : {stack_users_data_path}")


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

X = stack_users_df[
    [
        "Age",
        "Accessibility",
        "EdLevel",
        "Gender",
        "MentalHealth",
        "MainBranch",
        "YearsCode",
        "YearsCodePro",
        "PreviousSalary",
        "ComputerSkills",
    ]
]

y = stack_users_df["Employed"]
"""
VAL_COLS = ["PreviousSalary", "YearsCode", "YearsCodePro", "ComputerSkills"]

TO_DUMMIES = ["Age", "EdLevel", "Gender", "MentalHealth", "MainBranch"]

# ==========================
# Set up baseline models from dumps
# ==========================
"""
exp1 = dx.Explainer(
    joblib.load("output/models/decision_tree_baseline.joblib"), X, y
    )
exp2 = dx.Explainer(
    joblib.load("output/models/random_forest_baseline.joblib"), X, y
)
exp3 = dx.Explainer(
    joblib.load("output/models/logistic_regression_baseline.joblib"), X, y
)
exp4 = dx.Explainer(
    joblib.load("output/models/xgboost_baseline.joblib"), X, y
)
"""

# ==========================
# Linear Regression
# ==========================

tab_linear_regression.header("Regression Linéaire")
list_col3 = tab_linear_regression.multiselect(
    "Sélectionner les variables pour la regression linéaire: ",
    VAL_COLS + TO_DUMMIES + ["Employed"],
    default=VAL_COLS[1:] + TO_DUMMIES + ["Employed"],
)

y_col3 = tab_linear_regression.selectbox("Select", VAL_COLS)
result_df3, score3 = get_data_linear_regression(list_col3, y_col3)
tab_linear_regression.subheader(f"Le R2 du modèle est : {round(score3 * 100, 2)}%")
tab_linear_regression.table(result_df3)

# ==========================
# Logistic Regression
# ==========================

tab_logistic_regression.header("Regression Logistique")
list_col = tab_logistic_regression.multiselect(
    "Sélectionner les variables pour la regression logistique: ",
    VAL_COLS + TO_DUMMIES,
    default=VAL_COLS[1:] + TO_DUMMIES,
)
result_df, score, X, delta_prob = get_data_log_regression(parameters=list_col)
tab_logistic_regression.subheader(f"Le R2 du modèle est : {round(score * 100, 2)}%")
tab_logistic_regression.table(result_df)

# ==========================
# Fairness test
# ==========================

###
# Passer en fonction de façon à ce qu'on n'ait pas à charger les modèles sur cette page 
# (dans un script src plutôt comme pour get_data_..._regression ?)

tab_fairness_test.header("Modèles baseline:")

tab_fairness_test.subheader("Decision Tree performance")
result_df_exp1 = get_fairness_test(exp1)
tab_fairness_test.table(result_df_exp1)

tab_fairness_test.subheader("Random Forest performance")
result_df_exp2 = get_fairness_test(exp2)
tab_fairness_test.table(result_df_exp2)

tab_fairness_test.subheader("Logistic Regression performance")
result_df_exp3 = get_fairness_test(exp3)
tab_fairness_test.table(result_df_exp3)

tab_fairness_test.subheader("Gradient Boosting performance")
result_df_exp4 = get_fairness_test(exp4)
tab_fairness_test.table(result_df_exp4)
###

tab_fairness_test.header("Test d'équité")

criteria_selector_3 = tab_fairness_test.selectbox(
    "Sur quel critère tester l'équité ?",
    ["Age", "Gender", "MentalHealth", "Accessibility"],
)

criteria_selector_4 = tab_fairness_test.selectbox(
    'Quelle catégorie considérer comme "privileged" ?',
    set(stack_users_df[criteria_selector_3]), 
    # ici il faudra enlever le recours au df, par ex via un dict qui donne les catégories pour chq var possible de selector_3
)

plot = get_fairness_check(criteria_selector_3, criteria_selector_4)

(
    t5_fairness_check,
    t5_metric_scores,
    t5_stacked,
    t5_radar,
    t5_performance_and_fairness,
    t5_heatmap,
) = tab_fairness_test.tabs(
    [
        "Fairness Check",
        "Metric Scores",
        "Cumulated parity loss",
        "Radar",
        "Performance And Fairness",
        "Heatmap",
    ]
)

t5_fairness_check.plotly_chart(
    plot("fairness_check"), theme=None, use_container_width=True
)
t5_metric_scores.plotly_chart(
    plot("metric_scores"), theme=None, use_container_width=True
)
t5_stacked.plotly_chart(plot("stacked"), theme=None, use_container_width=True)
t5_radar.plotly_chart(plot("radar"), theme=None, use_container_width=True)
t5_performance_and_fairness.plotly_chart(
    plot("performance_and_fairness"), theme=None, use_container_width=True
)
t5_heatmap.plotly_chart(plot("heatmap"), theme=None, use_container_width=True)

# ==========================
# Bias mitigation
# ==========================

tab_bias_mitigation.header("Mitigation des biais avec Dalex")

model_selector = tab_bias_mitigation.selectbox(
    "Quel modèle devrait avoir ses biais mitigés ?",
    ["Random Forest", "Gradient Boosting", "Logistic Regression"],
    key="bias6_model_selectbox",
)

criteria_selector_5 = tab_bias_mitigation.selectbox(
    "Sur quel critère tester l'équité ?", ["Gender"], key="bias6_1_selectbox"
)

criteria_selector_6 = tab_bias_mitigation.selectbox(
    'Quelle catégorie considérer comme "privileged" ?',
    ["Woman", "Man"],
    key="bias6_2_selectbox",
)

plot = get_fairness_check_after_mitigation(
    criteria_selector_5, criteria_selector_6, model_selector
)

(
    t6_fairness_check,
    t6_metric_scores,
    t6_stacked,
    t6_radar,
    t6_performance_and_fairness,
    t6_heatmap,
) = tab_bias_mitigation.tabs(
    [
        "Fairness Check",
        "Metric Scores",
        "Cumulated parity loss",
        "Radar",
        "Performance And Fairness",
        "Heatmap",
    ]
)

t6_fairness_check.plotly_chart(
    plot("fairness_check"), theme=None, use_container_width=True
)
t6_metric_scores.plotly_chart(
    plot("metric_scores"), theme=None, use_container_width=True
)
t6_stacked.plotly_chart(plot("stacked"), theme=None, use_container_width=True)
t6_radar.plotly_chart(plot("radar"), theme=None, use_container_width=True)
t6_performance_and_fairness.plotly_chart(
    plot("performance_and_fairness"), theme=None, use_container_width=True
)
t6_heatmap.plotly_chart(plot("heatmap"), theme=None, use_container_width=True)
