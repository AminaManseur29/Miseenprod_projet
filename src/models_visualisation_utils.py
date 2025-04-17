"""
Ce module contient les fonctions nécessaires à la présentation des modèles.
"""

import os
import dalex as dx
import joblib
import pandas as pd
from dotenv import load_dotenv
from sklearn.linear_model import LogisticRegression

# ==========================
# Set up data
# ==========================

# Chargement des variables d'environnement
load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)

# Chargement des données depuis le répertoire sspcloud
stack_users_df = pd.read_csv(stack_users_data_path, index_col="Unnamed: 0")

VAR_NUM = ["PreviousSalary", "YearsCode", "YearsCodePro", "ComputerSkills"]
VAR_CAT = ["Age", "EdLevel", "Gender", "MentalHealth", "MainBranch"]

# ==========================
# Set up models (baseline + mitigated) from dumps
# ==========================

X_model = stack_users_df[
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

y_model = stack_users_df["Employed"]

exp2 = dx.Explainer(joblib.load("output/models/random_forest_baseline.joblib"), X_model, y_model)
exp2_m = dx.Explainer(joblib.load("output/models/random_forest_weighted.joblib"), X_model, y_model)
exp3 = dx.Explainer(
    joblib.load("output/models/logistic_regression_baseline.joblib"), X_model, y_model
)
exp3_m = dx.Explainer(
    joblib.load("output/models/logistic_regression_weighted.joblib"), X_model, y_model
)
exp4 = dx.Explainer(joblib.load("output/models/xgboost_baseline.joblib"), X_model, y_model)
exp4_m = dx.Explainer(joblib.load("output/models/xgboost_weighted.joblib"), X_model, y_model)

# ==========================
# Utils function
# ==========================


def get_data_log_regression(parameters):
    """
    Entraîne une régression logistique sur les variables données et mesure leur effet marginal
    sur la probabilité d'être employé.

    Paramètres
    ----------
    parameters : list of str
        Noms des variables à inclure (numériques et/ou catégorielles).

    Retourne
    --------
    results : DataFrame
        Coefficients, effets marginaux et noms des variables.
    score : float
        Précision du modèle.
    X : DataFrame
        Données utilisées pour l'entraînement.
    delta_p : list of float
        Effets marginaux bruts des variables.
    """

    val_cols = list(set(VAR_NUM).intersection(parameters))
    to_dummies = list(set(VAR_CAT).intersection(parameters))

    if len(to_dummies) > 0:
        df_to_regress = pd.get_dummies(stack_users_df[to_dummies], drop_first=True, dtype=int)
    else:
        df_to_regress = pd.DataFrame()

    df_to_regress[val_cols] = stack_users_df[val_cols]
    reg = LogisticRegression(max_iter=10).fit(df_to_regress, stack_users_df["Employed"])

    prob = reg.predict_proba(df_to_regress)[:, 0]
    delta_p = []

    for key in reg.feature_names_in_:
        df_mod = df_to_regress.copy()

        if key in VAR_NUM:
            df_mod[key] = df_mod[key] - 1
            prob_mod = reg.predict_proba(df_mod)[:, 0]
            delta_p.append((prob_mod - prob).mean())
        else:  # To_dummies
            df_mod[key] = 0
            prob_mod = reg.predict_proba(df_mod)[:, 0]
            delta_p.append((prob_mod - prob)[df_to_regress[key] == 1].mean())

    results = pd.DataFrame(
        {
            "Variables": reg.feature_names_in_,
            "Delta Prob.": [f"{round(x * 100, 2)} %" for x in delta_p],
            "Coeff.": reg.coef_[0],
        }
    )
    return results, reg.score(df_to_regress, stack_users_df["Employed"]), df_to_regress, delta_p


def get_model_performance(model):
    """
    Retourne les résultats de performance du modèle spécifié.

    Paramètres
    ----------
    model : str
        Nom du modèle ("Random Forest", "Logistic Regression", "Gradient Boosting").

    Retourne
    --------
    result : any
        Résultat de la méthode `model_performance().result` associée au modèle.
    """

    lookup = {
        "Random Forest": [exp2],
        "Logistic Regression": [exp3],
        "Gradient Boosting": [exp4],
    }
    return lookup[model][0].model_performance().result


def get_fairness_check(criteria, privileged):
    """
    Prépare une fonction de visualisation de la fairness selon un critère et un groupe privilégié.

    Paramètres
    ----------
    criteria : str
        Colonne du DataFrame utilisée comme variable protégée.
    privileged : str or int
        Valeur considérée comme privilégiée pour cette variable.

    Retourne
    --------
    function
        Fonction prenant un type de plot (`t`) et affichant la comparaison de fairness entre
        modèles.
    """

    protected = stack_users_df[criteria]
    f_object_rf = exp2.model_fairness(
        protected=protected, privileged=privileged, label="Random Forest"
    )
    f_object_lr = exp3.model_fairness(
        protected=protected, privileged=privileged, label="Logistic Regression"
    )
    f_object_gb = exp4.model_fairness(
        protected=protected, privileged=privileged, label="Gradient Boosting"
    )
    return lambda t: f_object_rf.plot([f_object_lr, f_object_gb], type=t, show=False)


def get_fairness_check_after_mitigation(criteria, privileged, model):
    """
    Prépare une fonction de visualisation de la fairness avant/après mitigation pour un modèle
    donné.

    Paramètres
    ----------
    criteria : str
        Colonne protégée du DataFrame.
    privileged : str or int
        Valeur privilégiée pour cette variable.
    model : str
        Nom du modèle ("Random Forest", "Gradient Boosting", "Logistic Regression").

    Retourne
    --------
    function
        Fonction prenant un type de plot (`t`) et affichant la fairness avant/après mitigation.
    """

    protected = stack_users_df[criteria]
    lookup = {
        "Random Forest": [exp2, exp2_m],
        "Gradient Boosting": [exp4, exp4_m],
        "Logistic Regression": [exp3, exp3_m],
    }

    f_object = lookup[model][0].model_fairness(
        protected=protected, privileged=privileged, label=model
    )
    f_object_mitigated = lookup[model][1].model_fairness(
        protected=protected, privileged=privileged, label=(model + " (Mitigated)")
    )
    return lambda t: f_object.plot([f_object_mitigated], type=t, show=False)
