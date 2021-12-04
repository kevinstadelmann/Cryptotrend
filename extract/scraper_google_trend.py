""" Google Trend API handler

Google Trend allows daily data for 90days periods. Because data is needed for

"""

import pandas as pd
from pytrends.request import TrendReq
import datetime as dt
import math
from datetime import timedelta

### EXTRACT ###

def scrap_googletrends():
    pytrends = TrendReq(hl='en-US', tz=360)

    #### build the playload
    kw_list = ["Bitcoin"]

    # define extracting period
    start_date = dt.datetime.strptime('2018-01-01', '%Y-%m-%d')
    end_date = dt.datetime.strptime('2021-12-01', '%Y-%m-%d')

    ### Building an array of 90d periods to receive google trend data with a one day resolution
    d90_periods = math.ceil( (end_date - start_date) / dt.timedelta(days=90))
    tmp_range = pd.date_range(start=start_date, periods= d90_periods + 1, freq= '90D')

    # make timeperiods
    index = 0
    date_ranges = []
    for i in tmp_range[:]:

        if index < int(len(tmp_range))-1:
            date_ranges.append(str(tmp_range[index].strftime('%Y-%m-%d')) + " " + str(tmp_range[index+1].strftime('%Y-%m-%d')))
        index += 1

    # initialization of the major data frame df_trends
    pytrends.build_payload(kw_list,timeframe=date_ranges[0])
    df_trends= pytrends.interest_over_time()

    #go trough other timespans
    for dates in date_ranges[1:]:

        common_date = dates.split(' ')[0]
        pytrends.build_payload(kw_list, timeframe=dates)
        tmp_df = pytrends.interest_over_time()
        multiplication_factor = df_trends.loc[common_date] / tmp_df.loc[common_date]
        df_trends = (pd.concat([df_trends, (tmp_df[1:] * multiplication_factor)]))

    df_trends.to_csv('../data/src/googletrend_bitcoin_src.csv', index=True)

### TRANSFORM ###

# load dirty data
df_trends = pd.read_csv('../data/dirty/googletrend_bitcoin_dirty.csv')

# remove column isPartial
df_trends = df_trends.drop(['isPartial'], axis=1)
# rename columnes
df_trends.columns = ['date', 'interest_rate']

# try to format the date
df_trends['date'] = pd.to_datetime(df_trends['date'], format='%Y-%m-%d', errors='coerce')
# try to format the interest_rate
df_trends['interest_rate'] = pd.to_numeric(df_trends['interest_rate'], errors='coerce')
#if not possible, drop entries
df_trends = df_trends.dropna()

# sort by date
df_trends = df_trends.sort_values(by="date", ascending=True)


# add percentual change from interest_rate on a daily basis
# skip first row, because there is no value to compare
for i,row in df_trends[1:].iterrows():

    dt_day1 = df_trends.loc[i, 'date']
    dt_day2 = df_trends.loc[i - 1, 'date']

    # exclude rows which are not successively with their date
    if dt_day1 + timedelta(days=-1) == dt_day2:
        var_count1 = df_trends.loc[i, 'interest_rate']
        var_count2 = df_trends.loc[i-1, 'interest_rate']
        df_trends.at[i,'percent_change'] = (var_count1 / var_count2)-1

    # if not successively, create a new entry with the mean of previous and next entry
    else:
        # take the left and right entries, surrounding the missing date
        idx1 = df_trends['date'].searchsorted(df_trends.loc[i-1, 'date'], side='left')
        idx2 = df_trends['date'].searchsorted(df_trends.loc[i-1, 'date'], side='right')

        # calculate the missing data
        var_day = df_trends.loc[idx1, 'date'] + timedelta(days=1)
        var_interest = (df_trends.loc[idx1, 'interest_rate'] + df_trends.loc[idx2, 'interest_rate']) / 2
        var_percent_change = (var_interest / df_trends.loc[idx1, 'interest_rate']) - 1

        # add the missing data
        df_trends = df_trends.append({'date': var_day, 'interest_rate': var_interest, 'percent_change': var_percent_change}, ignore_index=True)

        # order again by date
        df_trends = df_trends.sort_values(by="date", ascending=True)

        # reset index for additional missing data
        df_trends.reset_index(drop=True, inplace=True)

# safe cleaned file
df_trends.to_csv('../data/stage/googletrend_bitcoin_stage.csv', index=None)
