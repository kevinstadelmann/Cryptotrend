"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""

#Import libraries

import pytrends
import pandas as pd
import time
startTime = time.time()

#Connect to google trends

from pytrends.request import TrendReq
pytrends = TrendReq(hl= 'en-US', tz=360)

# Build Payload

kw_list = ["bit coin", "Bitcoin", "BTC", "Ethium", 'ETH', 'Dogecoin', 'Doge',
           'Doge coin']  # list of keywords to get data

keywords = []  ## a list is created with a for loop as google trends has a max limit # of 5 keywords
cat = '0'  # for all categories
geo = ''  # worldwide by default
gprop = ''  # websearch by default


def check_trends():
    pytrends.build_payload(keywords,
                           cat,
                           timeframe='2020-01-01 2020-12-31')

    data = pytrends.interest_over_time()
    print(data)


for kw in kw_list:
    keywords.append(kw)
    check_trends()
    keywords.pop()

##Notice it shows all keywords but they are not comperable.

##Here's a way to compare more keywords (5+) to create 2 separate lists w/ common keyword

kw_list1=['Bitcoin','BTC','Doge coin', 'Doge','Dogecoin']
kw_list2=['Bitcoin', 'bit coin' ,'Ethereum','ETH', 'Ethereum coin']

kw_list=kw_list1+kw_list2

pytrendsT=TrendReq(hl= 'en-US', tz=360)

pytrends1=TrendReq()
pytrends2=TrendReq()

#Build Payload with 2020 timeframe for 2 different lists

pytrends1.build_payload(kw_list1, cat, timeframe='2020-01-01 2020-12-31')
pytrends2.build_payload(kw_list2, cat, timeframe='2020-01-01 2020-12-31')

#Assigning dataframe for both lists

df1=pytrends1.interest_over_time()
df2=pytrends2.interest_over_time()

#Obtaining the mean value & creating a normalization factor with the common item in both lists (Bitcoin)

averageList1=[]
averageList2=[]
for item in kw_list1:
    averageList1.append(df1[item].mean().round(0))
for item in kw_list2:
    averageList2.append(df2[item].mean().round(0))

normalizationFactor=averageList1[0]/averageList2[0]

for i in range(len(averageList2)):
    normalisedVal=normalizationFactor*averageList2[i]
    averageList2[i]=normalisedVal.round(0)

#removing the common item Bitcoin from the second list so it's not duplicated

averageList2.pop(0)
kw_list2.pop(0)

kw_list=kw_list1+kw_list2

finalAverageList=averageList1+averageList2
print(finalAverageList)

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
data.to_csv('search_trends.csv')

executionTime = (time.time() - startTime)
print('Execution time in sec.: ' + str(executionTime))

data = data.reset_index()

import plotly.express as px

fig = px.line(data, x="date", y=['Bitcoin', 'Doge', 'Ethereum'], title='Keyword Web Search Interest Over Time')
fig.show()

# this method will return historical data of the searched keyword from Google Trend
# according to the timeframe you have specified
# we can visualize the data collected by using the Plotly library
###