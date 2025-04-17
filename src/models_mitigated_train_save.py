"""
Ce module permet l'entraînement et l'enregistrement des modèles MITIGATED ensuite utilisés
dans 7_Modeles.py.
"""

import os
from copy import copy
from joblib import dump
import pandas as pd
from sklearn.utils import resample
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import xgboost as xgb
import dalex as dx
from dalex.fairness import reweight
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

# ==========================
# Pre-processing mitigation : ré-échantillonnage pour créer un ensemble de données équilibré
# ==========================

# Identification de la variable cible
TARGET_COLUMN = "Employed"

# Séparation de l'ensemble de données en classes majoritaires/minoritaires
# en fonction de la variable cible
majority_class = stack_users_df[
    stack_users_df[TARGET_COLUMN] == stack_users_df[TARGET_COLUMN].mode()[0]
]
minority_class = stack_users_df[
    stack_users_df[TARGET_COLUMN] != stack_users_df[TARGET_COLUMN].mode()[0]
]

# Sur-échantillonnage de la classe minoritaire
minority_upsampled = resample(
    minority_class, replace=True, n_samples=len(majority_class), random_state=123
)

# Combinaison de la classe majoritaire avec la classe minoritaire sur-échantillonnée
upsampled_data = pd.concat([majority_class, minority_upsampled])

# Mélanger les données pour éviter tout biais d'ordre
upsampled_data = upsampled_data.sample(frac=1, random_state=123).reset_index(drop=True)

# Préparation des données pour la modélisation
X2_preprocess = upsampled_data[
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
y2_preprocess = upsampled_data["Employed"]

X2_preprocess_train, X2_preprocess_test, y2_preprocess_train, y2_preprocess_test = (
    train_test_split(X2_preprocess, y2_preprocess, test_size=0.25, random_state=4)
)

# 1. Régression logistique
# Entraînement du modèle sur les données pré-traitées
cv_logreg_preprocess = make_pipeline(preprocess, LogisticRegression(penalty="l2"))
cv_logreg_preprocess.fit(X2_preprocess_train, y2_preprocess_train)

# Sauvegarde du modèle
dump(cv_logreg_preprocess, "modeles/logistic_regression_preprocess.joblib")

# Créer un Explainer pour le Pipeline
exp_logreg_preprocess = dx.Explainer(
    cv_logreg_preprocess,
    X2_preprocess_test,
    y2_preprocess_test,
    label="Logistic regression Pipeline",
)

# Test d'équité sur le genre
protected = X2_preprocess_test.Gender
mf_logreg_preprocess = exp_logreg_preprocess.model_fairness(
    protected=protected, privileged="Woman"
)
print(
    "Test d'équité sur le genre - Logistic Regression sur données ré-échantillonnées :"
)
mf_logreg_preprocess.fairness_check()

# 2. Random Forest
# Entraînement du modèle sur les données pré-traitées
cv_forest_preprocess = make_pipeline(
    preprocess, RandomForestClassifier(n_estimators=200, max_depth=7, random_state=123)
)
cv_forest_preprocess.fit(X2_preprocess_train, y2_preprocess_train)

# Sauvegarde du modèle
dump(cv_forest_preprocess, "modeles/random_forest_preprocess.joblib")

# Créer un Explainer pour le Pipeline
exp_forest_preprocess = dx.Explainer(
    cv_forest_preprocess, X2_preprocess_test, y2_preprocess_test, verbose=False
)

# Test d'équité sur le genre
mf_forest_preprocess = exp_forest_preprocess.model_fairness(
    protected=protected, privileged="Woman"
)
print("Test d'équité sur le genre - Random Forest sur données ré-échantillonnées :")
mf_forest_preprocess.fairness_check()

# 3. XGBoost
# Entraînement du modèle sur les données pré-traitées
cv_xgb_preprocess = make_pipeline(
    preprocess,
    xgb.XGBClassifier(
        objective="multi:softmax",
        num_class=3,
        max_depth=3,
        learning_rate=0.1,
        n_estimators=100,
    ),
)
cv_xgb_preprocess.fit(X2_preprocess_train, y2_preprocess_train)

# Sauvegarde du modèle
dump(cv_xgb_preprocess, "modeles/xgboost_preprocess.joblib")

# Créer un Explainer pour le Pipeline
exp_xgb_preprocess = dx.Explainer(
    cv_xgb_preprocess, X2_preprocess_test, y2_preprocess_test, verbose=False
)

# Test d'équité sur le genre
mf_xgb_preprocess = exp_xgb_preprocess.model_fairness(
    protected=protected, privileged="Woman"
)
print("Test d'équité sur le genre - Gradient Boosting sur données ré-échantillonnées :")
mf_xgb_preprocess.fairness_check()

# ==========================
# In-processing mitigation : méthode reweight
# ==========================

PRIVILEGED = "Woman"

# 1. Régression logistique
# Entraînement du modèle avec reweight
weights = reweight(protected, y2_preprocess_test, verbose=False)
cv_logreg_weighted = copy(cv_logreg_preprocess)
kwargs = {cv_logreg_weighted.steps[-1][0] + "__sample_weight": weights}
cv_logreg_weighted.fit(X2_preprocess_test, y2_preprocess_test, **kwargs)

# Enregistrement du modèle
dump(cv_logreg_weighted, "modeles/logistic_regressing_weighted.joblib")

# Test d'équité sur le genre
exp_logreg_weighted = dx.Explainer(
    cv_logreg_weighted, X2_preprocess_test, y2_preprocess_test, verbose=False
)
mf_logreg_weighted = exp_logreg_weighted.model_fairness(
    protected, PRIVILEGED, label="weighted"
)
print(
    "Test d'équité sur le genre - Régression Logistique après pré- et in-processing :"
)
mf_logreg_weighted.fairness_check()

# 2. Random Forest
# Entraînement du modèle avec reweight
cv_forest_weighted = copy(cv_forest_preprocess)
kwargs = {cv_forest_weighted.steps[-1][0] + "__sample_weight": weights}
cv_forest_weighted.fit(X2_preprocess_test, y2_preprocess_test, **kwargs)

# Enregistrement du modèle
dump(cv_forest_weighted, "modeles/random_forest_weighted.joblib")

# Test d'équité sur le genre
exp_forest_weighted = dx.Explainer(
    cv_forest_weighted, X2_preprocess_test, y2_preprocess_test, verbose=False
)
mf_forest_weighted = exp_forest_weighted.model_fairness(
    protected, PRIVILEGED, label="weighted"
)
print("Test d'équité sur le genre - Random Forest après pré- et in-processing :")
mf_forest_weighted.fairness_check()

# 3. XGBoost
# Entraînement du modèle avec reweight
cv_xgb_weighted = copy(cv_xgb_preprocess)
kwargs = {cv_xgb_weighted.steps[-1][0] + "__sample_weight": weights}
cv_xgb_weighted.fit(X2_preprocess_test, y2_preprocess_test, **kwargs)

# Enregistrement du modèle
dump(cv_xgb_weighted, "modeles/xgboost_weighted.joblib")

# Test d'équité sur le genre
exp_xgb_weighted = dx.Explainer(
    cv_xgb_weighted, X2_preprocess_test, y2_preprocess_test, verbose=False
)
mf_xgb_weighted = exp_xgb_weighted.model_fairness(
    protected, PRIVILEGED, label="weighted"
)
print("Test d'équité sur le genre - XGBoost après pré- et in-processing :")
mf_xgb_weighted.fairness_check()
