# Distribution des variables principales

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px

st.set_page_config(
    page_title="Distribution des variables principales", 
    page_icon=":chart_with_upwards_trend:"
)

with st.sidebar:
    st.title("Projet Python pour la Data Science")
    st.subheader("Pierre CLAYTON")
    st.subheader("Clément DE LARDEMELLE")
    st.subheader("Louise LIGONNIERE")


st.markdown(
    """
    ## Distribution des variables principales

    On étudie ici la distribution des variables d'intérêt sur les répondants : l'âge, le genre, le niveau d'éducation, la branche professionnelle, le nombre d'années de code, le nombre d'années de code dans le cadre professionnel, le salaire précédent, et les compétences en informatique.

    Vous pouvez utiliser les flèches pour naviguer entre les graphiques.
    """
)

# Chargement des données
df = pd.read_csv("stackoverflow_full.csv", index_col="Unnamed: 0")

# Recodage des variables catégorielles (ENG -> FR)
df_fr = df.copy()

df_fr["EmployedCat"] = pd.cut(df_fr["Employed"], bins=[-1, 0, 1], labels=["Sans emploi", "En emploi"]).astype("object")

df_fr["Age"] = df_fr["Age"].replace(
    ["<35", ">35"],
    ["Moins de 35 ans", "Plus de 35 ans"]
)

df_fr["Accessibility"] = df_fr["Accessibility"].replace(
    ["No", "Yes"],
    ["Non", "Oui"]
)

df_fr["EdLevel"] = df_fr["EdLevel"].replace(
    ["NoHigherEd", "Undergraduate", "Master", "PhD", "Other"],
    ["Pas d'éducation supérieure", "Licence", "Master", "Doctorat", "Autre"]
)

df_fr["Gender"] = df_fr["Gender"].replace(
    ["Man", "Woman", "NonBinary"],
    ["Homme", "Femme", "Non-Binaire"]
)

df_fr["MentalHealth"] = df_fr["MentalHealth"].replace(
    ["No", "Yes"],
    ["Non", "Oui"]
)

df_fr["MainBranch"] = df_fr["MainBranch"].replace(
    ["Dev", "NotDev"],
    ["Développement", "Autre"]
)

# 1. Graphe Age
fig_age = px.histogram(df_fr, x="Age", barmode="group", text_auto = True)

fig_age.update_layout(
    title_text="Distribution de l'âge",
    xaxis_title_text='Age', 
    yaxis_title_text="Effectif",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 2. Graphe Genre
fig_genre = px.histogram(df_fr, x="Gender", barmode="group", text_auto = True)

fig_genre.update_layout(
    title_text="Distribution du genre",
    xaxis_title_text='Genre', 
    yaxis_title_text="Effectif",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 3. Graphe Niveau d'éducation
fig_ed = px.histogram(df_fr, x="EdLevel", barmode="group", 
                      text_auto = True, 
                      category_orders = dict(EdLevel = ["Pas d'éducation supérieure", "Licence", "Master", "Doctorat", "Autre"])
                     )

fig_ed.update_layout(
    title_text="Distribution du niveau d'éducation",
    xaxis_title_text="Niveau d'éducation", 
    yaxis_title_text="Effectif",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 4. Graphe Branche pro
fig_branch = px.histogram(df_fr, x="MainBranch", barmode="group", text_auto = True)

fig_branch.update_layout(
    title_text="Distribution de la branche professionnelle",
    xaxis_title_text="Branche professionnelle (principale)", 
    yaxis_title_text="Effectif",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 5. Graphe Années de code
fig_code = px.histogram(df_fr, x="YearsCode", barmode="group")

fig_code.update_layout(
    title_text="Distribution des années de code",
    xaxis_title_text="Nombre d'années de code", 
    yaxis_title_text="Effectif",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 6. Graphe Années de code pro
fig_codepro = px.histogram(df_fr, x="YearsCodePro", barmode="group")

fig_codepro.update_layout(
    title_text="Distribution des années de code professionnel",
    xaxis_title_text="Nombre d'années de code professionnel", 
    yaxis_title_text="Effectif",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 7. Graphe Salaire précédent
fig_salaire = px.histogram(df_fr, x="PreviousSalary", barmode="group")

fig_salaire.update_layout(
    title_text="Distribution du salaire précédent",
    xaxis_title_text="Salaire précédent", 
    yaxis_title_text="Effectif",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 8. Graphe Compétences en informatique
fig_info = px.histogram(df_fr, x="ComputerSkills", barmode="group")

fig_info.update_layout(
    title_text="Distribution des compétences en informatique",
    xaxis_title_text="Nombre de langages maîtrisés", 
    yaxis_title_text="Effectif",
    bargap=0.2, 
    bargroupgap=0.1 
)

# Choix du graphe
tab_age, tab_genre, tab_ed, tab_branch, tab_code, tab_codepro, tab_salaire, tab_info = st.tabs(["Age", "Genre", "Niveau d'éducation", "Branche professionnelle", "Années de code", "Années de code professionnel", "Salaire précédent", "Compétences en informatique"])

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
    Les répondants sont majoritairement jeunes (65% ont moins de 35 ans). Plus de 93% sont des hommes, ce qui est le défaut principal de notre base. Environ 50% des répondants ont un niveau licence, et 25% un master. La plus grande partie de la base travaille dans le développement (plus de 91%).

    Le nombre d'années de codage est très dispersé, atteignant jusqu'à 50 ans pour les répondants ayant le plus d'ancienneté de codage. On remarque toutefois un pic autour de 10 années de codage (ce qui est cohérent avec l'âge plutôt jeune des répondants). Le nombre d'années de codage dans le cadre professionnel est légèrement moins élevé et moins dispersé, avec un pic plutôt autour de 4 ans de codage.

    Le salaire précédent est aussi extrêmement dispersé. 

    Enfin, les compétences en informatique, mesurées ici par le nombre de langages maîtrisés, semble suivre une gaussienne avec en moyenne une dizaine de langages. On remarque quelques valeurs extrêmes de répondants maitrisant plus de 50 langages.
    """
)
