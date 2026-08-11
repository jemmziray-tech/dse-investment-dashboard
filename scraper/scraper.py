"""
DSE Insight - Market Data Scraper

Purpose:
    Collect raw market data from DSE sources
    and prepare it for processing.

Author:
    John Elifuraha Mziray
"""

import os
import logging
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


# -----------------------------
# Configuration
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

HISTORICAL_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "historical"
)


os.makedirs(
    HISTORICAL_DATA_PATH,
    exist_ok=True
)

# Change this when connecting to the real DSE endpoint
DSE_URL = "https://dse.co.tz"


# -----------------------------
# Logging setup
# -----------------------------

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# Request Handler
# -----------------------------

def fetch_page(url):
    """
    Download webpage content.
    """

    try:

        headers = {
            "User-Agent":
            "Mozilla/5.0"
        }


        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )


        response.raise_for_status()


        logging.info(
            f"Successfully fetched {url}"
        )


        return response.text


    except Exception as e:

        logging.error(
            f"Failed fetching {url}: {e}"
        )

        return None



# -----------------------------
# Extract Tables
# -----------------------------

def extract_tables(html):
    """
    Extract tables from HTML pages.
    """

    try:

        tables = pd.read_html(
            html
        )


        logging.info(
            f"{len(tables)} tables extracted"
        )


        return tables


    except Exception as e:

        logging.error(
            f"Table extraction failed: {e}"
        )

        return []



# -----------------------------
# Save Data in Time-Series
# -----------------------------

def save_dataframe(
        dataframe,
        filename
):
    
    # Add a 'Date' column if not present, to keep track of the time series
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Only inject date if it's not already there
    if 'Date' not in dataframe.columns:
        # Insert at the beginning
        dataframe.insert(0, 'Date', date_str)


    file_path = os.path.join(
        HISTORICAL_DATA_PATH,
        f"{filename}_historical.csv"
    )

    # If file exists, append without headers. If not, write with headers.
    file_exists = os.path.isfile(file_path)

    dataframe.to_csv(
        file_path,
        mode='a',
        index=False,
        header=not file_exists
    )


    logging.info(
        f"Appended to {file_path}"
    )


    return file_path



# -----------------------------
# Main Scraper
# -----------------------------

def run_scraper():

    print(
        "Starting DSE scraper..."
    )


    html = fetch_page(
        DSE_URL
    )


    if html is None:

        print(
            "Unable to retrieve data"
        )

        return



    tables = extract_tables(
        html
    )


    if len(tables) == 0:

        print(
            "No tables found"
        )

        return



    for index, table in enumerate(tables):

        filename = (
            f"dse_table_{index}"
        )


        path = save_dataframe(
            table,
            filename
        )


        print(
            f"Saved: {path}"
        )


    print(
        "Scraping completed successfully"
    )



# -----------------------------
# Execute
# -----------------------------

if __name__ == "__main__":

    run_scraper()