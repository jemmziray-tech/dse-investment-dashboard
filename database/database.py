import sqlite3
import pandas as pd
import os


DATABASE_PATH = "data/database/dse_insight.db"


os.makedirs(
    "data/database",
    exist_ok=True
)


def create_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    return connection



def load_market_data():

    df = pd.read_csv(
        "data/processed/daily_market.csv"
    )

    return df



def save_to_database():

    df = load_market_data()

    conn = create_connection()


    df.to_sql(
        "daily_market",
        conn,
        if_exists="append",
        index=False
    )


    conn.close()


    print(
        "Market data stored successfully"
    )



if __name__ == "__main__":

    save_to_database()