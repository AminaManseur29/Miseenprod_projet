# Langages utilisés

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import plotly
import plotly.express as px

st.set_page_config(
    page_title="Langages utilisés", 
    page_icon=":chart_with_upwards_trend:"
)

with st.sidebar:
    st.title("Projet Python pour la Data Science")
    st.subheader("Pierre CLAYTON")
    st.subheader("Clément DE LARDEMELLE")
    st.subheader("Louise LIGONNIERE")

st.markdown(
    """
    ## Langages utilisés par les répondants

    Les langages les plus employés par les répondants sont les suivants : 

    """
)

# Chargement des données
df = pd.read_csv("stackoverflow_full.csv", index_col="Unnamed: 0")

# Langages informatiques utilisés
languages = [str(cat).split(";") for cat in df["HaveWorkedWith"]]
languages_all = [item for sublist in languages for item in sublist]

# Décompte du nombre d'occurences de chaque langage
languages_count = Counter(languages_all)

# Création d'un nuage de mots
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(languages_count)

# Afficher le nuage de mots généré
fig, ax = plt.subplots(figsize = (12, 8))
ax.imshow(wordcloud, interpolation = 'bilinear')
plt.axis("off")
st.pyplot(fig)

# Les 20 langages les plus employés
top_languages20 = languages_count.most_common(20)
top_languages20 = pd.DataFrame(top_languages20, columns = ["Langage", "Count"], index = range(1,21))

fig_lang = px.bar(top_languages20.sort_values(by = "Count"), 
                        x = "Count", y = "Langage", orientation = 'h',
                        text_auto = True, 
                        color = "Count",color_continuous_scale = "darkmint")

fig_lang.update_layout(
    title_text="Les 20 langages les plus employés",
    xaxis_title_text="Nombre d'occurences", 
    yaxis_title_text="Langage",
    bargap=0.2, 
    bargroupgap=0.1,
    width=800,
    height=700
)

st.plotly_chart(fig_lang)

# Mesure alternative des compétences en informatique
st.markdown(
    """
    ### Une mesure alternative des compétences en informatique
    
    Jusqu'ici, les compétences en informatique étaient mesurées via la variable `ComputerSkills` qui comptait le nombre de langages maîtrisés par chaque développeur. Ici, on crée une mesure alternative des compétences en informatique grâce à un décompte des langages maîtrisés parmi les 10 langages les plus courants dans la base.

    On obtient la distribution suivante : 
    """
)

# Ajout d'une colonne qui compte le nombre de langages maîtrisés parmi les 10 plus courants
top_languages = languages_count.most_common(10)
top_languages = pd.DataFrame(top_languages, columns = ["Langage", "Nombre d'occurences"], index = range(1,11))

df['LanguagesList'] = df['HaveWorkedWith'].apply(lambda x: [] if pd.isna(x) else x.split(';'))

df['TopLanguagesCount'] = df['LanguagesList'].apply(lambda langlist: sum(lang in list(top_languages["Langage"]) for lang in langlist))

# Graphe Langages parmi les top 10 langages
fig_info2 = px.histogram(df, x="TopLanguagesCount", barmode="group")

fig_info2.update_layout(
    title_text="Distribution des compétences en informatique - mesure alternative",
    xaxis_title_text="Nombre de langages maîtrisés parmi les 10 les plus présents", 
    yaxis_title_text="Effectif",
    bargap=0.2, 
    bargroupgap=0.1 
)

st.plotly_chart(fig_info2)

st.markdown(
    """
    Les langages utilisés sont donc très concentrés. Les 4 premiers langages (JavaScript, Docker, HTML/CSS et SQL) sont tous utilisés par plus de 50% des répondants, et jusqu'à 67% pour JavaScript.

    Lorsque l'on compte le nombre de langages maîtrisés parmi les 10 langages les plus cités dans la base, on trouve des résultats cohérents. Ainsi, presque l'intégralité (98%) des répondants maîtrisent au moins 1 de ces 10 langages. En moyenne, les répondants en maîtrisent 5. 
    """
)
