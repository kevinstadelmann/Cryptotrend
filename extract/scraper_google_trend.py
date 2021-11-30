"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
import csv
from datetime import datetime
from datetime import timedelta
from pytrends.request import TrendReq
import pytrends
import pandas as pd
import time

### EXTRACT ###
str1 = '3/1/2021'
date_object1 = datetime.strptime(str1, '%d/%m/%Y')

startTime = time.time()

#Connect to google trends
pytrends = TrendReq(hl= 'en-US', tz=360)

# Build Payload
# list of keywords to get data
kw_list = ["bit coin", "Bitcoin", "BTC", "Etherium", 'ETH', 'Dogecoin', 'Doge',
           'Doge coin']

keywords = []  ## a list is created with a for loop as google trends has a max limit # of 5 keywords
cat = '0'  # for all categories
geo = ''  # worldwide by default
gprop = ''  # websearch by default

def check_trends():
    pytrends.build_payload(keywords,
                           cat,
                           timeframe='2020-01-01 2020-12-31')

    data = pytrends.interest_over_time()
    #print(data)

for kw in kw_list:
    keywords.append(kw)
    check_trends()
    keywords.pop()

##Notice it shows all keywords but they are not comperable.

##Here's a way to compare more keywords (5+) to create 2 separate lists w/ common keyword

kw_list1=['Bitcoin','BTC','Doge coin', 'Doge','Dogecoin']
kw_list2=['Bitcoin', 'bit coin' ,'Ethereum','ETH', 'Ethereum coin']

kw_list=kw_list1+kw_list2

pytrendsT=TrendReq(hl='en-US', tz=360)

pytrends1=TrendReq()
pytrends2=TrendReq()

#Build Payload with 2020 timeframe for 2 different lists

pytrends1.build_payload(kw_list1, cat, timeframe='2020-01-01 2020-12-31')
pytrends2.build_payload(kw_list2, cat, timeframe='2020-01-01 2020-12-31')

#Assigning dataframe for both lists

df1=pytrends1.interest_over_time()
df2=pytrends2.interest_over_time()

### TRANSFORM ###

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
#print(type(finalAverageList))
print(df1)
print(df2)
print(finalAverageList)

# save list to csv
#with open('../google_trends_src.csv', 'w') as f:
#    write = csv.writer(f)
#    for row in finalAverageList:
#        write.writerow(row)


### LOAD ###
