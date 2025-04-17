# Emploi et variables numériques : boxplots

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
from collections import Counter

st.set_page_config(
    page_title="Emploi et variables numériques", 
    page_icon=":chart_with_upwards_trend:"
)

with st.sidebar:
    st.title("Projet Python pour la Data Science")
    st.subheader("Pierre CLAYTON")
    st.subheader("Clément DE LARDEMELLE")
    st.subheader("Louise LIGONNIERE")

st.markdown(
    """
    ## Emploi et variables numériques

    On étudie ici la distribution des quatre principales variables numériques selon le statut d'emploi.
    """
)

# Chargement des données
df = pd.read_csv("stackoverflow_full.csv", index_col="Unnamed: 0")

# Recodage des variables catégorielles (ENG -> FR)
df_fr = df.copy()

df_fr["EmployedCat"] = pd.cut(df_fr["Employed"], bins=[-1, 0, 1], labels=["Sans emploi", "En emploi"]).astype("object")

# 1. Années de code vs. statut d'emploi
fig_code = px.box(df_fr, x="EmployedCat", y = "YearsCode",
                  color = "EmployedCat", color_discrete_sequence = ['rgb(246, 207, 113)','rgb(102, 197, 204)']
)

fig_code.update_layout(
    title_text="Distribution des années de code selon le statut d'emploi",
    xaxis_title_text="Statut d'emploi", 
    yaxis_title_text="Années de code",
    legend_title_text = "Statut d'emploi",
    bargap=0.2, 
    bargroupgap=0.1
)

# 2. Années de code pro vs. statut d'emploi
fig_codepro = px.box(df_fr, x="EmployedCat", y = "YearsCodePro",
                  color = "EmployedCat", color_discrete_sequence = ['rgb(246, 207, 113)','rgb(102, 197, 204)']
)

fig_codepro.update_layout(
    title_text="Distribution des années de code professionnel selon le statut d'emploi",
    xaxis_title_text="Statut d'emploi", 
    yaxis_title_text="Années de code professionnel",
    legend_title_text = "Statut d'emploi",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 3. Salaire précédent vs. statut d'emploi
fig_salaire = px.box(df_fr, x="EmployedCat", y = "PreviousSalary",
                  color = "EmployedCat", color_discrete_sequence = ['rgb(246, 207, 113)','rgb(102, 197, 204)']
)

fig_salaire.update_layout(
    title_text="Distribution du salaire précédent selon le statut d'emploi",
    xaxis_title_text="Statut d'emploi", 
    yaxis_title_text="Salaire précédent",
    legend_title_text = "Statut d'emploi",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 4. Compétences en informatique vs. statut d'emploi
fig_info = px.box(df_fr, x="EmployedCat", y = "ComputerSkills",
                  color = "EmployedCat", color_discrete_sequence = ['rgb(246, 207, 113)','rgb(102, 197, 204)']
)

fig_info.update_layout(
    title_text="Distribution des compétences en informatique (nombre de langages maîtrisés) selon le statut d'emploi",
    xaxis_title_text="Statut d'emploi", 
    yaxis_title_text="Nombre de langages maîtrisés",
    legend_title_text = "Statut d'emploi",
    bargap=0.2, 
    bargroupgap=0.1 
)

# 5. Compétences en informatique - mesure alternative vs. statut d'emploi
# Liste des 10 langages les plus employés
languages = [str(cat).split(";") for cat in df_fr["HaveWorkedWith"]]
languages_all = [item for sublist in languages for item in sublist]
top_languages = pd.DataFrame(Counter(languages_all).most_common(10), 
                             columns = ["Langage", "Nombre d'occurences"], index = range(1,11))

# Ajout d'une colonne qui compte le nombre de langages maîtrisés parmi les 10 plus courants
df_fr['LanguagesList'] = df_fr['HaveWorkedWith'].apply(lambda x: [] if pd.isna(x) else x.split(';'))
df_fr['TopLanguagesCount'] = df_fr['LanguagesList'].apply(lambda langlist: sum(lang in list(top_languages["Langage"]) for lang in langlist))

# Graphe
fig_info2 = px.box(df_fr, x="EmployedCat", y = "TopLanguagesCount",
                  color = "EmployedCat", color_discrete_sequence = ['rgb(246, 207, 113)','rgb(102, 197, 204)']
)

fig_info2.update_layout(
    title_text="Distribution des compétences en informatique (mesure alternative) selon le statut d'emploi",
    xaxis_title_text="Statut d'emploi", 
    yaxis_title_text="Nombre de langages maîtrisés parmi les 10 langages les plus présents",
    legend_title_text = "Statut d'emploi",
    bargap=0.2, 
    bargroupgap=0.1 
)

# Choix du graphe
tab_code, tab_codepro, tab_salaire, tab_info, tab_info2 = st.tabs(["Années de code", "Années de code professionnel", "Salaire précédent", "Compétences en informatique", "Compétences en informatique - mesure alternative"])

with tab_code:
    st.plotly_chart(fig_code)
with tab_codepro:
    st.plotly_chart(fig_codepro)
with tab_salaire:
    st.plotly_chart(fig_salaire)
with tab_info:
    st.plotly_chart(fig_info)
with tab_info2:
    st.plotly_chart(fig_info2)

st.markdown(
    """
    Le nombre d'années de codage, dans le cadre professionnel ou non, et le salaire précédent semblent peu varier selon le statut d'emploi. Ces variables semblent donc peu pertinentes pour expliquer l'employabilité des répondants.

    A l'inverse, les compétences en informatique (qu'elles soient mesurées par le nombre total de langages maîtrisés ou parmi les 10 langages les plus fréquents) semblent plus importantes chez les répondants en emploi. Ainsi, les 3 quarts des répondants sans emploi maîtrisent moins de 12 langages, alors que les 3 quarts des répondants en emploi maîtrisent plus de 13 langages. Ce résultat est néanmoins à relier avec la branche professionnelle principale : ainsi, les répondants ne travaillant pas dans le développement, même s'ils sont peu dans la base, maîtrisent moins de langages, et sont aussi significativement moins employés.
    """
)
