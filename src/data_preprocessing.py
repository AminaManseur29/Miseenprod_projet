"""
Ce module définit des fonctions utiles pour le prétraitement des données
"""

import pandas as pd

from bs4 import BeautifulSoup
import requests


def labels_translation(df):
    """
    Translates and categorizes specific columns in a DataFrame from English to French.

    This function performs the following operations:
    1. Creates a new categorical variable 'EmployedCat' from the 'Employed' column:
       - Values <= 0 are labeled as "Sans emploi" (Unemployed).
       - Values > 0 are labeled as "En emploi" (Employed).

    2. Translates the values of several columns from English to French:
       - "Age": "<35" → "Moins de 35 ans", ">35" → "Plus de 35 ans"
       - "Accessibility": "No" → "Non", "Yes" → "Oui"
       - "EdLevel": maps education levels to French equivalents
       - "Gender": maps gender identities to French
       - "MentalHealth": "No" → "Non", "Yes" → "Oui"
       - "MainBranch": "Dev" → "Développement", "NotDev" → "Autre"

    Args:
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the columns to be translated.

    Returns:
    -------
    pandas.DataFrame
        The DataFrame with translated values and a new 'EmployedCat' column.
    """

    # Nouvelle variable catégorisée pour Employed
    df["EmployedCat"] = pd.cut(
        df["Employed"], bins=[-1, 0, 1], labels=["Sans emploi", "En emploi"]
    )

    # Dictionnaire de traduction
    translations = {
        "Age": {"<35": "Moins de 35 ans", ">35": "Plus de 35 ans"},
        "Accessibility": {"No": "Non", "Yes": "Oui"},
        "EdLevel": {
            "NoHigherEd": "Pas d'éducation supérieure",
            "Undergraduate": "Licence",
            "Master": "Master",
            "PhD": "Doctorat",
            "Other": "Autre",
        },
        "Gender": {"Man": "Homme", "Woman": "Femme", "NonBinary": "Non-Binaire"},
        "MentalHealth": {"No": "Non", "Yes": "Oui"},
        "MainBranch": {"Dev": "Développement", "NotDev": "Autre"},
    }

    # Application des remplacements
    df.replace(translations, inplace=True)

    return df


# Enrichissement des données


def get_iso_country_codes(url):
    """
    Retrieves ISO country code table from iban.com.

    Returns:
        pd.DataFrame: A DataFrame containing the columns 'Country', 'Alpha-2 code',
                      Alpha-3 code', and 'Numeric code'.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    headers = [th.text.strip() for th in table.find_all("th")]
    rows = table.find_all("tr")[1:]

    data = [[td.text.strip() for td in row.find_all("td")] for row in rows]
    return pd.DataFrame(data, columns=headers)


def add_iso_codes(df, iso_df):
    """
    Adds an 'ISO' column to the `df` DataFrame containing ISO alpha-3 country codes.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.
        iso_df (pd.DataFrame): The ISO code DataFrame, with 'Country' and
        and 'Alpha-3 code' columns.

    Returns:
        pd.DataFrame: The DataFrame enriched with an 'ISO' column.
    """
    iso_dict = iso_df.set_index("Country")["Alpha-3 code"].to_dict()

    # Ajout manuel de valeurs manquantes
    manual_iso = {
        "United Kingdom of Great Britain and Northern Ireland": "GBR",
        "Russian Federation": "RUS",
        "United States of America": "USA",
        "Netherlands": "NLD",
        "Iran, Islamic Republic of...": "IRN",
        "Hong Kong (S.A.R.)": "HKG",
        "United Arab Emirates": "ARE",
        "Bolivia": "BOL",
        "Czech Republic": "CZE",
        "The former Yugoslav Republic of Macedonia": "MKD",
        "Venezuela, Bolivarian Republic of...": "VEN",
        "Dominican Republic": "DOM",
        "Syrian Arab Republic": "SYR",
        "Taiwan": "TWN",
        "South Korea": "KOR",
        "Republic of Moldova": "MDA",
        "Lao People's Democratic Republic": "LAO",
        "Democratic Republic of the Congo": "COG",
        "Philippines": "PHL",
        "United Republic of Tanzania": "TZA",
        "Kosovo": "XXK",
        "Nomadic": None,
        "Congo, Republic of the...": "COG",
        "Republic of Korea": "KOR",
        "Swaziland": "SWZ",
        "Libyan Arab Jamahiriya": "LBY",
        "Sudan": "SDN",
        "Palestine": "PSE",
        "Cape Verde": "CPV",
        "Niger": "NER",
        "Gambia": "GMB",
    }

    iso_dict.update(manual_iso)
    df["ISO"] = df["Country"].map(iso_dict)

    return df


def add_continent_info(df, path_to_excel):
    """
    Adds a 'Continent' column to the DataFrame from an Excel file
    file listing countries and continents.

    Args:
        df (pd.DataFrame): The DataFrame to be enriched.
        path_to_excel (str): Path to Excel file containing continent table.

    Returns:
        pd.DataFrame: The DataFrame enriched with the 'Continent' column.
    """
    cont_pays = pd.read_excel(path_to_excel, skiprows=1)
    continents_dict = cont_pays.set_index("Country")["Continental Region"].to_dict()

    # Valeurs manquantes à ajouter manuellement
    manual_continents = {
        "United Kingdom of Great Britain and Northern Ireland": "Europe",
        "Russian Federation": "Europe",
        "United States of America": "North,Central America",
        "Viet Nam": "Asia (West)",
        "Iran, Islamic Republic of...": "Asia (West)",
        "Hong Kong (S.A.R.)": "Asia (East)",
        "Belarus": "Europe",
        "The former Yugoslav Republic of Macedonia": "Europe",
        "Venezuela, Bolivarian Republic of...": "South America",
        "Syrian Arab Republic": "Asia (West)",
        "Taiwan": "Asia (East)",
        "South Korea": "Asia (East)",
        "Cameroon": "Africa",
        "Republic of Moldova": "Europe",
        "Lao People's Democratic Republic": "Asia (East)",
        "Democratic Republic of the Congo": "Africa",
        "United Republic of Tanzania": "Africa",
        "Kosovo": "Europe",
        "Congo, Republic of the...": "Africa",
        "Republic of Korea": "Asia (East)",
        "Saint Kitts and Nevis": "North,Central America",
        "Monaco": "Europe",
        "Libyan Arab Jamahiriya": "Asia (West)",
        "Palestine": "Asia (West)",
        "Isle of Man": "Europe",
        "Côte d'Ivoire": "Africa",
        "Senegal": "Africa",
        "Saint Lucia": "North,Central America",
        "Saint Vincent and the Grenadines": "North,Central America",
    }

    continents_dict.update(manual_continents)
    df["Continent"] = df["Country"].map(continents_dict)

    # Regroupement des sous-régions
    df["Continent"] = df["Continent"].replace(
        [
            "Africa",
            "Asia (East)",
            "Asia (South)",
            "Asia (West)",
            "North,Central America",
            "South America",
            "Oceania",
        ],
        [
            "Afrique",
            "Asie",
            "Asie",
            "Asie",
            "Amérique du Nord et Centrale",
            "Amérique du Sud",
            "Océanie",
        ],
    )

    return df


# Ajout de diverses variables mesurant le niveau de développement des pays
def add_hdi_info(df, path_to_excel):
    """
    Adds the Human Development Index (HDI/HDI) to the DataFrame from an Excel file.

    Args:
        df (pd.DataFrame): The DataFrame containing a 'Country' column.
        path_to_excel (str): Path to Excel file containing HDI data.

    Returns:
        pd.DataFrame: The DataFrame enriched with an 'HDI' column.
    """

    # Lecture des colonnes nécessaires
    infos_pays = pd.read_excel(
        path_to_excel,
        usecols=[1, 2, 4, 6, 10],
        skiprows=6,
        names=[
            "Country",
            "HDI",
            "Life expectancy at birth",
            "Expected years of schooling",
            "Gross national income (GNI) per capita",
        ],
    )

    hdi_dict = infos_pays.set_index("Country")["HDI"].to_dict()

    # Valeurs manquantes à ajouter manuellement
    manual_hdi = {
        "United Kingdom of Great Britain and Northern Ireland": 0.929,
        "Turkey": 0.838,
        "United States of America": 0.921,
        "Iran, Islamic Republic of...": 0.774,
        "Hong Kong (S.A.R.)": 0.952,
        "Bolivia": 0.692,
        "Czech Republic": 0.889,
        "The former Yugoslav Republic of Macedonia": 0.770,
        "Venezuela, Bolivarian Republic of...": 0.691,
        "Taiwan": 0.768,
        "South Korea": None,
        "Republic of Moldova": 0.767,
        "Democratic Republic of the Congo": 0.571,
        "United Republic of Tanzania": 0.549,
        "Kosovo": None,
        "Nomadic": None,
        "Congo, Republic of the...": 0.571,
        "Republic of Korea": None,
        "Swaziland": 0.597,
        "Libyan Arab Jamahiriya": 0.718,
        "Palestine": 0.715,
        "Isle of Man": None,
        "Cape Verde": None,
    }

    hdi_dict.update(manual_hdi)

    # Mapping
    df["HDI"] = df["Country"].map(hdi_dict)

    return df


def add_life_expectancy(df, path_to_excel):
    """
    Adds life expectancy at birth to the DataFrame from an Excel file.

    Args:
        df (pd.DataFrame): The DataFrame containing a 'Country' column.
        path_to_excel (str): Path to Excel file containing data.

    Returns:
        pd.DataFrame: The DataFrame enriched with a 'LifeExpectancy' column.
    """

    # Chargement des données
    infos_pays = pd.read_excel(
        path_to_excel,
        usecols=[1, 2, 4, 6, 10],
        skiprows=6,
        names=[
            "Country",
            "HDI",
            "Life expectancy at birth",
            "Expected years of schooling",
            "Gross national income (GNI) per capita",
        ],
    )

    le_dict = infos_pays.set_index("Country")["Life expectancy at birth"].to_dict()

    manual_life_exp = {
        "United Kingdom of Great Britain and Northern Ireland": 80.7422,
        "Turkey": 76.0324,
        "United States of America": 77.1982,
        "Iran, Islamic Republic of...": 73.8749,
        "Hong Kong (S.A.R.)": 85.4734,
        "Bolivia": 63.6304,
        "Czech Republic": 77.7283,
        "The former Yugoslav Republic of Macedonia": 73.8415,
        "Venezuela, Bolivarian Republic of...": 70.5536,
        "Taiwan": 78.2107,
        "South Korea": 73.2845,
        "Republic of Moldova": 68.8459,
        "Democratic Republic of the Congo": 63.5187,
        "United Republic of Tanzania": 66.2007,
        "Kosovo": None,
        "Nomadic": None,
        "Congo, Republic of the...": 63.5187,
        "Republic of Korea": 73.2845,
        "Swaziland": 57.0657,
        "Libyan Arab Jamahiriya": 71.9112,
        "Palestine": 73.4727,
        "Isle of Man": None,
        "Cape Verde": None,
    }

    le_dict.update(manual_life_exp)

    # Mapping
    df["LifeExpectancy"] = df["Country"].map(le_dict)

    return df


def add_expected_schooling(df, path_to_excel):
    """
    Adds the expected years of education to the DataFrame from an Excel file.

    Args:
        df (pd.DataFrame): The DataFrame containing a 'Country' column.
        path_to_excel (str): Path to Excel file containing data.

    Returns:
        pd.DataFrame: The DataFrame enriched with an 'ExpectedSchooling' column.
    """
    # Chargement des données
    infos_pays = pd.read_excel(
        path_to_excel,
        usecols=[1, 2, 4, 6, 10],
        skiprows=6,
        names=[
            "Country",
            "HDI",
            "Life expectancy at birth",
            "Expected years of schooling",
            "Gross national income (GNI) per capita",
        ],
    )

    eys_dict = infos_pays.set_index("Country")["Expected years of schooling"].to_dict()

    manual_schooling = {
        "United Kingdom of Great Britain and Northern Ireland": 17.30971909,
        "Turkey": 18.3382206,
        "United States of America": 16.28097916,
        "Iran, Islamic Republic of...": 14.61524963,
        "Hong Kong (S.A.R.)": 17.27816963,
        "Bolivia": 14.94697094,
        "Czech Republic": 16.21968079,
        "The former Yugoslav Republic of Macedonia": 13.62443234,
        "Venezuela, Bolivarian Republic of...": 12.81608,
        "Taiwan": 14.2361149,
        "South Korea": 10.78317,
        "Republic of Moldova": 14.43299961,
        "Democratic Republic of the Congo": 12.33081527,
        "United Republic of Tanzania": 9.221489906,
        "Kosovo": None,
        "Nomadic": None,
        "Congo, Republic of the...": 12.33081527,
        "Republic of Korea": 10.78317,
        "Swaziland": 13.74434586,
        "Libyan Arab Jamahiriya": 12.85428,
        "Palestine": 13.35801029,
        "Isle of Man": None,
        "Cape Verde": None,
    }

    eys_dict.update(manual_schooling)

    df["ExpectedSchooling"] = df["Country"].map(eys_dict)

    return df


def add_gni_per_capita(df, path_to_excel):
    """
    Adds gross national income (GNI) per capita to the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing a 'Country' column.
        path_to_excel (str): Path to Excel file containing data.

    Returns:
        pd.DataFrame: The DataFrame enriched with a 'GNIperCapita' column.
    """

    # Chargement des données
    infos_pays = pd.read_excel(
        path_to_excel,
        usecols=[1, 2, 4, 6, 10],
        skiprows=6,
        names=[
            "Country",
            "HDI",
            "Life expectancy at birth",
            "Expected years of schooling",
            "Gross national income (GNI) per capita",
        ],
    )

    gnipc_dict = infos_pays.set_index("Country")[
        "Gross national income (GNI) per capita"
    ].to_dict()

    manual_gni = {
        "United Kingdom of Great Britain and Northern Ireland": 45224.76564,
        "Turkey": 31032.80106,
        "United States of America": 64765.21509,
        "Iran, Islamic Republic of...": 13000.7117,
        "Hong Kong (S.A.R.)": 62606.8454,
        "Bolivia": 8111.190194,
        "Czech Republic": 38745.21386,
        "The former Yugoslav Republic of Macedonia": 15917.75283,
        "Venezuela, Bolivarian Republic of...": 4810.882621,
        "Taiwan": 17504.39969,
        "South Korea": None,
        "Republic of Moldova": 14875.33189,
        "Democratic Republic of the Congo": 2889.283521,
        "United Republic of Tanzania": 2664.329096,
        "Kosovo": None,
        "Nomadic": None,
        "Congo, Republic of the...": 2889.283521,
        "Republic of Korea": None,
        "Swaziland": 7678.591873,
        "Libyan Arab Jamahiriya": 15335.712,
        "Palestine": 6582.899416,
        "Isle of Man": None,
        "Cape Verde": None,
    }

    gnipc_dict.update(manual_gni)

    df["GNIperCapita"] = df["Country"].map(gnipc_dict)

    return df


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
        A list of column names to group by. The first column is used to compute subgroup
        percentages.
        For example: ["Gender", "EmployedCat"]

    count_col_name : str, optional
        Name of the column in the result that will contain the raw counts (default is "count").

    percent_col_name : str, optional
        Name of the column in the result that will contain the percentage values (default is
        "percentage").

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


def categorize_employment_status(
    df, column="Employed",
    new_col="EmployedCat",
    labels=["Sans emploi", "En emploi"]
):
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
