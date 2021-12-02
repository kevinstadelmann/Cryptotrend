"""graphical analysis of the data

Wrap it up and answer questions

"""
import pandas as pd
import matplotlib.pyplot as plt
#import pandas_profiling as pp


### loading and preparing data ###

df_twitter = pd.read_csv('../data/stage/twitter_bitcoin_stage.csv')
df_google = pd.read_csv('../data/stage/googletrend_bitcoin_stage.csv')
df_coingecko = pd.read_csv('../data/stage/coingecko_stage_kevin.csv')

# select timespan for analysis (2018-2021)
df_twitter = df_twitter[df_twitter.date.between('2020-02-01', '2021-11-01')]
#df_google = df_google[df_google.date.between('2020-02-01', '2021-11-01')]

# join data on date
merge_data = pd.merge(df_twitter[['date','count','percent_change']],
                      df_google[['date','interest_rate']],
                      how='inner', on='date')

merge_data = pd.merge(merge_data, df_coingecko[['date', 'close']],
                      how='inner', on='date')

# first graphical analysis

def first_analysis():
    fig, ax = plt.subplots()
    ax.plot(merge_data['count'], label='Twitter counts', color='y', linewidth=1.0)
    ax.plot(merge_data['close'], label='Valuation', color='b', linewidth=1.0)
    ax.set_xlabel('Time')  # Add an x-label to the axes.
    ax.set_ylabel('Values')
    ax.set_title("Simple Plot")
    ax.legend()

#first_analysis()
plt.show()

# Question 1
# Do cryptocurrencies depend on popularity?
# Correlation + Regression Analysis

# Question 2
# Do people invest in cryptocurrencies in opposition to stock market?
# Regression Analysis

# Question 3
# What is the future of cryptocurrencies?
# Logarithmic regression

