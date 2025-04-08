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

def plot_map(df_carto, min_respondents=100):
    """
    Create a choropleth map showing the employment rate per country 
    (only for countries with at least `min_respondents`).

    Parameters:
    ----------
    df_carto : pandas.DataFrame
        DataFrame with columns 'ISO', 'Country', 'count', and 'percentage'.
    min_respondents : int, optional
        Minimum number of respondents required to display a country.

    Returns:
    -------
    plotly.graph_objects.Figure
        Choropleth map figure.
    """
    df_filtered = df_carto[df_carto["count"] > min_respondents]

    fig_taux = px.choropleth(
        df_filtered,
        locations="ISO",
        color="percentage",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Sunsetdark,
    )

    fig_taux.update_layout(
        title_text=(
            f"Taux d'emploi par pays (≥ {min_respondents} répondants)"
        ),
        coloraxis_colorbar_title_text="Taux d'emploi",
    )

    return fig_taux

def plot_choropleth_map(
    df,
    location_col,
    value_col,
    hover_col,
    color_scale=px.colors.sequential.Sunsetdark,
    title="",
    colorbar_title="",
    filter_col=None,
    min_value=None
):
    """
    General-purpose function to generate a choropleth map.

    Parameters:
    ----------
    df : pandas.DataFrame
        Input data with at least the columns for locations and values.
    location_col : str
        Column name containing ISO codes or geographic codes.
    value_col : str
        Column name to be represented by color.
    hover_col : str
        Column name to show when hovering.
    color_scale : list, optional
        Plotly color scale to use.
    title : str, optional
        Title of the map.
    colorbar_title : str, optional
        Title for the color scale bar.
    filter_col : str, optional
        Column to apply a minimum value filter on (e.g., count of respondents).
    min_value : float, optional
        Minimum value required to include a row in the map.

    Returns:
    -------
    plotly.graph_objects.Figure
        A choropleth map.
    """
    if filter_col and min_value is not None:
        df = df[df[filter_col] > min_value]

    fig = px.choropleth(
        df,
        locations=location_col,
        color=value_col,
        hover_name=hover_col,
        color_continuous_scale=color_scale,
    )

    fig.update_layout(
        title_text=title,
        coloraxis_colorbar_title_text=colorbar_title,
    )

    return fig

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