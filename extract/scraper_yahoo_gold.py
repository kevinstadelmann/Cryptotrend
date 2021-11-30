####IMPORTS######

import bs4
import re
import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
from selenium import webdriver

#################
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
#################

###Defining Ticker, period (Time Frame) & Interval

ticker = 'GC=F'   ##Symbol for Gold
period1 = int(time.mktime(datetime.datetime(2018, 1, 1, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2021, 11, 1, 23, 59).timetuple()))
interval = '1d'

###URL From Yahoo Finance - Historical Data

Hist_url = f'https://finance.yahoo.com/quote/{ticker}/history?period1={period1}&period2={period2}&interval={interval}&filter=history&frequency=1d&includeAdjustedClose=true'

###Using Selenium & webdriver to scroll down the page as the website load content dynamically

driver = webdriver.Firefox()
driver.get(Hist_url)
driver.maximize_window()

#Scroll down till element is visible
#start_date=driver.find_element(By.xpath("/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/section/div[2]/table/tbody/tr[756]/td[1]/span")p
#driver.execute_script("arguments[0].scrollIntoView();", start_date)

#Scroll down by pixel
#driver.execute_script("window.scrollBy(0,5000)","")

#Scroll down page till end
driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

### Requesting URL & Scraping using BeautifulSoup

r = requests.get(Hist_url, headers=headers)

soup = BeautifulSoup(r.content, 'html.parser')

Hist_table = soup.find('table', class_='W(100%) M(0)')

### Scraping the table header
for header in Hist_table.find_all('thead'):
    t_date = header.find('th', class_= 'Ta(start) W(100px) Fw(400) Py(6px)').text
    t_open = header.find_all('th', class_= 'Fw(400) Py(6px)')[0].text
    t_high = header.find_all('th', class_='Fw(400) Py(6px)')[1].text
    t_low = header.find_all('th', class_='Fw(400) Py(6px)')[2].text
    t_close = header.find_all('th', class_='Fw(400) Py(6px)')[3].text
    t_adjclose = header.find_all('th', class_='Fw(400) Py(6px)')[4].text
    t_volume = header.find_all('th', class_='Fw(400) Py(6px)')[5].text
    print(t_date, t_open, t_high, t_low, t_close, t_adjclose, t_volume)


###Creating empty lists to add the scraped content:

dates=[]
open_t=[]
high_t=[]
low_t=[]
close_t=[]
adjclose=[]
volume_t=[]

###for loop to go through all rows in table & append to the list

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
    saving_csv = '../data/src/yahoo_{}_src.csv'
    df.to_csv(saving_csv.format(ticker), index=False)           ####using format to add automatically add ticker used in the title

### TRANSFORM ###
