import pandas as pd

def compute_top_languages_count(df, source_col, top_languages_list, new_col="TopLanguagesCount"):
    """
    Adds a column to the DataFrame (df) that counts how many langages from the top are known.
    
    Parameters :
        df (DataFrame): le dataframe d'origine
        source_col (str): nom de la colonne contenant les langages séparés par des ';'
        top_languages_list (list): liste des langages à compter
        new_col (str): nom de la nouvelle colonne à créer

    Returns:
        DataFrame: le dataframe avec deux colonnes supplémentaires : une liste et un compte
    """
    df = df.copy()
    df["LanguagesList"] = df[source_col].apply(
        lambda x: [] if pd.isna(x) else [lang.strip() for lang in x.split(";")]
    )

    df[new_col] = df["LanguagesList"].apply(
        lambda langlist: sum(lang in top_languages_list for lang in langlist)
    )

    return df


def group_percentage_by(df, group_cols, count_col_name="count", percent_col_name="percentage"):
    """
    Computes the count and percentage distribution of observations across subgroups in a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data to be grouped and analyzed.
    
    group_cols : list of str
        A list of column names to group by. The first column is used to compute subgroup percentages.
        For example: ["Gender", "EmployedCat"].
    
    count_col_name : str, optional
        Name of the column in the result that will contain the raw counts (default is "count").
    
    percent_col_name : str, optional
        Name of the column in the result that will contain the percentage values (default is "percentage").

    Returns
    -------
    pandas.DataFrame
        A DataFrame with the group columns, counts, and percentage values for each subgroup.
    """
    # Calcul du nombre d'éléments dans chaque groupe
    grouped_df = (
        df.groupby(group_cols, observed=True)
        .size()
        .reset_index(name=count_col_name)
    )

    # Calcul du total par le premier niveau de regroupement
    total_counts = df.groupby(group_cols[0]).size()

    # Ajout du pourcentage
    grouped_df[percent_col_name] = (
        grouped_df[count_col_name] / grouped_df[group_cols[0]].map(total_counts) * 100
    ).round(1)

    return grouped_df

import pandas as pd

def categorize_employment_status(df, column="Employed", new_col="EmployedCat", labels=["Sans emploi", "En emploi"]):
    """
    Converts a binary employment column into a categorical column with readable labels.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the column to transform.

    column : str, optional
        The name of the binary column to convert (default is "Employed").

    new_col : str, optional
        The name of the new column to be created (default is "EmployedCat").

    labels : list of str, optional
        The labels to assign to the categories: [label_for_0, label_for_1].

    Returns
    -------
    pandas.DataFrame
        A copy of the original DataFrame with the new categorical column added.
    """
    df_copy = df.copy()
    df_copy[new_col] = pd.cut(
        df_copy[column],
        bins=[-1, 0, 1],
        labels=labels
    ).astype("object")
    
    return df_copy
