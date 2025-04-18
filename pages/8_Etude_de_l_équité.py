"""
Ce module génère la page Etude de l'équité de l'application de visualisation Streamlit.
"""

import streamlit as st
from src.models_visualisation_utils import (
    get_fairness_check,
    get_fairness_check_after_mitigation,
)

# ==========================
# User interface
# ==========================

# Configuration de la page
st.set_page_config(
    page_title="Etude de l'équité",
    page_icon=":chart_with_upwards_trend:",
)

with st.sidebar:
    st.title("Projet Mise en production pour la data-science")
    st.subheader("Louise LIGONNIERE")
    st.subheader("Amina MANSEUR")
    st.subheader("Lila MEKKI")

st.markdown(
    """
    ## Etude de l'équité selon le genre
    """
)

(tab_fairness_test, tab_bias_mitigation) = st.tabs(
    ["Test d'équité selon le genre", "Modèles intégrant une mitigation des biais"]
)

# ==========================
# Fairness test
# ==========================

latext = r'''
    Commençons par un petit mot sur la mesure de l'équité de nos modèles. En effet, pour faciliter
    le développement d'un modèle responsable, nous utilisons le package Python dalex :
    https://dalex.drwhy.ai/

    Citant le tutoriel de Dalex :

    > L'idée est que les rapports entre les scores des métriques privilégiées et non privilégiées
    devraient être proches de 1. Plus ils le sont, plus c'est équitable. Pour assouplir un peu ce
    critère, cela peut être formulé de manière plus réfléchie :
    $$
    \forall i \in \{a, b, ..., z\}, \quad \epsilon < \frac{métrique_i}{métrique_{privilégiée}} <
    \frac{1}{\epsilon}
    $$

    > Où epsilon est une valeur comprise entre 0 et 1, elle devrait être une valeur minimale
    acceptable du rapport. Par défaut, elle est de 0.8, ce qui respecte la règle des quatre
    cinquièmes (règle des 80%) souvent observée dans l'embauche, par exemple.

    Description des métriques utilisées pour l'évaluation de la performance en termes d'équité pour
    chaque stratégie :

    - **Ratio d'opportunité égale** calculé à partir du taux de vrais positifs (rappel)
    > Ce nombre décrit les proportions d'instances positives correctement classifiées.
    > $TPR = \frac{TP}{P}$

    - **Ratio de parité prédictive** calculé à partir de la valeur prédictive positive (précision)
    > Ce nombre décrit le ratio d'échantillons qui ont été correctement classifiés comme positifs
    parmi toutes les prédictions positives.
    > $PPV = \frac{TP}{TP + FP}$

    - **Ratio d'égalité de précision** calculé à partir de la précision
    > Ce nombre est le ratio des instances correctement classifiées (positives et négatives) parmi
    toutes les décisions.
    > $ACC = \frac{TP + TN}{TP + FP + TN + FN}$

    - **Ratio d'égalité prédictive** calculé à partir du taux de faux positifs
    > Ce nombre décrit la part de négatifs réels qui ont été faussement classifiés comme positifs.
    > $FPR = \frac{FP}{TP + TN}$

    - **Ratio de parité statistique** calculé à partir du taux de positifs
    > Ce nombre est le taux global d'instances classifiées positivement, incluant à la fois les
    décisions correctes et incorrectes.
    > $PR = \frac{TP + FP}{TP + FP + TN + FN}$
'''

tab_fairness_test.write(latext)

criteria_selector_3 = tab_fairness_test.selectbox(
    'Quelle catégorie considérer comme "privileged" ?',
    ["Man", "Woman"],
)

plot = get_fairness_check("Gender", criteria_selector_3)

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

tab_bias_mitigation.markdown(
    """
    Comment mitiger le biais observé ?
    - **Atténuation en prétraitement** :
        - *Nettoyage des données* : Gérer les valeurs manquantes et les erreurs qui peuvent affecter
        certains groupes.
        - *Sélection des caractéristiques* : Choisir des caractéristiques qui n'incluent pas de
        variables de substitution pour les attributs protégés.
        - *Ré-échantillonnage ou ré-pondération* : Équilibrer l'ensemble de données en
        suréchantillonnant les groupes sous-représentés.

    - **Atténuation en cours de traitement** :
        - *Sélection d'algorithmes* : Choisir des algorithmes moins sensibles aux déséquilibres.
        - *Incorporer des contraintes d'équité* : Modifier les algorithmes pour inclure l'équité
        pendant l'entraînement.
        - *Validation* : Utiliser la validation croisée pour garantir des performances équitables
        entre les sous-groupes.

    - **Atténuation après le traitement** :
        - *Ajustement des seuils de décision* : Égaliser les faux positifs et les faux négatifs
        entre les groupes.
        - *Étalonnage* : Ajuster les prédictions pour garantir la cohérence.
        - *Analyse des résultats* : Analyser les décisions en termes d'équité avant de les
        finaliser.

    Après plusieurs essais, on retient deux étapes que l'on applique dans l'estimation de nos
    modèles présentés ci-dessous :
    - avant le traitement, un ré-échantillonnage des données pour créer un ensemble de données
    équilibré
    - pendant le traitement, l'application de la technique de repondération, qui ajuste les poids
    attribués aux différents échantillons de l'ensemble de données d'entraînement, accordant
    davantage d'importance aux groupes sous-représentés. Cela contribue à réduire les biais en
    veillant à ce que le modèle accorde plus d'attention à ces groupes pendant l'entraînement.
    """
)

model_selector = tab_bias_mitigation.selectbox(
    "Quel modèle devrait avoir ses biais mitigés ?",
    ["Random Forest", "Gradient Boosting", "Logistic Regression"],
    key="bias6_model_selectbox",
)

criteria_selector_4 = tab_bias_mitigation.selectbox(
    'Quelle catégorie considérer comme "privileged" ?',
    ["Man", "Woman"],
    key="bias6_2_selectbox",
)

plot = get_fairness_check_after_mitigation(
    "Gender", criteria_selector_4, model_selector
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
