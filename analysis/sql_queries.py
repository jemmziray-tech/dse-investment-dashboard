import sqlite3
import pandas as pd


DATABASE_PATH = "data/database/dse_insight.db"


def connect_db():
    return sqlite3.connect(
        DATABASE_PATH
    )


# -----------------------------
# Top Gainers
# -----------------------------

def top_gainers(limit=5):

    conn = connect_db()

    query = f"""
    SELECT
        Symbol,
        Close,
        Change,
        Volume
    FROM daily_market

    ORDER BY Change DESC

    LIMIT {limit};
    """


    df = pd.read_sql(
        query,
        conn
    )

    conn.close()

    return df



# -----------------------------
# Top Losers
# -----------------------------

def top_losers(limit=5):

    conn = connect_db()


    query = f"""
    SELECT
        Symbol,
        Close,
        Change,
        Volume

    FROM daily_market

    ORDER BY Change ASC

    LIMIT {limit};
    """


    df = pd.read_sql(
        query,
        conn
    )


    conn.close()

    return df




# -----------------------------
# Highest Volume
# -----------------------------

def highest_volume(limit=5):

    conn = connect_db()


    query = f"""
    SELECT
        Symbol,
        Volume,
        Close

    FROM daily_market

    ORDER BY Volume DESC

    LIMIT {limit};
    """


    df = pd.read_sql(
        query,
        conn
    )


    conn.close()

    return df




# -----------------------------
# Largest Companies
# -----------------------------

def largest_companies(limit=5):

    conn = connect_db()


    query = f"""
    SELECT
        Symbol,
        "MCAP (TZS 'B)" AS Market_Cap

    FROM daily_market

    ORDER BY Market_Cap DESC

    LIMIT {limit};
    """


    df = pd.read_sql(
        query,
        conn
    )


    conn.close()

    return df




# -----------------------------
# Company Search
# -----------------------------

def company_details(symbol):

    conn = connect_db()


    query = """
    SELECT *
    FROM daily_market

    WHERE Symbol = ?
    """


    df = pd.read_sql(
        query,
        conn,
        params=(symbol.upper(),)
    )


    conn.close()

    return df




# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    print("\nTOP GAINERS")
    print(top_gainers())


    print("\nTOP LOSERS")
    print(top_losers())


    print("\nHIGHEST VOLUME")
    print(highest_volume())


    print("\nLARGEST COMPANIES")
    print(largest_companies())


    print("\nCRDB DETAILS")
    print(company_details("CRDB"))