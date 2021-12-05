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

# format column date as date and make sure it is the index (for plotting needed)
df_q3['date'] = pd.to_datetime(df_q3['date'], format='%Y-%m-%d')
df_q3.set_index(['date'],inplace=True)

def graphical_overview():

    fig, ax = plt.subplots()

    ax.plot(df_q3['close'], color='r', linewidth=0.8)
    ax.set_yscale('log')
    ax.set_xlabel('Time')
    ax.set_ylabel('Bitcoin value')
    ax.set_title("Graphical analysis: Bitcoin value over time")
    plt.show()

graphical_overview()

# regression logarithmic fit
def bitcoin_logarithmic_regression():
    def funct(x,p1,p2):
        return p1*np.log(x) + p2

    xdata = np.array([x+1 for x in range(len(df_q3))])
    ydata = np.log(df_q3['close'])

    popt, pcov = curve_fit(funct, xdata, ydata, p0 =(3.0,-10))

    fittedydata = funct(np.array([x for x in range(len(df_q3))]), popt[0], popt[1])

    plt.semilogy(dates, df_q3['close'])
    for i in range(-3,5):
        plt.fill_between(dates, np.exp(fittedydata + i -1), np.exp(fittedydata+1))

    #plt.ylim(botton=1)
    plt.show()

    #plt.plot(df_bitcoin['date'], np.exp(fittedydata))
bitcoin_logarithmic_regression()