"""Merging stage data to answer project questions

Every question has its own data file with the joined data from the
different stage-files.

"""

import pandas as pd



### Question ONE ###
# Do cryptocurrencies depend on popularity?
# Correlation + Regression Analysis
def merge_data_question_one():

    # load needed stage files
    df_twitter = pd.read_csv('../data/stage/twitter_bitcoin_stage.csv')
    df_google = pd.read_csv('../data/stage/googletrend_bitcoin_stage.csv')
    df_coingecko = pd.read_csv('../data/stage/coingecko_stage.csv')

    # select time period for analysis (2018-2021)
    df_twitter = df_twitter[df_twitter.date.between('2018-10-01', '2021-11-01')]

    # rename columns to not have problems with join the different data
    # and to make them more meaningful later on
    df_twitter.rename(columns = {"percent_change": "twitter_percent_change"}, inplace = True)
    df_twitter.rename(columns={"count": "twitter_count"}, inplace=True)

    df_google.rename(columns = {"percent_change": "interest_percent_change"}, inplace = True)

    df_coingecko.rename(columns = {"%_close": "bitcoin_percent_change", }, inplace = True)
    df_coingecko.rename(columns={"close": "bitcoin_value"}, inplace=True)

    # join data on date and select necessary columns
    df_q1 = pd.merge(df_twitter[['date', 'twitter_count', 'twitter_percent_change']],
                          df_google[['date', 'interest_rate', 'interest_percent_change']],
                          how='inner', on='date')

    df_q1 = pd.merge(df_q1, df_coingecko[['date', 'bitcoin_value', 'bitcoin_percent_change', 'volume','%_volume']],
                          how='inner', on='date')

    # if there are still NA values, fill them with 0
    df_q1 = df_q1.fillna(0)
    #print(df_question_one)
    # safe to csv
    df_q1.to_csv('../data/merged/data_question_one.csv', index=False)
merge_data_question_one()



### Question TWO ###
# Do people invest in cryptocurrencies in opposition to stock market?
# Regression Analysis
def merge_data_question_two():

    # load needed stage files
    df_coingecko = pd.read_csv('../data/stage/coingecko_stage.csv', index_col=False)
    df_gold = pd.read_csv('../data/stage/yahoo_gold_stage.csv', index_col=False)
    df_nasdaq = pd.read_csv('../data/stage/yahoo_nasdaq_stage.csv', index_col=False)
    df_oil = pd.read_csv('../data/stage/yahoo_oil_stage.csv', index_col=False)

    # select time period for analysis (2018-2021)
    df_coingecko = df_coingecko[df_coingecko.date.between('2020-10-01', '2021-11-01')]

    # rename columns to not have problems with join the different data
    # and to make them more meaningful later on
    df_coingecko.rename(columns={"close": "bitcoin_value"}, inplace=True)
    df_gold.rename(columns={"close": "gold_value"}, inplace=True)
    df_nasdaq.rename(columns={"close": "nasdaq_value"}, inplace=True)
    df_oil.rename(columns={"close": "oil_value"}, inplace=True)

    # to plot the values so the history (last date) is on the left of the plots
    df_coingecko = df_coingecko.sort_values(by="date")

        # join data on date and select necessary columns
    df_q2 = pd.merge(df_coingecko[['date', 'bitcoin_value']],
                               df_gold[['date', 'gold_value']],
                               how='inner', on='date')
    df_q2 = pd.merge(df_q2,
                               df_nasdaq[['date', 'nasdaq_value']],
                               how='inner', on='date')

    df_q2 = pd.merge(df_q2,
                               df_oil[['date', 'oil_value']],
                               how='inner', on='date')


    # if there are still NA values, fill them with 0
    df_question_two = df_q2.fillna(0)

    # safe to csv
    df_q2.to_csv('../data/merged/data_question_two.csv', index=False)

    # if there are still NA values, fill them with 0
    df_q2 = df_q2.fillna(0)

    # safe to csv
    df_q2.to_csv('../data/merged/data_question_two.csv', index=False)


#merge_data_question_two()

### Question THREE ###
# Question 3
# What is the future of cryptocurrencies?
# Logarithmic regression

def merge_data_question_three():
    # load needed stage files
    df_q3 = pd.read_csv('../data/stage/coingecko_stage.csv', index_col=False)

    # remove non-necessary columns
    df_q3 = df_q3.drop(['name', 'time_stamps', '%_market_cap', 'volume', '%_volume', 'open', '%_open'], axis=1)

    # history left to right, oldest to newest
    df_q3 = df_q3.sort_values(by="date")

    # safe to csv
    df_q3.to_csv('../data/merged/data_question_three.csv', index=False)

merge_data_question_three()