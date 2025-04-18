"""
plot_utils.py

Ce module contient un ensemble de fonctions de visualisation basées sur Plotly et Matplotlib,
permettant de générer des graphiques interactifs tels que des histogrammes, barplots, boxplots,
cartes choroplèthes et nuages de mots, à partir de DataFrames pandas.
"""

from collections import Counter

import matplotlib.pyplot as plt
import plotly.express as px
# from plotly.offline import init_notebook_mode
from wordcloud import WordCloud

# Initialize Plotly for notebooks
# init_notebook_mode(connected=True)


def plot_hist(data, col, title, xaxis_title=None, yaxis_title="Effectif"):
    """
    Creates a histogram of the specified column.

    Parameters
    ----------
    data : pandas.DataFrame
        The input DataFrame.
    col : str
        The column to plot.
    title : str
        Title of the histogram.
    xaxis_title : str, optional
        Custom title for the X-axis. Defaults to `col`.
    yaxis_title : str, optional
        Custom title for the Y-axis. Default is "Effectif".

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly histogram figure.
    """
    xaxis_label = xaxis_title if xaxis_title is not None else col

    fig = px.histogram(data, x=col, barmode="group", text_auto=True)
    fig.update_layout(
        title_text=title,
        xaxis_title_text=xaxis_label,
        yaxis_title_text=yaxis_title,
        bargap=0.2,
        bargroupgap=0.1,
    )
    return fig


def plot_hist_orders(data, col, title, cat_orders):
    """
    Creates a histogram of the specified column with custom category order.

    Parameters
    ----------
    data : pandas.DataFrame
        The input DataFrame.
    col : str
        The column to plot.
    title : str
        Title of the histogram.
    cat_orders : dict
        Dictionary defining the order of categories.

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly histogram figure.
    """
    fig = px.histogram(
        data, x=col, barmode="group", text_auto=True, category_orders=cat_orders
    )
    fig.update_layout(
        title_text=title,
        xaxis_title_text=col,
        yaxis_title_text="Effectif",
        bargap=0.2,
        bargroupgap=0.1,
    )
    return fig


def plot_bar(data, col, title):
    """
    Creates a horizontal bar plot of the specified column.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing the column to plot.
    col : str
        The column to visualize.
    title : str
        Title of the plot.

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly horizontal bar chart.
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
        The input DataFrame.
    y_col : str
        Column for the Y-axis (e.g., categories).
    color_col : str
        Column used for coloring the bars.
    title : str
        Title of the plot.
    cat_orders : dict
        Dictionary defining the display order of categories.
    x_col : str, optional
        Column for the X-axis values (default is "percentage").

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly horizontal bar chart.
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
    yaxis_title=None,
):
    """
    Creates a box plot to visualize the distribution of a numeric variable across categories.

    Parameters
    ----------
    data : pandas.DataFrame
        Input data to plot.
    x_col : str
        Column used for X-axis (categorical variable).
    y_col : str
        Column used for Y-axis (numerical variable).
    color_col : str
        Column used for coloring boxes (usually same as `x_col`).
    title : str
        Title of the plot.
    color_sequence : list of str, optional
        Color palette for the boxes.
    xaxis_title : str, optional
        Custom label for the X-axis.
    yaxis_title : str, optional
        Custom label for the Y-axis.

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly box plot.
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
        title_text=(f"Taux d'emploi par pays (≥ {min_respondents} répondants)"),
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
    min_value=None,
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
    Generates and plots a word cloud from a specified column of a DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
        Input data.
    col : str
        Column containing text data (e.g., delimited by semicolons).

    Returns
    -------
    matplotlib.figure.Figure
        Matplotlib figure with the word cloud.
    collections.Counter
        Counter object with word frequencies.
    """
    tokens = [str(cat).split(";") for cat in data[col]]
    item_all = [item for sublist in tokens for item in sublist]  # découpage en mots
    item_count = Counter(item_all)  # décompte occurrences

    # Création d'un nuage de mots
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(item_count)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    return fig, item_count
