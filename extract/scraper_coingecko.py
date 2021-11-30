"""Scrap Data about cryptocurrencies from coingecko.com.

This function take as input:
    - coin_name: The name of the cryptocurrency you want to analyze
    - start_date: The starting date of the period you want to analyze
    - end_date: The ending date of the period you want to analyze

The program goes first on the main page where it scraps all the name of the cryptocurrencies,
and store the name in a dictionary with the webpage reference. So when the user input coin_name,
the program check if this name exist on the webpage and then use its web reference to access historical data.
The output is a clean dataframe exported as a CSV-file.
"""

### IMPORT ###
from bs4 import BeautifulSoup
import requests
import pandas as pd
from function_scraper import from_name_to_web_ref

pd.options.display.float_format = '{:.2f}'.format

### EXTRACT ###

HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})


def scrap_coingecko(coin_name, end_date, start_date):
    # Use the function from 'function scraper.py' to get the dictionary with the first 100 coin name with their web
    # reference
    name_webref = from_name_to_web_ref()
    coin_ref = name_webref[coin_name]

    # Access the URL with the historical data for the selected coin
    URL_HIST = 'https://www.coingecko.com{}/historical_data/usd?end_date={}&start_date={}#panel'
    response_hist = requests.get(URL_HIST.format(coin_ref, end_date, start_date), headers=HEADERS)
    print('URL Historical Data: ',response_hist.status_code)
    soup = BeautifulSoup(response_hist.content, 'html.parser')

    # Get the data in the table from the HTML script
    names, dates, market_cap, volume, open_, close = [], [], [], [], [], []
    table = soup.find('table', {'class': 'table-striped'})
    rows = table.find('tbody').find_all('tr')
    count = 0
    for row in rows:
        count += 1
        date = row.find('th', {'class': 'font-semibold text-center'}).get_text()
        dates.append(date)
        td = row.find_all('td', {'class': 'text-center'})
        value = []
        for item in td:
            data_str = item.get_text().strip('\n').strip('$').strip(' ').strip('$')

            # Exception: if a N/A value or a number cannot be transform as float (display which number is not a number)
            try:
                data_float = float(data_str.replace(',', ''))
                value.append(data_float)
            except:
                value.append(data_str)
                print('At row: ', count)
                print('The value is not a number: ', data_str)
        names.append(coin_name)
        market_cap.append(value[0])
        volume.append(value[1])
        open_.append(value[2])
        close.append(value[3])

    # Create column name from the header in the HTML script
    lst_head = []
    header = table.find('thead').find('tr').find_all('th', {'class': 'text-center'})
    for head in header:
        lst_head.append(head.get_text())

    # Create a dictionary for all the data with the corresponding header, then transform into a Pandas DataFrame,
    # then export as a CSV file
    data = {'Name': names, lst_head[0]: dates, lst_head[1]: market_cap, lst_head[2]: volume, lst_head[3]: open_,
            lst_head[4]: close}
    data_crypto = pd.DataFrame(data)
    data_crypto.to_csv('../data/src/coingecko_src.csv', index=False)

    # Checking if the DataFrame is correctly outputted
    print(data_crypto.head())
    print(data_crypto.dtypes)
    print(data_crypto.shape)
    if count == data_crypto.shape[0]:
        print('Done!')
    else:
        print('Different number of rows, something happened!')
    return data_crypto


# Selected value
coin_name = 'Bitcoin'
start_date = '2018-01-01'
end_date = '2021-01-01'

df = scrap_coingecko(coin_name, end_date, start_date)
