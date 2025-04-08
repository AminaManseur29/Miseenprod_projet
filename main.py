import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from wordcloud import WordCloud
from collections import Counter
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode

init_notebook_mode(connected=True)
from IPython.display import (
    HTML,
)  # pour afficher les graphes dans une cellule de notebook

from bs4 import BeautifulSoup
import requests

from src.data_preprocessing import (
    labels_translation,
    get_iso_country_codes,
    add_iso_codes,
    add_continent_info,
    add_hdi_info,
    add_life_expectancy,
    add_expected_schooling,
    add_gni_per_capita,
)

# Chargement des données
stack_users_data = pd.read_csv("data/stackoverflow_full.csv", index_col="Unnamed: 0")

# Traduction des labels
users_data_fr = labels_translation(stack_users_data)

# Récupérer les codes ISO des pays
iso_df = get_iso_country_codes()

# Ajouter les codes ISO au DataFrame des utilisateurs
users_data_fr = add_iso_codes(users_data_fr, iso_df)

# Ajouter l'information sur le continent des pays
PATH_TO_CONTINENT_EXCEL = "data/Countries_Languages.xls"  # Remplace par le chemin réel
users_data_fr = add_continent_info(users_data_fr, PATH_TO_CONTINENT_EXCEL)

# Ajouter les données HDI
PATH_TO_HDI_EXCEL = "data/HDI.xlsx"  # Remplace par le chemin réel
users_data_fr = add_hdi_info(users_data_fr, PATH_TO_HDI_EXCEL)

# Ajouter l'espérance de vie
PATH_TO_LIFE_EXPECTANCY_EXCEL = "data/HDI.xlsx"  # Remplace par le chemin réel
users_data_fr = add_life_expectancy(users_data_fr, PATH_TO_LIFE_EXPECTANCY_EXCEL)

# Ajouter les années d'éducation espérées
PATH_TO_EDUCATION_EXCEL = "data/HDI.xlsx"  # Remplace par le chemin réel
users_data_fr = add_expected_schooling(users_data_fr, PATH_TO_EDUCATION_EXCEL)

# Ajouter les informations sur le RNB par habitant
PATH_TO_GNI_EXCEL = "data/HDI.xlsx"  # Remplace par le chemin réel
users_data_fr = add_gni_per_capita(users_data_fr, PATH_TO_GNI_EXCEL)
