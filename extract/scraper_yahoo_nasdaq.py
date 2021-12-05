####IMPORTS######

import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from datetime import datetime
import time
from pandas.tseries.offsets import BDay

#################
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
#################
###Defining Ticker, period (Time Frame) & Interval

ticker = '^IXIC'  ##Symbol for NASDAQ
interval = '1d'

# Due to the restriction that Yahoo Finance only display 100 rows
# so we define a function to deduct 100 days from the end time till we reach the total time frame needed

end = datetime.today()


def getStockData(endPeriod, businessDays):
    businessDaysSets = int(businessDays / 100)
    for y in range(businessDaysSets):
        end = endPeriod - BDay(y * 100 + (y))
        start = end - BDay(100)
        unixStart = int(time.mktime(start.timetuple()))
        unixEnd = int(time.mktime(end.timetuple()))

        ##URL From Yahoo Finance - Historical Data
        Hist_url = f'https://finance.yahoo.com/quote/{ticker}/history?period1={unixStart}&period2={unixEnd}&interval={interval}&filter=history&frequency=1d&includeAdjustedClose=true'

        ## Requesting URL & Scraping using BeautifulSoup
        r = requests.get(Hist_url, headers=headers)

        soup = BeautifulSoup(r.content, 'html.parser')

        Hist_table = soup.find('table', class_='W(100%) M(0)')

        ###Creating empty lists to add the scraped content:
        dates = []
        open_t = []
        high_t = []
        low_t = []
        close_t = []
        adjclose = []
        volume_t = []

        ###for loop to go through all rows in table & append to the list

        for line in Hist_table.find_all('tbody'):
            rows = line.find_all('tr')
            for row in rows:
                date = row.find('td', class_='Py(10px) Ta(start) Pend(10px)').text
                dates.append(date)
                open = row.find_all('td', class_='Py(10px) Pstart(10px)')[0].text
                open_t.append(open)
                high = row.find_all('td', class_='Py(10px) Pstart(10px)')[1].text
                high_t.append(high)
                low = row.find_all('td', class_='Py(10px) Pstart(10px)')[2].text
                low_t.append(low)
                close = row.find_all('td', class_='Py(10px) Pstart(10px)')[3].text
                close_t.append(close)
                adj_close = row.find_all('td', class_='Py(10px) Pstart(10px)')[4].text
                adjclose.append(adj_close)
                volume = row.find_all('td', class_='Py(10px) Pstart(10px)')[5].text
                volume_t.append(volume)
            data = {'symbol': ticker, 'date': dates, 'open': open_t, 'high': high_t, 'low': low_t, 'close': close_t,
                    'adjusted_close': adjclose, 'volume': volume_t}
            df = pd.DataFrame(data)
            print(df)
            saving_csv = '../data/src/yahoo_{}_src.csv'
            ##using format to add automatically add ticker used in the title
            ##And appending the data with new time frame into the csv file
            df.to_csv(saving_csv.format(ticker), mode='a', header=True, index=False)


getStockData(end, 1100)  ##reflecting on the number of days - years equivalent (2021-2018)


### TRANSFORM ###