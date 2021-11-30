"""CSV handler for extracted Twitter data

Extracts data out of csv file, transforms it ... blabla

"""

import pandas as pd
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

### EXTRACT ###
df_btc = pd.read_csv('../data/twitter_bitcoin_src.csv', header=None)

### TRANSFORM ###

# add column name
df_btc.columns = ['date', 'count']

# remove counts which are not numeric and dates which are not dates
# 1. Try to convert to numeric/date, if not possible, make nan-value
df_btc['count'] = pd.to_numeric(df_btc['count'], errors='coerce')
df_btc['date'] = pd.to_datetime(df_btc['date'], format='%d/%m/%Y', errors='coerce').dt.date

# 2. drop nan-values
df_btc = df_btc.dropna()

# remove duplicates
df_btc = df_btc.drop_duplicates()

# date is wrong, months need to increase by one
for i,row in df_btc.iterrows():
    df_btc.at[i, 'date'] = df_btc.at[i, 'date'] + relativedelta(months=1)

# sort dataframe by date
df_btc = df_btc.sort_values(by="date")

# reset index
df_btc.reset_index(drop=True, inplace=True)

# add percentual change from count-values on a daily basis
# skip first row, because there is no value to compare
for i,row in df_btc[1:].iterrows():

    dt_day1 = df_btc.loc[i, 'date']
    dt_day2 = df_btc.loc[i - 1, 'date']

    # exclude rows which are not successively with their date
    if dt_day1 + timedelta(days=-1) == dt_day2:
        var_count1 = df_btc.loc[i, 'count']
        var_count2 = df_btc.loc[i-1, 'count']
        df_btc.at[i,'percent_change'] = (var_count1 / var_count2)-1

# add column asset / source / created_ts
df_btc['asset'] = "BTC"
df_btc['source'] = "Twitter"
df_btc['created_ts'] = datetime.now(tz=None)

print(df_btc[['date','count','percent_change']])

# save cleaned file
df_btc.to_csv('../data/twitter_bitcoin_stage.csv', index=False)

### LOAD ###
