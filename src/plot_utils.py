import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)
from IPython.display import HTML #pour afficher les graphes dans une cellule de notebook

import requests
import matplotlib.pyplot as plt 
from io import StringIO
import numpy as np
import pandas as pd

from wordcloud import WordCloud

from collections import Counter

def plot_hist(data, col, title):
    """
    Plots histogram of the column required (col) and gives a title. 
    Args : 
        data (DataFrame): dataframe used 
        col (str): column of interest 
        title (str) : title 
    Returns : 
        a bar plot of the required data 
    """
    fig = px.histogram(data, x=col, barmode='group', text_auto=True)
    fig.update_layout(
        title_text=title,
        xaxis_title_text=col, 
        yaxis_title_text="Effectif",
        bargap=0.2, 
        bargroupgap=0.1 
    )
    return fig

def plot_hist_orders(data, col, title, cat_orders):
    """
        Plots histogram of the column required (col) and gives a title. 
    Args : 
        data (DataFrame): dataframe used 
        col (str): column of interest 
        title (str) : title 
        cat_orders(dict) : dictionnary of the groups on which to plot 
    Returns : 
        a bar plot of the required data 
    """
    fig = px.histogram(data, x=col, barmode='group', text_auto=True, category_orders=cat_orders)
    fig.update_layout(
        title_text=title,
        xaxis_title_text=col, 
        yaxis_title_text="Effectif",
        bargap=0.2, 
        bargroupgap=0.1 
    )
    return fig

def plot_map(data_geo, col):
    """
        Plots a map of the column required (col) and gives a title. 
    Args : 
        data_geo (DataFrame): dataframe used 
        col (str): column of interest 
        title (str) : title 
        cat_orders(dict) : dictionnary of the groups on which to plot 
    Returns : 
        Map of the data and size 
    """ 
    fig_geo = px.choropleth(data_geo[data_geo['count'] > 100], locations="ISO",
                    color="percentage",
                    hover_name="Country",
                    color_continuous_scale=px.colors.sequential.Sunsetdark)

    fig_geo.update_layout(
        title_text="Taux d'emploi par pays (pour les pays ayant au moins 100 répondants)",
        coloraxis_colorbar_title_text="Taux d'emploi",
    )
    return fig_geo


def make_wordcloud(data, col):
    """
    Plots a wordcloud of the column col from a dataframe

    Args : 
        data (DataFrame) 
        col (str) : column from which the wordcloud is extracted
    Returns : 
        a wordcloud 
    """
    languages = [str(cat).split(";") for cat in data[col]]
    languages_all = [item for sublist in languages for item in sublist] # découpage en mots
    languages_count = Counter(languages_all)

    # Création d'un nuage de mots
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(languages_count)
    return wordcloud