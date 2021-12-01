import pandas as pd
from pytrends.request import TrendReq
import datetime as dt
import math

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

df_trends = pd.read_csv('../data/dirty/googletrend_bitcoin_dirty.csv')

# remove column isPartial
df_trends = df_trends.drop(['isPartial'], axis=1)
# rename column names
df_trends.columns = ['date', 'interest_rate']

# safe cleaned file
df_trends.to_csv('../data/stage/googletrend_bitcoin_stage.csv', index=None)

