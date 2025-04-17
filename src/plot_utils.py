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

def plot_hist(data, col, title,xaxis_title= None,yaxis_title = "Effectif"):
    """
    Plots histogram of the column required (col) and gives a title. 
    Args : 
        data (DataFrame): dataframe used 
        col (str): column of interest 
        title (str) : title 
    Returns : 
        a bar plot of the required data 
    """
    xaxis_label = xaxis_title if xaxis_title is not None else col

    fig = px.histogram(data, x=col, barmode='group', text_auto=True)
    fig.update_layout(
        title_text=title,
        xaxis_title_text=col, 
        yaxis_title_text=yaxis_title,
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

def plot_bar(data,col,title):
    """
    Creates a bar plot of the column (col) and gives a title. 

    Parameters :
    ----------
    data : pandas.DataFrame
            DataFrame of the langages used 
    col : str
        Column of interest for the bar plot 
    title : str 
        Title of the graph 

    Returns:
    -------
    plotly bar plot 
    """

    fig = px.bar(
        data.sort_values(by="Count"),
        x="Count",
        y=col,
        orientation="h",
        text_auto=True,
        color="Count",
        color_continuous_scale="darkmint",
    )

    fig.update_layout(
        title_text=title,
        xaxis_title_text="Nombre d'occurences",
        yaxis_title_text=col,
        bargap=0.2,
        bargroupgap=0.1,
        width=800,
        height=700,
    )

def plot_bar_orders(data, y_col, color_col, title, cat_orders, x_col="percentage"):
    """
    Creates a horizontal bar plot showing the distribution of categories with percentages.

    Parameters
    ----------
    data : pandas.DataFrame
        The DataFrame containing the data to plot.  
    y_col : str
        The column to be shown on the Y-axis (e.g. 'Gender').  
    color_col : str
        The column to color the bars by (e.g. 'EmployedCat').
    title : str
        The title of the plot.
    cat_orders : dict
        Dictionary specifying the order of categorical variables for better display.  
    x_col : str, optional
        The column to be shown on the X-axis (default is 'percentage').

    Returns
    -------
    fig : plotly.graph_objects.Figure
        A Plotly horizontal bar chart with percentage formatting and custom styling.
    """
    fig = px.bar(
        data,
        orientation="h",
        x=x_col,
        y=y_col,
        color=color_col,
        text_auto=True,
        category_orders=cat_orders,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )

    fig.update_layout(
        title_text=title,
        xaxis_title_text="Pourcentage",
        yaxis_title_text=y_col,
        legend_title_text=color_col,
        bargap=0.2,
        bargroupgap=0.1,
        width=800,
        height=700,
    )

    fig.update_traces(texttemplate="%{x}%")
    return fig

def plot_box(
    data,
    x_col,
    y_col,
    color_col,
    title,
    color_sequence=["rgb(246, 207, 113)", "rgb(102, 197, 204)"],
    xaxis_title=None,
    yaxis_title=None
):
    """
    Creates a box plot to visualize the distribution of a numerical variable
    across different categories.

    Parameters
    ----------
    data : pandas.DataFrame
        The input DataFrame containing the data to plot.

    x_col : str
        The column to display on the X-axis (categorical variable).

    y_col : str
        The column to display on the Y-axis (numerical variable).

    color_col : str
        The column to color the boxes by. Usually the same as x_col for categorical comparison.

    title : str
        The title of the plot.

    color_sequence : list of str, optional
        A list of color codes to use for the boxes (default is pastel-like colors).

    xaxis_title : str, optional
        Custom label for the X-axis. Defaults to the value of `x_col`.

    yaxis_title : str, optional
        Custom label for the Y-axis. Defaults to the value of `y_col`.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        A Plotly box plot figure with customized layout.
    """

    x_title = xaxis_title if xaxis_title is not None else x_col
    y_title = yaxis_title if yaxis_title is not None else y_col

    fig = px.box(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        color_discrete_sequence=color_sequence,
    )

    fig.update_layout(
        title_text=title,
        xaxis_title_text=x_title,
        yaxis_title_text=y_title,
        legend_title_text=color_col,
        bargap=0.2,
        bargroupgap=0.1,
        width=800,
        height=700,
    )

    return fig

def plot_map(df_carto, min_respondents=100):
    """
    Creates a choropleth map showing the employment rate per country 
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

    fig = px.choropleth(
        df_filtered,
        locations="ISO",
        color="percentage",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Sunsetdark,
    )

    fig.update_layout(
        title_text=(
            f"Taux d'emploi par pays (≥ {min_respondents} répondants)"
        ),
        coloraxis_colorbar_title_text="Taux d'emploi",
    )

    return fig

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
        a wordcloud and the count of the items in the desired column 
    """
    tokens = [str(cat).split(";") for cat in data[col]]
    item_all = [item for sublist in tokens for item in sublist] # découpage en mots
    item_count = Counter(item_all) # décompte occurrences

    # Création d'un nuage de mots
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(item_count)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    return fig,item_count