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

from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
from function_scraper import from_name_to_web_ref
pd.options.display.float_format = '{:.2f}'.format


### EXTRACT ###

HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', \
            'Accept-Language': 'en-US, en;q=0.5'})

coin_name='Bitcoin'
start_date='2018-01-01'
end_date='2021-01-01'

def scrap_coingecko(coin_name,end_date,start_date):
    name_webref=from_name_to_web_ref()
    #print(name_webref)
    names, dates, market_cap, volume, open_, close = [],[],[],[],[],[]
    coin_ref=name_webref[coin_name]
    URL_HIST = 'https://www.coingecko.com{}/historical_data/usd?end_date={}&start_date={}#panel'
    response = requests.get(URL_HIST.format(coin_ref, end_date, start_date),headers=HEADERS)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find('table', {'class': 'table-striped'}).find('tbody').find_all('tr')
    for result in results:
        date = result.find('th', {'class': 'font-semibold text-center'}).get_text()
        dates.append(date)
        td = result.find_all('td', {'class': 'text-center'})
        value = []
        for item in td:
            data_str = item.get_text().strip('\n').strip('$').strip(' ').strip('$')
            try:
                data_float = float(data_str.replace(',', ''))
                value.append(data_float)
            except:
                value.append(data_str)
                print(data_str)
        names.append(coin_name)
        market_cap.append(value[0])
        volume.append(value[1])
        open_.append(value[2])
        close.append(value[3])
    data = {'Name': names, 'Date': dates, 'Market_Cap': market_cap, 'Volume': volume, 'Open': open_, 'Close': close}
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    data_crypto = df.set_index('Date')
    data_crypto.to_csv('../data/src/coingecko_src.csv', index=False)

    print(data_crypto.head())
    print(data_crypto.dtypes)
    print(data_crypto.shape)
    print('Done!')
    print('Finally')
    return data_crypto

### TRANSFORM ###

df=scrap_coingecko(coin_name,end_date,start_date)

time=df.index
market_cap=df['Market_Cap']
plt.plot(time, market_cap, label='Market Capitalisation')

plt.xlabel('Time')
plt.ylabel('Dollar')

plt.title("test plot")

plt.legend()

plt.show(block=True)
plt.interactive(False)
plt.show()
