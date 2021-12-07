"""
Automated scraping coingecko.com
"""

### IMPORT ###
import pandas as pd
from scraper_coingecko import scrap_coingecko
from coingecko_enrichment import percentage_in_change
from datetime import datetime


def check_missing_values(df):
    col_len = df.shape[1]
    lst_row_col = []
    for col in range(0, col_len):
        for index, row in df.iterrows():
            if pd.isna(row[col]) or row[col] in ['N/A', 'NaN', 'nan', 'None', 'NULL', '-', '']:
                lst_row_col.append((index, col))
    return lst_row_col

def replace_missing_value_by_previous(df, lst_row_col):
    for pos in lst_row_col:
        row_n = pos[0]
        prev_row = row_n + 1
        prev_value = df.iloc[prev_row, pos[1]]
        print('Before: {}'.format(df.iloc[pos[0], pos[1]]))
        df.iloc[pos[0], pos[1]] = prev_value
        print('After: {}\n'.format(df.iloc[pos[0], pos[1]]))
    return df

def final_formating_nummeric(df):
    for col in df.columns:
        if col == 'date' or col == 'name':
            pass
        else:
            try:
                df[col] = pd.to_numeric(df[col], errors='raise')
                print('{}: OK!'.format(col))
            except ValueError as e:
                print('{}: Not OK!'.format(col))
                print(e)
    return df

def main():
    coin_name = input('Enter a cryptocurrency: ')
    start_date = input('Starting date (YYYY-MM-DD): ')
    end_date = input('Ending date (YYYY-MM-DD): ')
    try:
        df = scrap_coingecko(coin_name, end_date, start_date)
        df.columns = ['name', 'date', 'market_cap', 'volume', 'open', 'close']
        lst = check_missing_values(df)
        df = replace_missing_value_by_previous(df, lst)
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='ignore')
        df=final_formating_nummeric(df)
        df_enrich = percentage_in_change(df)
        price_diff = df['close'] - df['open']
        df_enrich.insert(10, 'gain/loss', price_diff)
        df_enrich['gain/loss'] = df['gain/loss'].astype(float).round(2)
        df_enrich['time_stamps'] = datetime.now(tz=None).date()
        df_enrich.set_index('date', inplace=True)
        df_enrich.to_csv('C:/Users/natr/Deskto/HSLU_S2/CIP/project/pycharm/'
                         'venv/personal_scraping/data/{}_data.csv'.format(coin_name), index=True)
        print('Done!')
    except KeyError:
        print("'{}' is not a cryptocurrency.".format(coin_name))
        print("Check the coin's name")
        print("Or try to change for 'Not popular'.")
        main()
    except AttributeError:
        print("Check the date format (YYYY-MM-DD) or date range.")
        main()


if __name__=='__main__':
    print("Welcome dear user!")
    print("This program will scrap data, clean and enrich data about cryptocurrency.")
    #condition=input("If you want to analyse specific coin, type 'Not popular' or press 'ENTER': ")
    main()
