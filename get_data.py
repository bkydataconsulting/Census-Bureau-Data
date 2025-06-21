import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("d806bbf255019a46722f2234180a716c1bdef532")

def get_population_by_state():
    url = "https://api.census.gov/data/2022/acs/acs5"
    params = {
        "get": "NAME,B01003_001E",  # State Name, Total Population
        "for": "state:*",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from Census API")

    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df.rename(columns={"B01003_001E": "Population"}, inplace=True)
    df["Population"] = df["Population"].astype(int)
    return df.sort_values(by="Population", ascending=False)

def get_median_income_by_state():
    """
    Fetches the median household income for each state from the US Census API.
    Returns a DataFrame sorted by income (highest to lowest).
    """
    url = "https://api.census.gov/data/2022/acs/acs5"
    params = {
        "get": "NAME,B19013_001E",  # State Name, Median Household Income
        "for": "state:*",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from Census API")

    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    df.rename(columns={"B19013_001E": "Median_Income"}, inplace=True)
    # Some states may have missing or null values, so we use pd.to_numeric with errors='coerce'
    df["Median_Income"] = pd.to_numeric(df["Median_Income"], errors='coerce')
    return df.sort_values(by="Median_Income", ascending=False)

def get_median_income_by_zip():
    """
    Fetches the median household income and population for each ZIP Code Tabulation Area (ZCTA) from the US Census API.
    Returns a DataFrame sorted by income (highest to lowest).
    Note: ZCTAs are the Census Bureau's approximation of ZIP codes.
    """
    url = "https://api.census.gov/data/2022/acs/acs5"
    params = {
        # Get ZCTA Name, Median Household Income, and Total Population
        "get": "NAME,B19013_001E,B01003_001E",
        "for": "zip code tabulation area:*",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from Census API")

    data = response.json()
    df = pd.DataFrame(data[1:], columns=data[0])
    # Clean up the ZIP code column to only show the 5-digit code
    df["ZIP_Code"] = df["NAME"].str.replace("ZCTA5 ", "", regex=False)
    df.rename(columns={"B19013_001E": "Median_Income", "B01003_001E": "Population"}, inplace=True)
    # Convert columns to numeric, handling missing values
    df["Median_Income"] = pd.to_numeric(df["Median_Income"], errors='coerce')
    df["Population"] = pd.to_numeric(df["Population"], errors='coerce')
    # Select only the relevant columns for display
    return df[["ZIP_Code", "Median_Income", "Population"]].sort_values(by="Median_Income", ascending=False)