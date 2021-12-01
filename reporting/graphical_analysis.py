import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

btc = pd.read_csv("BTC.csv")
twitter = pd.read_csv("twitter.csv")

#print(btc["Date"])
#print(twitter["Date"])

#plt.plot(twitter["Date"], btc["count"], label="Bitcoin Prize")
#plt.plot(btc["Date"], btc["Close"], label="Twitter Counts")
#plt.show()
#https://www.kdnuggets.com/2020/01/stock-market-forecasting-time-series-analysis.html
# See Table under: https://www.programiz.com/python-programming/datetime/strptime
# for more formating options
str1 = '3/1/2021'
str2 = '2021-01-03'
str3 = '1-03-21'

date_object1 = datetime.strptime(str1, '%d/%m/%Y')
date_object2 = datetime.strptime(str2, '%Y-%m-%d')
date_object3 = datetime.strptime(str3, '%m-%d-%y')

print(date_object1.date())
print(date_object2.date())
print(date_object3.date())

# code from HosHos
#graphical presentation

import numpy as np
import matplotlib.pyplot as plt
y_pos=np.arange(len(kw_list))
plt.barh(y_pos,finalAverageList,align='center',alpha=0.5)
plt.yticks(y_pos,kw_list)
plt.xlabel('Average popularity')
plt.show()

## Notice in the graph we use the more popular keyword for different cryptocurrencies
## so we use Bitcoin, Doge, Ethereum

kw_list = ["Bitcoin", "Doge", "Ethereum",] # list of keywords to get data

pytrends.build_payload(kw_list, cat=0, timeframe='2020-01-01 2020-12-31')

#1 Interest over Time

data = pytrends.interest_over_time()

print(data)

data = pytrends.interest_over_time()

data = data.drop(labels=['isPartial'],axis='columns')    #there’s a column named isPartial
data.to_csv('../data/search_trends.csv')

executionTime = (time.time() - startTime)
print('Execution time in sec.: ' + str(executionTime))

data = data.reset_index()

import plotly.express as px

fig = px.line(data, x="date", y=['Bitcoin', 'Doge', 'Ethereum'], title='Keyword Web Search Interest Over Time')
fig.show()

# this method will return historical data of the searched keyword from Google Trend
# according to the timeframe you have specified
# we can visualize the data collected by using the Plotly library
#

