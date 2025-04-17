"""
Ce module doit permettre l'entraînement et l'enregistrement des modèles ensuite utilisés dans 7_Modeles.py.
"""

preprocess = make_column_transformer(
    (StandardScaler(), num),
    (OneHotEncoder(), cat))

X1=df[['Age', 'Accessibility', 'EdLevel', 'Gender', 'MentalHealth', 'MainBranch','YearsCode', 'YearsCodePro', 'PreviousSalary', 'ComputerSkills']]
y1=df['Employed']

X1_train, X1_test, y1_train, y1_test=train_test_split(X1, y1, test_size = 0.25, random_state = 4)

# Avec l'échantillon d'origine
# Régression logistique
cv_lr1 = make_pipeline(
    preprocess,
    LogisticRegression(penalty='l2'))
cv_lr1.fit(X1_train, y1_train)

# Arbre de décision
cv_tree1 = make_pipeline(preprocess, DecisionTreeClassifier(max_depth=7, random_state=123))
cv_tree1.fit(X1_train, y1_train)

# Forêt aléatoire
cv_forest1 = make_pipeline(preprocess, RandomForestClassifier(n_estimators=200, max_depth=7, random_state=123))
cv_forest1.fit(X1_train, y1_train)

# XGBoost
cv_xg1 = make_pipeline(preprocess, xgb.XGBClassifier(objective='multi:softmax', num_class=3, max_depth=3, learning_rate=0.1, n_estimators=100))
cv_xg1.fit(X1_train, y1_train)

from joblib import dump

# Sauvegarde des modèles
dump(cv_lr1, 'modeles/logistic_regression_baseline.joblib')
dump(cv_tree1, 'modeles/decision_tree_baseline.joblib')
dump(cv_forest1, 'modeles/random_forest_baseline.joblib')
dump(cv_xg1, 'modeles/xgboost_baseline.joblib')

# Etude de la performance et de l'équité

# Créer un Explainer pour le Pipeline
exp_tree1 = dx.Explainer(cv_tree1, X1_test, y1_test, verbose=False)
exp_forest1 = dx.Explainer(cv_forest1, X1_test, y1_test, verbose=False)
exp1 = dx.Explainer(cv_lr1, X1_test, y1_test, label='Logistic regression Pipeline')
exp_xg1=dx.Explainer(cv_xg1, X1_test, y1_test, verbose=False)

# Performance du modèle
pd.concat([exp.model_performance().result for exp in [exp1, exp_tree1, exp_forest1,exp_xg1]])

# Importance des variables
exp_tree1.model_parts().plot(objects=[exp_forest1.model_parts(), exp1.model_parts(),exp_xg1.model_parts()])

# Preparation pour le test d'équité de Gender
protected = X1_test.Gender 
mf_tree1 = exp_tree1.model_fairness(protected=protected,
                                  privileged = "Woman")

mf_forest1 = exp_forest1.model_fairness(protected=protected,
                                  privileged = "Woman")

mf_log1 = exp1.model_fairness(protected=protected,
                                  privileged = "Woman")
mf_xg1=exp_xg1.model_fairness(protected=protected,
                                  privileged = "Woman")

mf_tree1.fairness_check()
mf_forest1.fairness_check()
mf_log1.fairness_check()
mf_xg1.fairness_check()

mf_tree1.plot(objects=[mf_log1, mf_forest1,mf_xg1],
             type="performance_and_fairness",
             fairness_metric="FPR",
             performance_metric="accuracy")

# Un exemple pour mieux comprendre
john = pd.DataFrame({'Age': '<35',
                       'Accessibility': ['Yes'],
                       'EdLevel': ['PhD'],
                       'Gender': ['Man'],
                       'MentalHealth': ['No'],
                       'MainBranch': ['Dev'],
                       'YearsCode':[14],
                       'YearsCodePro':[7],
                       'PreviousSalary': [60000],
                       'ComputerSkills': [7]
                     },
                      index = ['John'])
mary = pd.DataFrame({'Age': '<35',
                       'Accessibility': ['Yes'],
                       'EdLevel': ['PhD'],
                       'Gender': ['Woman'],
                       'MentalHealth': ['No'],
                       'MainBranch': ['Dev'],
                       'YearsCode':[14],
                       'YearsCodePro':[7],
                       'PreviousSalary': [60000],
                       'ComputerSkills': [7]
                     },
                      index = ['Mary'])
jean = pd.DataFrame({'Age': '<35',
                       'Accessibility': ['Yes'],
                       'EdLevel': ['PhD'],
                       'Gender': ['NonBinary'],
                       'MentalHealth': ['No'],
                       'MainBranch': ['Dev'],
                       'YearsCode':[14],
                       'YearsCodePro':[7],
                       'PreviousSalary': [60000],
                       'ComputerSkills': [7]
                     },
                      index = ['Jean'])

bd_john = exp_xg1.predict_parts(john, type='break_down', label=john.index[0])
bd_mary = exp_xg1.predict_parts(mary, type='break_down', label=mary.index[0])
bd_jean = exp_xg1.predict_parts(jean, type='break_down', label=jean.index[0])
bd_interactions_john = exp_xg1.predict_parts(john, type='break_down_interactions', label="John+")
bd_interactions_mary = exp_xg1.predict_parts(mary, type='break_down_interactions', label="Mary+")
bd_interactions_jean = exp_xg1.predict_parts(jean, type='break_down_interactions', label="Jean+")
sh_john = exp_xg1.predict_parts(john, type='shap', B = 10, label=john.index[0])
sh_mary = exp_xg1.predict_parts(mary, type='shap', B = 10, label=mary.index[0])
sh_jean = exp_xg1.predict_parts(jean, type='shap', B = 10, label=jean.index[0])

sh_john.plot(bar_width = 16)

sh_mary.plot(bar_width = 16)

sh_jean.plot(bar_width = 16)

### Mitigation des biais et nouveaux modèles

## Pre-processing mitigation

# NETTOYAGE DES DONNÉES
# Effectué lors de l'exploration des données

# SÉLECTION DES CARACTÉRISTIQUES
# Suppression des caractéristiques qui pourraient être des proxies pour des attributs protégés (comme 'Country' s'il est un proxy pour l'origine ethnique)
#df = df.drop(['Country'], axis=1)

# RÉ-ÉCHANTILLONNAGE
# Identification de la variable cible
target_column = 'Employed'

# Séparation de l'ensemble de données en classes majoritaires et minoritaires en fonction de la variable cible
majority_class = df[df[target_column] == df[target_column].mode()[0]]  
minority_class = df[df[target_column] != df[target_column].mode()[0]]  

# Sur-échantillonnage de la classe minoritaire
minority_upsampled = resample(minority_class,
                              replace=True,      
                              n_samples=len(majority_class), 
                              random_state=123) 

# Combinaison de la classe majoritaire avec la classe minoritaire sur-échantillonnée
upsampled_data = pd.concat([majority_class, minority_upsampled])

# Mélanger les données pour éviter tout biais d'ordre
upsampled_data = upsampled_data.sample(frac=1, random_state=123).reset_index(drop=True)

# L'ensemble de données 'upsampled_data' est maintenant un ensemble de données équilibré
upsampled_data.head()

## In-Processing mitigation

# Data preprocessing & preparation for modeling
X=upsampled_data[['Age', 'Accessibility', 'EdLevel', 'Gender', 'MentalHealth', 'MainBranch','YearsCode', 'YearsCodePro', 'PreviousSalary', 'ComputerSkills']]
y=upsampled_data['Employed']

X_train, X_test, y_train, y_test=train_test_split(X, y, test_size = 0.25, random_state = 4)

# Creation and training of classification models
#Avec les données pré-traitées
#Logistic regression
cv_lr = make_pipeline(
    preprocess,
    LogisticRegression(penalty = 'l2'))
cv_lr.fit(X_train, y_train)

#Decision Tree
cv_tree = make_pipeline(preprocess, DecisionTreeClassifier(max_depth=7, random_state=123))
cv_tree.fit(X_train, y_train)

#Random Forest
cv_forest = make_pipeline(preprocess, RandomForestClassifier(n_estimators=200, max_depth=7, random_state=123))
cv_forest.fit(X_train, y_train)

#XGBoost
cv_xg = make_pipeline(preprocess,xgb.XGBClassifier(objective='multi:softmax', num_class=3, max_depth=3, learning_rate=0.1, n_estimators=100))
cv_xg.fit(X_train, y_train)

# Sauvegarde des modèles
dump(cv_lr, 'modeles/logistic_regression.joblib')
dump(cv_tree, 'modeles/decision_tree.joblib')
dump(cv_forest, 'modeles/random_forest.joblib')
dump(cv_xg, 'modeles/xgboost.joblib')

# Performance analysis
# Créer un Explainer pour le Pipeline
exp_tree = dx.Explainer(cv_tree, X_test, y_test, verbose=False)
exp_forest = dx.Explainer(cv_forest, X_test, y_test, verbose=False)
exp = dx.Explainer(cv_lr, X_test, y_test, label='Logistic regression Pipeline')
exp_xg=dx.Explainer(cv_xg, X_test, y_test, verbose=False)

# Performance du modèle
pd.concat([exp.model_performance().result for exp in [exp, exp_tree, exp_forest,exp_xg]])

# Importance des variables
exp_tree.model_parts().plot(objects=[exp_forest.model_parts(), exp.model_parts(),exp_xg.model_parts()])

# Analysis of algorithmic fairness
# Preparation du Test Fairness
protected = X_test.Gender
mf_tree = exp_tree.model_fairness(protected=protected,
                                  privileged = "Woman")

mf_forest = exp_forest.model_fairness(protected=protected,
                                  privileged = "Woman")

mf_log = exp.model_fairness(protected=protected,
                                  privileged = "Woman")
mf_xg=exp_xg.model_fairness(protected=protected,
                                  privileged = "Woman")

mf_tree.fairness_check()

mf_forest.fairness_check()

mf_log.fairness_check()

mf_xg.fairness_check()

mf_tree.plot(objects=[mf_log, mf_forest, mf_xg])

mf_tree.plot(objects=[mf_log, mf_forest,mf_xg], type='stacked')

mf_tree.plot(objects=[mf_log, mf_forest,mf_xg],
             type="performance_and_fairness",
             fairness_metric="FPR",
             performance_metric="accuracy")

# Bias mitigation
# Ceteris paribus cutoff
mf_tree.plot(objects=[mf_log, mf_forest,mf_xg], type="ceteris_paribus_cutoff", subgroup="Woman")

# ROC Pivot
from dalex.fairness import resample, reweight, roc_pivot
privileged="Woman"
exp1 = copy(exp)
exp2 = copy(exp_forest)
exp3=copy(exp_tree)
expg=copy(exp_xg)
# roc pivot
exp1 = roc_pivot(exp1, protected, privileged, theta = 0.02, verbose = False)
exp2 = roc_pivot(exp2, protected, privileged, theta = 0.02, verbose = False)
exp3 = roc_pivot(exp3, protected, privileged, theta = 0.02, verbose = False)
expg = roc_pivot(expg, protected, privileged, theta = 0.02, verbose = False)

fobject1 = exp1.model_fairness(protected, privileged, label='roc Logistic')
fobject2 = exp2.model_fairness(protected, privileged, label='roc forest')
fobject3 = exp3.model_fairness(protected, privileged, label='roc tree')
fobjectg = expg.model_fairness(protected, privileged, label='roc xg')

fobject1.plot([fobject2,fobject3,fobjectg])

fobjectg.fairness_check()

fobject1.fairness_check()

fobject2.fairness_check()

fobject3.fairness_check()

# Resample
# copying
clf_u = copy(cv_lr)
clf_p = copy(cv_lr)
clfx=copy(cv_xg)
clfx2=copy(cv_xg)

indices_uniform = resample(X_test.Gender, y_test, verbose = False)
indices_preferential = resample(X_test.Gender,
                                y_test,
                                type = 'preferential', # different type
                                probs = exp.y_hat, # requires probabilities
                                verbose = False)


clf_u.fit(X_test.iloc[indices_uniform, :], y_test.iloc[indices_uniform])
clf_p.fit(X_test.iloc[indices_preferential, :], y_test.iloc[indices_preferential])
clfx.fit(X_test.iloc[indices_preferential, :], y_test.iloc[indices_preferential])
clfx2.fit(X_test.iloc[indices_uniform, :], y_test.iloc[indices_uniform])

exp3u = dx.Explainer(clf_u, X_test, y_test, verbose = False)
exp3p = dx.Explainer(clf_p, X_test, y_test, verbose = False)
exp3x = dx.Explainer(clfx, X_test, y_test, verbose = False)
exp3x1 = dx.Explainer(clfx2, X_test, y_test, verbose = False)

fobject3u = exp3u.model_fairness(protected, privileged, label='res_unif_lr')
fobject3p = exp3p.model_fairness(protected, privileged, label='res_pref_lr')
fobject3xx = exp3x.model_fairness(protected, privileged, label='res_pref_xg')
fobject3x1 = exp3x1.model_fairness(protected, privileged, label='res_unif_xg')

fobject3u.fairness_check()

fobject3p.fairness_check()

fobject3x1.fairness_check()

fobject3xx.fairness_check()

# Reweight
# Regression logistique
weights = reweight(protected, y_test, verbose = False)
cv_weighted_lr = copy(cv_lr)
kwargs = {cv_weighted_lr.steps[-1][0] + '__sample_weight': weights}
cv_weighted_lr.fit(X_test,y_test, **kwargs)

dump(cv_weighted_lr, 'modeles/test_lr.joblib')

expw_lr = dx.Explainer(cv_weighted_lr, X_test, y_test, verbose = False)
fobjectw_lr = expw_lr.model_fairness(protected, privileged, label='weighted')
fobjectw_lr.fairness_check()

fobject3wp = expw_lr.model_fairness(X_test.Age, '<35', label='weighted')
fobject3wp.fairness_check()

fobject3wp = expw_lr.model_fairness(X_test.MentalHealth, 'No', label='weighted')
fobject3wp.fairness_check()

fobject3wp = expw_lr.model_fairness(X_test.Accessibility, 'No', label='weighted')
fobject3wp.fairness_check()

# Arbre de décision
clf_weighted_forest = copy(cv_forest)
kwargs = {clf_weighted_forest.steps[-1][0] + '__sample_weight': weights}
clf_weighted_forest.fit(X_test,y_test, **kwargs)

dump(clf_weighted_forest, 'modeles/test_forest.joblib')

expwt = dx.Explainer(clf_weighted_forest, X_test, y_test, verbose = False)
fobject3wt = expwt.model_fairness(protected, privileged, label='weighted')
fobject3wt.fairness_check()

# XGBoost
clf_weighted_xg = copy(cv_xg)
kwargs = {clf_weighted_xg.steps[-1][0] + '__sample_weight': weights}
clf_weighted_xg.fit(X_test,y_test, **kwargs)

dump(clf_weighted_xg, 'modeles/test_xgb.joblib')

expxg = dx.Explainer(clf_weighted_xg, X_test, y_test, verbose = False)
fobjectxg = expxg.model_fairness(protected, privileged, label='weighted')
fobjectxg.fairness_check()

fobjectxg = expxg.model_fairness(X_test.Accessibility, 'No', label='weighted')
fobjectxg.fairness_check()

fobjectxg = expxg.model_fairness(X_test.MentalHealth, 'No', label='weighted')
fobjectxg.fairness_check()

fobjectxg = expxg.model_fairness(X_test.Age, '<35', label='weighted')
fobjectxg.fairness_check()

fobjectxg.plot()

# Detailed analysis with Dalex
explanation=expxg.model_parts()
explanation.result
explanation.plot()

explanationp=exp_xg1.model_parts()
explanationp.result
explanationp.plot()

mp = expxg.model_performance(model_type = 'classification')
mp.result

mp.plot(geom="roc")

## Post-processing mitigation/evaluation

# Complementary analysis
# Effectuer une validation croisée
cv_scores = cross_val_score(cv_xg, X_train, y_train, cv=5, scoring='accuracy')

# Afficher les scores de validation croisée
print("Scores de validation croisée :", cv_scores)
print("Précision moyenne : {:.2f}".format(cv_scores.mean()))

param_grid = {
    'xgbclassifier__learning_rate': [0.01, 0.1, 0.2],
    'xgbclassifier__max_depth': [3, 4, 5],
    'xgbclassifier__n_estimators': [50, 100, 200]
}

# Choisissez une stratégie de validation croisée, par exemple, une validation croisée à 5 plis
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Créez un pipeline avec prétraitement et XGBoost
xgb_model = make_pipeline(preprocess, xgb.XGBClassifier())

# Configurez GridSearchCV avec le pipeline
grid_search = GridSearchCV(xgb_model, param_grid, cv=kf, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)

# Affichez les meilleurs hyperparamètres
print("Meilleurs Hyperparamètres : ", grid_search.best_params_)

# Évaluez sur l'ensemble de test
y_pred = grid_search.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Erreur quadratique moyenne sur l'ensemble de test : ", mse)

ale_num = expxg.model_profile(type = 'accumulated', label="ale")

pdp_num = expxg.model_profile(type = 'partial', label="pdp")

pdp_num.plot(ale_num)

## Interprétation / visualisation de notre meilleur modèle (XGBoost)

john = pd.DataFrame({'Age': '<35',
                       'Accessibility': ['Yes'],
                       'EdLevel': ['PhD'],
                       'Gender': ['Man'],
                       'MentalHealth': ['No'],
                       'MainBranch': ['Dev'],
                       'YearsCode':[4],
                       'YearsCodePro':[7],
                       'PreviousSalary': [60000],
                       'ComputerSkills': [7]
                     },
                      index = ['John'])
mary = pd.DataFrame({'Age': '<35',
                       'Accessibility': ['Yes'],
                       'EdLevel': ['PhD'],
                       'Gender': ['Woman'],
                       'MentalHealth': ['No'],
                       'MainBranch': ['Dev'],
                       'YearsCode':[4],
                       'YearsCodePro':[7],
                       'PreviousSalary': [60000],
                       'ComputerSkills': [7]
                     },
                      index = ['Mary'])
jean = pd.DataFrame({'Age': '<35',
                       'Accessibility': ['Yes'],
                       'EdLevel': ['PhD'],
                       'Gender': ['NonBinary'],
                       'MentalHealth': ['No'],
                       'MainBranch': ['Dev'],
                       'YearsCode':[4],
                       'YearsCodePro':[7],
                       'PreviousSalary': [60000],
                       'ComputerSkills': [7]
                     },
                      index = ['Jean'])

bd_john = expxg.predict_parts(john, type='break_down', label=john.index[0])
bd_mary1 = expxg.predict_parts(mary, type='break_down', label=mary.index[0])
bd_jean = expxg.predict_parts(jean, type='break_down', label=jean.index[0])
bd_interactions_john = expxg.predict_parts(john, type='break_down_interactions', label="John+")
bd_interactions_mary1 = expxg.predict_parts(mary, type='break_down_interactions', label="Mary+")
bd_interactions_jean = expxg.predict_parts(jean, type='break_down_interactions', label="Jean+")
sh_john1 = expxg.predict_parts(john, type='shap', B = 10, label=john.index[0])
sh_mary1 = expxg.predict_parts(mary, type='shap', B = 10, label=mary.index[0])
sh_jean = expxg.predict_parts(jean, type='shap', B = 10, label=jean.index[0])

bd_john.plot(bd_interactions_john)

bd_mary1.plot(bd_interactions_mary1)

sh_mary1.plot(bar_width = 16)

sh_john1.plot(bar_width = 16)

sh_jean.plot(bar_width = 16)