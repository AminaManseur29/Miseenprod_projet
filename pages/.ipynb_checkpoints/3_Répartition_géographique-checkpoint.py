# Répartition géographique

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.express as px

st.set_page_config(
    page_title="Répartition géographique", 
    page_icon=":chart_with_upwards_trend:"
)

with st.sidebar:
    st.title("Projet Python pour la Data Science")
    st.subheader("Pierre CLAYTON")
    st.subheader("Clément DE LARDEMELLE")
    st.subheader("Louise LIGONNIERE")

st.markdown(
    """
    ## Répartition géographique des répondants

    On étudie ici la répartition géographique de deux variables : le nombre de développeurs ayant répondu à l'enquête, et le taux d'emploi.

    """
)

# Chargement des données
df = pd.read_csv("stackoverflow_full.csv", index_col="Unnamed: 0")

# Ajout d'une colonne Code ISO (nécessaire pour les cartes)

from bs4 import BeautifulSoup
import requests

url = "https://www.iban.com/country-codes"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html')

table = soup.find('table')

titles = table.find_all('th')

table_titles = [title.text for title in titles]

iso = pd.DataFrame(columns = table_titles)

column_data = table.find_all('tr')

for row in column_data[1:]:
    row_data = row.find_all('td')
    individual_row_data = [data.text for data in row_data]
    length = len(iso)
    iso.loc[length] = individual_row_data

iso_dict = iso.set_index('Country')['Alpha-3 code'].to_dict()

dict_missing_values = {'United Kingdom of Great Britain and Northern Ireland' : 'GBR',
                       'Russian Federation' : 'RUS',
                       'United States of America' : 'USA',
                       'Netherlands' : 'NLD',
                       'Iran, Islamic Republic of...' : 'IRN',
                       'Hong Kong (S.A.R.)' : 'HKG',
                       'United Arab Emirates' : 'ARE',
                       'Bolivia' : 'BOL',
                       'Czech Republic' : 'CZE',
                       'The former Yugoslav Republic of Macedonia' : 'MKD',
                       'Venezuela, Bolivarian Republic of...' : 'VEN',
                       'Dominican Republic' : 'DOM',
                       'Syrian Arab Republic' : 'SYR',
                       'Taiwan' : 'TWN',
                       'South Korea' : 'KOR',
                       'Republic of Moldova' : 'MDA',
                       "Lao People's Democratic Republic" : 'LAO',
                       'Democratic Republic of the Congo' : 'COG',
                       'Philippines' : 'PHL',
                       'United Republic of Tanzania' : 'TZA',
                       'Kosovo' : 'XXK',
                       'Nomadic' : None,
                       'Congo, Republic of the...' : 'COG',
                       'Republic of Korea' : 'KOR',
                       'Swaziland' : 'SWZ',
                       'Libyan Arab Jamahiriya' : 'LBY',
                       'Sudan' : 'SDN',
                       'Palestine' : 'PSE',
                       'Cape Verde' : 'CPV',
                       'Niger' : 'NER',
                       'Gambia' : 'GMB'
                      }

iso_dict.update(dict_missing_values)

df['ISO'] = df['Country'].map(iso_dict)

# Tableau nombre de répondants et taux d'emploi par pays
df_carto = df.groupby(['Country','ISO'])['Employed'].agg(['count', 'mean']).reset_index()
df_carto.columns = ['Country', 'ISO', 'count', 'percentage']
df_carto['percentage'] *= 100

# 1. Carte du nb de développeurs par pays
fig_nb = px.choropleth(df_carto, locations="ISO",
                    color="count",
                    hover_name="Country",
                    color_continuous_scale=px.colors.sequential.Sunsetdark)

fig_nb.update_layout(
    title_text="Nombre de répondants par pays",
    coloraxis_colorbar_title_text = "Effectif",
)

# 2. Carte du taux d'emploi par pays
fig_taux = px.choropleth(df_carto[df_carto['count']>100], locations="ISO",
                    color="percentage",
                    hover_name="Country",
                    color_continuous_scale=px.colors.sequential.Sunsetdark)

fig_taux.update_layout(
    title_text="Taux d'emploi par pays (pour les pays ayant au moins 100 répondants)",
    coloraxis_colorbar_title_text = "Taux d'emploi",
)

# 3. Tableau nombre de répondants et taux d'emploi par continent

# Dictionnaire des continents
cont_pays = pd.read_excel("Countries_Languages.xls", skiprows = 1)
continents_dict = cont_pays.set_index('Country')['Continental Region'].to_dict()

# Ajout des valeurs manquantes
dict_missing_values = {'United Kingdom of Great Britain and Northern Ireland' : 'Europe',
                       'Russian Federation' : 'Europe',
                       'United States of America' : 'North,Central America',
                       'Viet Nam' : 'Asia (West)',
                       'Iran, Islamic Republic of...' : 'Asia (West)',
                       'Hong Kong (S.A.R.)' : 'Asia (East)',
                       'Belarus' : 'Europe',
                       'The former Yugoslav Republic of Macedonia' : 'Europe',
                       'Venezuela, Bolivarian Republic of...' : 'South America',
                       'Syrian Arab Republic' : 'Asia (West)',
                       'Taiwan' : 'Asia (East)',
                       'South Korea' : 'Asia (East)',
                       'Cameroon' : 'Africa',
                       'Republic of Moldova' : 'Europe',
                       "Lao People's Democratic Republic" : 'Asia (East)',
                       'Democratic Republic of the Congo' : 'Africa',
                       'United Republic of Tanzania' : 'Africa',
                       'Kosovo' : 'Europe',
                       'Congo, Republic of the...' : 'Africa',
                       'Republic of Korea' : 'Asia (East)',
                       'Saint Kitts and Nevis' : 'North,Central America',
                       'Monaco' : 'Europe',
                       'Libyan Arab Jamahiriya' : 'Asia (West)',
                       'Palestine' : 'Asia (West)',
                       'Isle of Man' : 'Europe',
                       "Côte d'Ivoire" : 'Africa',
                       'Senegal' : 'Africa',
                       'Saint Lucia' : 'North,Central America',
                       'Saint Vincent and the Grenadines' : 'North,Central America'
                      }

continents_dict.update(dict_missing_values)

# Ajout de la colonne Continent
df['Continent'] = df['Country'].map(continents_dict)

df["Continent"] = df["Continent"].replace(
    ["Africa", "Asia (East)", "Asia (South)", "Asia (West)", "North,Central America", "South America", "Oceania"],
    ["Afrique", "Asie", "Asie", "Asie", "Amérique du Nord et Centrale","Amérique du Sud", "Océanie"]
)

# Tableau des répondants et emploi en fonction des continents
df_carto_cont = df.groupby(['Continent'])['Employed'].agg(['count', 'mean'])
df_carto_cont = df_carto_cont.sort_values(by = "count", ascending = False).reset_index()
df_carto_cont["mean"] = (df_carto_cont["mean"]*100).round(2)

df_carto_cont.columns = ['Continent', 'Nombre de répondants', "Taux d'emploi"]

# Choix du graphe
tab_nb, tab_taux, tab_cont = st.tabs(["Nombre de répondants par pays", "Taux d'emploi par pays", "Nombre de répondants et taux d'emploi par continent"])

with tab_nb:
    st.plotly_chart(fig_nb)
with tab_taux:
    st.plotly_chart(fig_taux)
with tab_cont:
    st.dataframe(df_carto_cont)

st.markdown(
    """

    Les répondants sont répartis sur tous les continents de façon relativement satisfaisante. Ainsi, l'Europe et l'Amérique du Nord et Centrale concentrent plus de 70% des répondants. L'Asie est aussi plutôt bien représentée, avec 17% des répondants. Le principal écueil est que l'Amérique du Sud, l'Océanie et l'Afrique sont peu représentés dans la base. Les pays les plus représentés sont les États-Unis (20% des répondants), l'Allemagne (7%), l'Inde (7%), le Royaume-Uni (6%), le Canada, la France et le Brésil (entre 3.5 et 4%). 

    Le taux d'emploi est globalement uniforme entre les pays et continents, entre 50 et 60%. On note tout de même quelques valeurs élevées (dépassant les 65% voire atteignant plus de 70% pour le Pérou et le Sri Lanka). Ces valeurs sont toutefois à relativiser du fait de la faible taille des échantillons de répondants dans ces pays. Les valeurs les plus faibles, entre 40 et 45%, sont trouvées en Géorgie, Biélorussie, Ukraine et Russie. Ces valeurs sont surtout fiables pour la Russie et l'Ukraine (où les échantillons de répondants sont suffisants). Du point de vue des continents, le taux d'emploi semble légèrement plus faible en Europe que dans les autres régions, et légèrement plus élevé en Afrique.   
    """
)
