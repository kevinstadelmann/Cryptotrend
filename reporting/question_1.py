"""CSV handler for extracted Twitter data

Extracts data out of csv file, transforms it ... blabla
# https://www.askpython.com/python/examples/correlation-regression-analysis
https://datatofish.com/multiple-linear-regression-python/

# how correlate things are: https://www.youtube.com/watch?v=cxogUULzU9E&list=PLnSVMZC68_e667DFySPQwmsl-tNaVo8ED&index=7
# heatmap would be nice ;)

"""

# Question 1
# Do cryptocurrencies depend on popularity?
# Correlation + Regression Analysis

# https://www.askpython.com/python/examples/correlation-regression-analysis
#https://datatofish.com/multiple-linear-regression-python/
# heatmap would be nice ;)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import matplotlib.dates as mdates
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm


### load prepared data
df_q1 = pd.read_csv('../data/merged/data_question_one.csv')

# format column date as date and make sure it is the index (for plotting needed)
df_q1['date'] = pd.to_datetime(df_q1['date'], format='%Y-%m-%d')
df_q1.set_index(['date'],inplace=True)

#df_q1 = df_q1[df_q1['twitter_count'] > 0]
#df_q1 = df_q1[df_q1['bitcoin_value'] > 0]
#df_q1 = df_q1[df_q1['interest_rate'] > 0]



def graphical_overview():
    # Method to plot the bitcoin valuation together with the google trend and twitter count data.

    # Display volume in Billion USD
    df_q1['volume'] = df_q1['volume'] / 100000

    # smooth data to make it more readable in plot
    df_q1['twitter_count'] = df_q1['twitter_count'].rolling(30).sum() / 30
    #df_q1['bitcoin_value'] = df_q1['bitcoin_value'].rolling(30).sum() / 30
    df_q1['volume'] = df_q1['volume'].rolling(30).sum() / 30

    fig, ax = plt.subplots()

    # add leftside y-axis
    ax.plot(df_q1['twitter_count'], label='Twitter counts (smoothed)', color='g', linewidth=0.5)
    ax.plot(df_q1['bitcoin_value'], label='Bitcoin value in USD', color='r', linewidth=1.5)
    ax.plot(df_q1['volume'], label='24h volume in USD Millions', color='y', linewidth=1.0)

    # add right-side y-axis
    ax2 = ax.twinx()
    ax2.plot(df_q1['interest_rate'], color='b', linewidth=0.5)
    ax2.set_ylabel('Google Trend Index', color='b')

    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    ax.set_title("Graphical analysis: Popularity impact on Bitcoin valuation")
    ax.legend()
    plt.show()

graphical_overview()

def plot_bitcoin_twitter_regression():

    # define regression
    var_y = df_q1.loc[:, 'bitcoin_value'].values.reshape(-1, 1) # values converts it into a numpy array
    var_x = df_q1.loc[:, 'twitter_count'].values.reshape(-1, 1) # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()                       # create object for the class
    linear_regressor.fit(var_x, var_y)                          # perform linear regression
    var_y_predicted = linear_regressor.predict(var_x)           # make predictions

    # create and format plot
    plt.scatter(var_x, var_y,color='blue', s=5)
    plt.plot(var_x, var_y_predicted, color='red', label="Linear Regression")
    plt.title('Bitcoin value vs. Twitter count', fontsize=14)
    plt.ylabel('Bitcoin value', fontsize=10)
    plt.xlabel('Twitter counts', fontsize=10)
    plt.grid(True)
    plt.legend()
    plt.show()

#plot_bitcoin_twitter_regression()

def plot_bitcoin_google_regression():

    # define regression
    var_y = df_q1.loc[:, 'bitcoin_value'].values.reshape(-1, 1) # values converts it into a numpy array
    var_x = df_q1.loc[:, 'interest_rate'].values.reshape(-1, 1) # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()                       # create object for the class
    linear_regressor.fit(var_x, var_y)                          # perform linear regression
    var_y_predicted = linear_regressor.predict(var_x)           # make predictions

    # create and format plot
    plt.scatter(var_x, var_y,color='blue', s=5)
    plt.plot(var_x, var_y_predicted, color='red', label="Linear Regression")
    plt.title('Bitcoin value vs. Google Trend Index', fontsize=14)
    plt.ylabel('Bitcoin value', fontsize=10)
    plt.xlabel('Google Trend Index', fontsize=10)
    plt.grid(True)
    plt.legend()
    plt.show()

#plot_bitcoin_google_regression()

def plot_bitcoin_volume_regression():
    # Display volume in Billion USD
    df_q1['volume'] = df_q1['volume'] / 1000000000

    # define regression
    var_y = df_q1.loc[:, 'bitcoin_value'].values.reshape(-1, 1) # values converts it into a numpy array
    var_x = df_q1.loc[:, 'volume'].values.reshape(-1, 1)        # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()                       # create object for the class
    linear_regressor.fit(var_x, var_y)                          # perform linear regression
    var_y_predicted = linear_regressor.predict(var_x)           # make predictions

    # create and format plot
    plt.scatter(var_x, var_y,color='blue', s=5)
    plt.plot(var_x, var_y_predicted, color='red', label="Linear Regression")
    plt.title('Bitcoin value vs. 24h Volume', fontsize=14)
    plt.ylabel('Bitcoin value', fontsize=10)
    plt.xlabel('24h Volume in Billion USD', fontsize=10)
    plt.grid(True)
    plt.legend()
    plt.show()

#plot_bitcoin_volume_regression()

def corr_popularity_bitcoin():
    # https://www.askpython.com/python/examples/correlation-regression-analysis
    numeric_col = ['bitcoin_percent_change', 'interest_percent_change', 'twitter_percent_change']

    # Using Correlation analysis to depict the relationship between the numeric/continuous data variables
    corr = df_q1.loc[:, numeric_col].corr()
    print(corr)

#corr_popularity_bitcoin()

def multiple_regression():
    # Display volume in Billion USD
    df_q1['volume'] = df_q1['volume'] / 1000000000

    X = df_q1[['volume', 'twitter_count', 'interest_rate']]  # here we have 2 variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
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
    #print(predictions)

    df_q1['predicted_bitcoin_valuation'] = predictions
    #print(df_q1)
    #print_model = model.summary()
    #print(print_model)
#multiple_regression_v2()

# predict bitcoin valuation with popularity
# compare it graphically
def graphical_analysis_predicted_bitcoin():
    # Method to plot the bitcoin valuation together with the google trend and twitter count data.

    multiple_regression()

    # smoother for the predicted bitcoin price
    #df_q1['predicted_bitcoin_valuation'] = df_q1['predicted_bitcoin_valuation'].rolling(7).sum() / 7
    #df_q1['bitcoin_value'] = df_q1['bitcoin_value'].rolling(7).sum() / 7

    # multiply interest by 1000 to make it visible in the graphical analysis
    #merge_data['interest_rate'] = merge_data['interest_rate'] * 1000

    fig, ax = plt.subplots()
    ax.plot(df_q1['predicted_bitcoin_valuation'], label='Predicted Bitcoin value', color='b', linewidth=0.8)
    ax.plot(df_q1['bitcoin_value'], label='Bitcoin value', color='r', linewidth=1.0)
    ax.set_xlabel('Time')  # Add an x-label to the axes.
    ax.set_ylabel('Value in USD')
    ax.set_title("Graphical analysis: Bitcoin value vs. predicted Bitcoin value by popularity")
    ax.legend()
    plt.show()

#multiple_regression()
#graphical_analysis()
graphical_analysis_predicted_bitcoin()