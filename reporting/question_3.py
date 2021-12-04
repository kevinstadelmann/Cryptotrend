"""CSV handler for extracted Twitter data

Extracts data out of csv file, transforms it ... blabla
https://medium.datadriveninvestor.com/using-logarithmic-regression-to-predict-the-future-prices-of-bitcoin-and-ethereum-52f05e7b92b8
"""

# Question 3
# What is the future of cryptocurrencies?
# Logarithmic regression

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# load data
#df_coingecko = pd.read_csv('../data/stage/coingecko_stage_kevin.csv')
df_q3 = pd.read_csv('../data/merged/data_question_three.csv')
df_q3 = df_q3[['date','close']]
df_q3 = df_q3[df_q3['close'] > 0]
dates = df_q3['date']

def funct(x,p1,p2):
    return p1*np.log(x) + p2

ydata = np.log(df_q3['close'])
xdata = np.array([x+1 for x in range(len(df_q3))])
popt, pcov = curve_fit(funct, ydata, ydata, p0 =(3.0,-10))

fittedydata = funct(np.array([x for x in range(len(df_q3))]), popt[0], popt[1])

plt.semilogy(dates, df_q3['close'])
for i in range(-3,5):
    plt.fill_between(dates, np.exp(fittedydata + i -1), np.exp(fittedydata+1))

#plt.ylim(botton=1)
plt.set_yscale('linear')
plt.show()

#plt.plot(df_bitcoin['date'], np.exp(fittedydata))