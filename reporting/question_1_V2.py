"""CSV handler for extracted Twitter data

Extracts data out of csv file, transforms it ... blabla

"""

# Question 1
# Do cryptocurrencies depend on popularity?
# Correlation + Regression Analysis

# https://www.askpython.com/python/examples/correlation-regression-analysis
https://datatofish.com/multiple-linear-regression-python/

# how correlate things are: https://www.youtube.com/watch?v=cxogUULzU9E&list=PLnSVMZC68_e667DFySPQwmsl-tNaVo8ED&index=7
# heatmap would be nice ;)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import seaborn as sns
import statsmodels.api as sm

### load prepared data
df_q1 = pd.read_csv('../data/merged/data_question_one.csv')
#df_q1['volume'] = df_q1['volume'] / 1000000
df_q1

def plot_bitcoin_twitter():

    # add linear regression line on scatter plot
    m, b = np.polyfit(df_q1['bitcoin_value'], df_q1['twitter_count'], 1)
    plt.plot(df_q1['bitcoin_value'], m * df_q1['bitcoin_value'] + b, color='red')

    plt.scatter(df_q1['bitcoin_value'], df_q1['twitter_count'], color='blue', s=5)
    plt.title('Bitcoin valuation vs. Twitter counts', fontsize=14)
    plt.xlabel('Bitcoin value', fontsize=10)
    plt.ylabel('Twitter counts', fontsize=10)
    plt.grid(True)
    plt.show()
#plot_bitcoin_twitter()

def plot_bitcoin_google():

    # add linear regression line on scatter plot
    m, b = np.polyfit(df_q1['bitcoin_value'], df_q1['interest_rate'], 1)
    plt.plot(df_q1['bitcoin_value'], m * df_q1['bitcoin_value'] + b, color='red')

    plt.scatter(df_q1['bitcoin_value'], df_q1['interest_rate'], color='blue', s=5)
    plt.title('Bitcoin valuation vs. Google interest rate', fontsize=14)
    plt.xlabel('Bitcoin value', fontsize=10)
    plt.ylabel('Google interest rate', fontsize=10)
    plt.grid(True)
    plt.show()

#plot_bitcoin_google()

def plot_bitcoin_volume():

    # add linear regression line on scatter plot
    m, b = np.polyfit(df_q1['bitcoin_value'], df_q1['volume'], 1)
    plt.plot(df_q1['bitcoin_value'], m * df_q1['bitcoin_value'] + b, color='red')

    plt.scatter(df_q1['bitcoin_value'], df_q1['volume'], color='blue', s=5)
    plt.title('Bitcoin valuation vs. volume', fontsize=14)
    plt.xlabel('Bitcoin value', fontsize=10)
    plt.ylabel('volume', fontsize=10)
    plt.grid(True)
    plt.show()

plot_bitcoin_volume()


def multiple_regression():

    X = df_q1[['volume', 'twitter_count']]  # here we have 2 variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
    Y = df_q1['bitcoin_value']

    # with sklearn
    regr = linear_model.LinearRegression()
    regr.fit(X, Y)

    print('Intercept: \n', regr.intercept_)
    print('Coefficients: \n', regr.coef_)

    # prediction with sklearn
    #New_Interest_Rate = 2.75
    #New_Unemployment_Rate = 5.3
    #print('Predicted Stock Index Price: \n', regr.predict([[New_Interest_Rate, New_Unemployment_Rate]]))

    # with statsmodels
    X = sm.add_constant(X)  # adding a constant

    model = sm.OLS(Y, X).fit()
    predictions = model.predict(X)

    print_model = model.summary()
    print(print_model)
#multiple_regression()


#Intercept:
# 0.19598202659276687
# Coefficients:
# interest_percent_change[-0.69204176
# twitter_percent_change 1.15324789]

#bitcoin_change = 0.19 + (-0.69 * interest_percen_change) + (1.15 * twitter_percent_change)

# Intercept:
#  -170.44687677552974
# Coefficients:
#  [3.54388994e+02 2.21079218e-01]