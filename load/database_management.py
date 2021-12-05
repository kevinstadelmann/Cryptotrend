"""This file handles the loading into the database part of the project

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.
https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
https://datatofish.com/pandas-dataframe-to-sql/
  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
# Module Imports
import mariadb
import sys
import pandas as pd


### load data into database ###

def load_twitter_bitcoin():
    df_tw = pd.read_csv("../data/stage/twitter_bitcoin_stage.csv")

    for index, row in df_tw.iterrows():
        cur.execute("INSERT INTO cip_project.twitter_bitcoin_stage (date,asset,count,percent_change,source,created_ts) VALUES(?,?,?,?,?,?)",
        (row.date, row.asset, df_tw.at[index ,'count'], row.percent_change, row.source, row.created_ts))



def load_coingecko():
    df_tw = pd.read_csv("../data/stage/coingecko_stage.csv")

    for index, row in df_tw.iterrows():
        cur.execute("INSERT INTO cip_project.coingecko_bitcoin_stage (date,name,market_cap,%_market_cap,"
                    "volume,%_volume,open,%_open,close,%_close,gain/loss,created_ts) VALUES(?,?,?,?,?,?)",
                    (row.date, row.name, row.market_cap, row.%_market_cap, row.volume, row.%_volume
                    row.open, row.%_open, row.close, row.%_close, row.gain/loss, row.created_ts))


try:
    # Connect to MariaDB
    conn = mariadb.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="cip_project",
        autocommit=True  # automatically commit SQL statements

    )
    # Get Cursor
    cur = conn.cursor()

    # Load data
    #load_twitter_bitcoin()


except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
