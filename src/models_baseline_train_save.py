"""
Ce module permet l'entraînement et l'enregistrement des modèles BASELINE ensuite utilisés
dans 7_Modeles.py.
"""

import os
from joblib import dump
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import xgboost as xgb
import dalex as dx
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
stack_users_data_path = os.environ.get(
    "stack_users_data_path", "data/StackOverflowSurvey.csv"
)

# Chargement des données depuis le répertoire sspcloud
stack_users_df = pd.read_csv(stack_users_data_path, index_col="Unnamed: 0")

VAR_CAT = ["Age", "Accessibility", "EdLevel", "Gender", "MentalHealth", "MainBranch"]
VAR_NUM = ["YearsCode", "YearsCodePro", "PreviousSalary", "ComputerSkills"]

# Preprocess
preprocess = make_column_transformer(
    (StandardScaler(), VAR_NUM), (OneHotEncoder(), VAR_CAT)
)

# Préparation des données
X1 = stack_users_df[
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
y1 = stack_users_df["Employed"]

X1_train, X1_test, y1_train, y1_test = train_test_split(
    X1, y1, test_size=0.25, random_state=4
)

# 1. Régression logistique
# Entraînement du modèle sur l'échantillon d'origine
cv_logreg = make_pipeline(preprocess, LogisticRegression(penalty="l2"))
cv_logreg.fit(X1_train, y1_train)

# Sauvegarde du modèle
dump(cv_logreg, "modeles/logistic_regression_baseline.joblib")

# Créer un Explainer pour le Pipeline
exp_logreg = dx.Explainer(
    cv_logreg, X1_test, y1_test, label="Logistic regression Pipeline"
)

# Test d'équité sur le genre
protected = X1_test.Gender
mf_logreg = exp_logreg.model_fairness(protected=protected, privileged="Woman")
print("Test d'équité sur le genre - Logistic Regression :")
mf_logreg.fairness_check()

# 2. Random Forest
# Entraînement du modèle sur l'échantillon d'origine
cv_forest = make_pipeline(
    preprocess, RandomForestClassifier(n_estimators=200, max_depth=7, random_state=123)
)
cv_forest.fit(X1_train, y1_train)

# Sauvegarde du modèle
dump(cv_forest, "modeles/random_forest_baseline.joblib")

# Créer un Explainer pour le Pipeline
exp_forest = dx.Explainer(cv_forest, X1_test, y1_test, verbose=False)

# Test d'équité sur le genre
mf_forest = exp_forest.model_fairness(protected=protected, privileged="Woman")
print("Test d'équité sur le genre - Random Forest :")
mf_forest.fairness_check()

# 3. XGBoost
cv_xgb = make_pipeline(
    preprocess,
    xgb.XGBClassifier(
        objective="multi:softmax",
        num_class=3,
        max_depth=3,
        learning_rate=0.1,
        n_estimators=100,
    ),
)
cv_xgb.fit(X1_train, y1_train)

# Sauvegarde du modèle
dump(cv_xgb, "modeles/xgboost_baseline.joblib")

# Créer un Explainer pour le Pipeline
exp_xgb = dx.Explainer(cv_xgb, X1_test, y1_test, verbose=False)

# Test d'équité sur le genre
mf_xgb = exp_xgb.model_fairness(protected=protected, privileged="Woman")
print("Test d'équité sur le genre - Gradient Boosting :")
mf_xgb.fairness_check()
