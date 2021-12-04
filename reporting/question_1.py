"""CSV handler for extracted Twitter data

Extracts data out of csv file, transforms it ... blabla

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
import seaborn as sns

### load prepared data
df_q1 = pd.read_csv('../data/merged/data_question_one.csv')


def graphical_analysis():
    # Method to plot the bitcoin valuation together with the google trend and twitter count data.

    # multiply interest by 1000 to make it visible in the graphical analysis
    df_q1['interest_rate'] = df_q1['interest_rate'] * 1000
    df_q1['volume'] = df_q1['volume'] / 1000000

    fig, ax = plt.subplots()
    ax.plot(df_q1['twitter_count'], label='Twitter counts', color='y', linewidth=1.0)
    ax.plot(df_q1['bitcoin_value'], label='Bitcoin value', color='r', linewidth=1.0)
    ax.plot(df_q1['interest_rate'], label='Google interest rate', color='b', linewidth=1.0)
    ax.plot(df_q1['volume'], label='Volume', color='g', linewidth=1.0)
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    ax.set_title("Graphical analysis: Popularity impact on Bitcoin valuation")
    ax.legend()
    plt.show()

graphical_analysis()

def corr_popularity_bitcoin():
    # https://www.askpython.com/python/examples/correlation-regression-analysis
    numeric_col = ['bitcoin_percent_change', 'interest_percent_change', 'twitter_percent_change']

    # Using Correlation analysis to depict the relationship between the numeric/continuous data variables
    corr = df_q1.loc[:, numeric_col].corr()
    print(corr)

#corr_popularity_bitcoin()

def multiple_regression():
    var_dependent = df_q1[['twitter_percent_change', 'interest_percent_change']].values
    var_independent = df_q1[['bitcoin_percent_change']].values

    regr = linear_model.LinearRegression()
    regr.fit(var_dependent, var_independent)

    df_q1.reset_index(drop=True, inplace=True)
    print(df_q1)
    for i,row in df_q1.iterrows():
        var_interest = df_q1.loc[i, 'interest_percent_change']
        var_count = df_q1.loc[i, 'twitter_percent_change']
        btc_predicted = int(regr.predict([[var_count, var_interest]]))

        df_q1.at[i, 'predicted_bitcoin_valuation'] = btc_predicted
    print(df_q1)
#multiple_regression()


# predict bitcoin valuation with popularity
# compare it graphically
def graphical_analysis_predicted_bitcoin():
    # Method to plot the bitcoin valuation together with the google trend and twitter count data.

    multiple_regression()

    # multiply interest by 1000 to make it visible in the graphical analysis
    #merge_data['interest_rate'] = merge_data['interest_rate'] * 1000

    fig, ax = plt.subplots()
    ax.plot(df_q1['predicted_bitcoin_valuation'], label='Valuation predicted', color='y', linewidth=1.0)
    ax.plot(df_q1['close'], label='Valuation', color='r', linewidth=1.0)
    ax.set_xlabel('Time')  # Add an x-label to the axes.
    ax.set_ylabel('Values')
    ax.set_title("Graphical analysis: Predicted Bitcoin price by popularity")
    ax.legend()
    plt.show()


#graphical_analysis()
#graphical_analysis_predicted_bitcoin()
