import bs4
import re
from io import StringIO
import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import csv
import json


baseurl = 'https://finance.yahoo.com/quote/CL%3DF'

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}

r = requests.get('https://finance.yahoo.com/quote/CL%3DF?p=CL%3DF')
soup = BeautifulSoup(r.content, 'lxml')

result = soup.find('div', class_='Pos(r) Bgc($lv2BgColor) Mb(20px) Maw($maxModuleWidth) Miw($minGridWidth) Miw(ini)!--tab768 Miw(ini)!--tab1024 Mstart(a) Mend(a) Px(20px)').find_all('a')

urls = []

for link in result :
    urls.append('https://finance.yahoo.com'+link.get('href'))

#Hist_url = urls[2]                     ##need to figure out a way to select this based on 'history'
##################
##figure the date adjustment issues


#################
Hist_url = 'https://finance.yahoo.com/quote/CL%3DF/history?period1=1514764800&period2=1609459200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
##print(Hist_url)

r = requests.get(Hist_url, headers=headers)

soup = BeautifulSoup(r.content, 'html.parser')

Hist_table = soup.find('table', class_='W(100%) M(0)')

##print(Hist_table)
for header in Hist_table.find_all('thead'):
    t_date = header.find('th', class_= 'Ta(start) W(100px) Fw(400) Py(6px)').text
    t_open = header.find_all('th', class_= 'Fw(400) Py(6px)')[0].text
    t_high = header.find_all('th', class_='Fw(400) Py(6px)')[1].text
    t_low = header.find_all('th', class_='Fw(400) Py(6px)')[2].text
    t_close = header.find_all('th', class_='Fw(400) Py(6px)')[3].text
    t_adjclose = header.find_all('th', class_='Fw(400) Py(6px)')[4].text
    t_volume = header.find_all('th', class_='Fw(400) Py(6px)')[5].text
    print(t_date, t_open, t_high, t_low, t_close, t_adjclose, t_volume)


#def scraping(symbol):
symbol = 'CL=F'
dates=[]
open_t=[]
high_t=[]
low_t=[]
close_t=[]
adjclose=[]
volume_t=[]

for line in Hist_table.find_all('tbody'):
    rows = line.find_all('tr')
    for row in rows:
        date = row.find('td', class_ = 'Py(10px) Ta(start) Pend(10px)').text
        dates.append(date)
        open = row.find_all('td', class_ = 'Py(10px) Pstart(10px)')[0].text
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
    data = {'Symbol': symbol, 'Date': dates, 'Open': open_t, 'High': high_t, 'Low': low_t, 'Close': close_t,
                    'Adjusted Close': adjclose, 'Volume': volume_t}
    df = pd.DataFrame(data)
    print(df)
    df.to_csv(r'/home/student/Cloud/Owncloud/SyncVM (S2)/cryptotrendanalyzer/data/YahFin_Oil.csv')
    #saving_csv = r'YahFin_crypto_{}.csv'
    #df.to_csv(saving_csv.format(symbol))



    #return df
    #df.to_csv(r'YahFin_crypto.csv')

    #return data
        #print(date, open, high, low, close, adj_close, volume)                          ##stops after 144 rows

#name='Crude Oil'
#data={'Name':name,'Date':dates,'Open':open_t, 'High':high_t, 'Low':low_t,'Close':close_t, 'Adjusted Close':adjclose, 'Volume':volume_t}
#print(data)

#%%

##df=pd.DataFrame(data)
##df.head()