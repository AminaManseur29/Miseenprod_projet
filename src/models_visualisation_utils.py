
"""
Ce module contient les fonctions nécessaires à la présentation des modèles.
"""

import dalex as dx
import joblib
from sklearn.linear_model import LinearRegression, LogisticRegression
import pandas as pd


# ==========================
# Set up data
# ==========================

FILE_PATH = "stackoverflow_full.csv"

stack_users_data = pd.read_csv(FILE_PATH)

stack_users_data = stack_users_data.drop(columns=["Unnamed: 0"])
stack_users_data = stack_users_data.drop(columns="HaveWorkedWith")

X = stack_users_data[
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

y = stack_users_data["Employed"]

VAL_COLS = ["PreviousSalary", "YearsCode", "YearsCodePro", "ComputerSkills"]

TO_DUMMIES = ["Age", "EdLevel", "Gender", "MentalHealth", "MainBranch"]


# ==========================
# Set up models (baseline + mitigated) from dumps
# ==========================

exp1 = dx.Explainer(
    joblib.load("output/models/decision_tree_baseline.joblib"), X, y
)
exp1_m = dx.Explainer(
    joblib.load("output/models/decision_tree.joblib"), X, y
)
exp2 = dx.Explainer(
    joblib.load("output/models/random_forest_baseline.joblib"), X, y
)
exp2_m = dx.Explainer(
    joblib.load("output/models/test_forest.joblib"), X, y
)
exp3 = dx.Explainer(
    joblib.load("output/models/logistic_regression_baseline.joblib"), X, y
)
exp3_m = dx.Explainer(
    joblib.load("output/models/test_lr.joblib"), X, y
)
exp4 = dx.Explainer(
    joblib.load("output/models/xgboost_baseline.joblib"), X, y
)
exp4_m = dx.Explainer(
    joblib.load("output/models/test_xgb.joblib"), X, y
)


# ==========================
# Utils function
# ==========================

def get_data_linear_regression(parameters, difference):
    val_cols = list(set(VAL_COLS).intersection(parameters).difference(difference))
    to_dummies = list(set(TO_DUMMIES).intersection(parameters).difference(difference))
    if len(to_dummies) > 0:
        X = pd.get_dummies(stack_users_data[to_dummies], drop_first=True, dtype=int)
    else:
        X = pd.DataFrame()
    X[val_cols] = stack_users_data[val_cols]
    reg = LinearRegression().fit(X, stack_users_data[difference])

    results = pd.DataFrame({"Variables": reg.feature_names_in_, "Coeff.": reg.coef_})
    return results, reg.score(X, stack_users_data[difference])


def get_data_log_regression(parameters):
    val_cols = list(set(VAL_COLS).intersection(parameters))
    to_dummies = list(set(TO_DUMMIES).intersection(parameters))

    if len(to_dummies) > 0:
        X = pd.get_dummies(stack_users_data[to_dummies], drop_first=True, dtype=int)
    else:
        X = pd.DataFrame()

    X[val_cols] = stack_users_data[val_cols]
    reg = LogisticRegression(max_iter=10).fit(X, stack_users_data["Employed"])

    prob = reg.predict_proba(X)[:, 0]
    delta_p = []

    for key in reg.feature_names_in_:
        X_mod = X.copy()

        if key in VAL_COLS:
            X_mod[key] = X_mod[key] - 1
            prob_mod = reg.predict_proba(X_mod)[:, 0]
            delta_p.append((prob_mod - prob).mean())
        else:  # To_dummies
            X_mod[key] = 0
            prob_mod = reg.predict_proba(X_mod)[:, 0]
            delta_p.append((prob_mod - prob)[X[key] == 1].mean())

    results = pd.DataFrame(
        {
            "Variables": reg.feature_names_in_,
            "Delta Prob.": [f"{round(x * 100, 2)} %" for x in delta_p],
            "Coeff.": reg.coef_[0],
        }
    )
    return results, reg.score(X, stack_users_data["Employed"]), X, delta_p


def get_fairness_check(criteria, privileged):
    protected = stack_users_data[criteria]
    f_object_dc = exp1.model_fairness(
        protected=protected, privileged=privileged, label="Decision Tree"
    )
    f_object_rf = exp2.model_fairness(
        protected=protected, privileged=privileged, label="Random Forest"
    )
    f_object_lr = exp3.model_fairness(
        protected=protected, privileged=privileged, label="Logistic Regression"
    )
    f_object_gb = exp4.model_fairness(
        protected=protected, privileged=privileged, label="Gradient Boosting"
    )
    return lambda t: f_object_dc.plot([f_object_rf, f_object_lr, f_object_gb], type=t, show=False)


def get_fairness_check_after_mitigation(criteria, privileged, model):
    protected = stack_users_data[criteria]
    lookup = {
        "Random Forest": [exp2, exp2_m],
        "Gradient Boosting": [exp4, exp4_m],
        "Logistic Regression": [exp3, exp3_m]
    }

    f_object = lookup[model][0].model_fairness(
        protected=protected, privileged=privileged, label=model
    )
    f_object_mitigated = lookup[model][1].model_fairness(
        protected=protected, privileged=privileged, label=(model + " (Mitigated)")
    )
    return lambda t: f_object.plot([f_object_mitigated], type=t, show=False)
