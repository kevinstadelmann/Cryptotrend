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
import os
import sys
import pandas as pd

# load data into database


def load_coingecko_stage():
    try:
        df_tw = pd.read_csv("../data/stage/coingecko_stage.csv")

        for index, row in df_tw.iterrows():
            cur.execute("INSERT INTO cip_project.coingecko_stage (date,name,market_cap,perc_market_cap,"
                        "volume,perc_volume,open,perc_open,close,perc_close,gain_loss,time_stamps) "
                        "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (row.date, row.name, row.market_cap, row.perc_market_cap, row.volume, row.perc_volume,
                         row.open, row.perc_open, row.close, row.perc_close, row.gain_loss, row.time_stamps))
        print('Successfully load coingecko_stage!')
    except mariadb.Error as e:
        print(f"Error adding entry to database: {e}")


def load_coingecko_src():
    try:
        df_tw=pd.read_csv("../data/src/coingecko_src.csv")

        for index, row in df_tw.iterrows():
            cur.execute("INSERT INTO cip_project.original_coingecko (name, date,market_cap,"
                        "volume,open,close) VALUES(?,?,?,?,?,?)",
                        (row.name, row.date, row.market_cap, row.volume, row.open, row.close))
        print('Successfully load original_coingecko!')
    except mariadb.Error as e:
        print(f"Error adding entry to database: {e}")


# Connect to MariaDB
try:
    conn = mariadb.connect(
        user="admin",
        password="123",
        host="127.0.0.1",
        port=3306,
        database="cip_project",
        autocommit=True         #automatically commit SQL statements

    )
    # Get Cursor
    cur = conn.cursor()

    load_coingecko_src()
    load_coingecko_stage()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


