"""CSV handler for extracted Twitter data

Extracts data out of csv file, transforms it ... blabla

"""

# Question 3
# What is the future of cryptocurrencies?
# Logarithmic regression

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# load data
df_coingecko = pd.read_csv('../data/stage/coingecko_stage_kevin.csv')
df_bitcoin = df_coingecko[['date','close']]
df_bitcoin = df_bitcoin[df_bitcoin['close'] > 0]

def funct(x,p1,p2):
    return p1*np.log(x) + p2

xdata = np.array([x+1 for x in range(len(df_bitcoin))])
ydata = np.log(df_bitcoin['close'])

#print(xdata)
#print(ydata)
plt.semilogy(df_bitcoin['date'], df_bitcoin['close'])
popt, pcov = curve_fit(funct, ydata, ydata, p0 =(3.0,-10))
fittedydata = funct(xdata, popt[0], popt[1])
plt.plot(df_bitcoin['date'], np.exp(fittedydata))

plt.show()