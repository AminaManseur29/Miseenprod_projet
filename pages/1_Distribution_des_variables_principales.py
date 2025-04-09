"""
Ce module génère la distribution des variables principales
"""

import streamlit as st
import pandas as pd

from src.data_preprocessing import labels_translation
from src.plot_utils import plot_hist, plot_hist_orders

st.set_page_config(
    page_title="Distribution des variables principales",
    page_icon=":chart_with_upwards_trend:",
)

with st.sidebar:
    st.title("Projet Python pour la Data Science")
    st.subheader("Pierre CLAYTON")
    st.subheader("Clément DE LARDEMELLE")
    st.subheader("Louise LIGONNIERE")


st.markdown(
    """
    ## Distribution des variables principales

    On étudie ici la distribution des variables d'intérêt sur les répondants :
    l'âge, le genre, le niveau d'éducation, la branche professionnelle, le nombre d'années de code,
    le nombre d'années de code dans le cadre professionnel, le salaire précédent,
    et les compétences en informatique.

    Vous pouvez utiliser les flèches pour naviguer entre les graphiques.
    """
)

STACK_USERS_DATA = "data/StackOverflowSurvey.csv"

# Chargement des données
stack_users_df = pd.read_csv(STACK_USERS_DATA, index_col="Unnamed: 0")

# Recodage des variables catégorielles (ENG -> FR)
stack_users_df_fr = labels_translation(stack_users_df)

# 1. Graphe Age
fig_age = plot_hist(stack_users_df_fr, "Age", "Distribution de l'âge")

# 2. Graphe Genre
fig_genre = plot_hist(stack_users_df_fr, "Gender", "Distribution du genre")

# 3. Graphe Niveau d'éducation
fig_ed = plot_hist_orders(
    stack_users_df_fr,
    "EdLevel",
    "Distribution du niveau d'éducation",
    {
        "EdLevel": [
            "Pas d'éducation supérieure",
            "Licence",
            "Master",
            "Doctorat",
            "Autre",
        ]
    },
)

# 4. Graphe Branche pro
fig_branch = plot_hist(
    stack_users_df_fr, "MainBranch", "Distribution de la branche professionnelle"
)

# 5. Graphe Années de code
fig_code = plot_hist(
    stack_users_df_fr, "YearsCode", "Distribution des années de code"
)

# 6. Graphe Années de code pro
fig_codepro = plot_hist(
    stack_users_df_fr, "YearsCodePro", "Distribution des années de code professionnel"
)

# 7. Graphe Salaire précédent
fig_salaire = plot_hist(
    stack_users_df_fr, "PreviousSalary", "Distribution du salaire précédent"
)

# 8. Graphe Compétences en informatique
fig_info = plot_hist(
    stack_users_df_fr,
    "ComputerSkills",
    "Distribution des compétences en informatique",
)

# Choix du graphe
tab_age, tab_genre, tab_ed, tab_branch, tab_code, tab_codepro, tab_salaire, tab_info = (
    st.tabs(
        [
            "Age",
            "Genre",
            "Niveau d'éducation",
            "Branche professionnelle",
            "Années de code",
            "Années de code professionnel",
            "Salaire précédent",
            "Compétences en informatique",
        ]
    )
)

with tab_age:
    st.plotly_chart(fig_age)
with tab_genre:
    st.plotly_chart(fig_genre)
with tab_ed:
    st.plotly_chart(fig_ed)
with tab_branch:
    st.plotly_chart(fig_branch)

with tab_code:
    st.plotly_chart(fig_code)
with tab_codepro:
    st.plotly_chart(fig_codepro)
with tab_salaire:
    st.plotly_chart(fig_salaire)
with tab_info:
    st.plotly_chart(fig_info)

st.markdown(
    """
    Les répondants sont majoritairement jeunes (65% ont moins de 35 ans).
    Plus de 93% sont des hommes, ce qui est le défaut principal de notre base.
    Environ 50% des répondants ont un niveau licence, et 25% un master.
    La plus grande partie de la base travaille dans le développement (plus de 91%).

    Le nombre d'années de codage est très dispersé,
    atteignant jusqu'à 50 ans pour les répondants ayant le plus d'ancienneté de codage.
    On remarque toutefois un pic autour de 10 années de codage
    (ce qui est cohérent avec l'âge plutôt jeune des répondants).
    Le nombre d'années de codage dans le cadre professionnel est légèrement moins élevé et moins
    dispersé, avec un pic plutôt autour de 4 ans de codage.

    Le salaire précédent est aussi extrêmement dispersé.

    Enfin, les compétences en informatique, mesurées ici par le nombre de langages maîtrisés,
    semble suivre une gaussienne avec en moyenne une dizaine de langages. On remarque quelques
    valeurs extrêmes de répondants maitrisant plus de 50 langages.
    """
)
