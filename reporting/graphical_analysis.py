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

