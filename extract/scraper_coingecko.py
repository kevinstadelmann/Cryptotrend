"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
pd.options.display.float_format = '{:.2f}'.format
import matplotlib.pyplot as plt

coin_name='Bitcoin'
start_date='2018-01-01'
end_date='2021-01-01'

def scrap_coingecko(coin_name,end_date,start_date):
    #--------------------------------------------------------Create a function for this part---------------------------
    website = 'https://www.coingecko.com/en'
    response1 = requests.get(website)
    print(response1.status_code)
    soup1 = BeautifulSoup(response1.content, 'html.parser')
    web_table = soup1.find('table', {'class': 'table-scrollable'}).find('tbody').find_all('tr')
    dict_name = {}
    for row in web_table:
        name = row.find('a', {
            'class': 'tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between'}).get_text().strip('\n')
        web_ref = row.find('a', {'class': 'tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between'}).get(
            'href')
        dict_name[name] = web_ref
    #------------------------------------------------------------------------------------------------------------------
    names, dates, market_cap, volume, open_, close = [],[],[],[],[],[]
    website_historical = 'https://www.coingecko.com{}/historical_data/usd?end_date={}&start_date={}#panel'
    coin_ref=dict_name[coin_name]
    response = requests.get(website_historical.format(coin_ref, end_date, start_date))
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
    data_crypto.to_csv(r'C:\Users\natr\Desktop\HSLU_S2\CIP\project\CoinGecko_Scrap.csv')
    print(data_crypto.head())
    print(data_crypto.dtypes)
    print(data_crypto.shape)
    print('Done!')
    print('Bye bye...')
    return data_crypto


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
