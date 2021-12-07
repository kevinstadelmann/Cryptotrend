"""This python file to clean dirty CSV file from various impurities
"""

import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

### EXTRACT Dirty CSV File ###
df = pd.read_csv('../data/dirty/yahoo_nasdaq_src_dirty.csv', header=None)

### TRANSFORM ###

### Assigning the first row as Column Headers & drop this row
df1 = df.rename(columns=df.iloc[0])
df2 = df1.drop([0], axis=0)

### Remove values which are not numeric & convert to numeric, if not possible, make nan-value
#Any string or text to be replaced with Nan + replace comma so we can convert string to float
df2['open'] = pd.to_numeric(df2['open'].str.replace(',',''), errors='coerce')
df2['high'] = pd.to_numeric(df2['high'].str.replace(',',''), errors='coerce')
df2['low'] = pd.to_numeric(df2['low'].str.replace(',',''), errors='coerce')
df2['close'] = pd.to_numeric(df2['close'].str.replace(',',''), errors='coerce')
df2['adjusted_close'] = pd.to_numeric(df2['adjusted_close'].str.replace(',',''), errors='coerce')
df2['volume'] = pd.to_numeric(df2['volume'].str.replace(',',''), errors='coerce')

### Format Date
df2['date'] = pd.to_datetime(df2['date'], errors='coerce').dt.date

### Replacing NULL, NA, Missing with nan values to drop them
df2.replace('NA', np.nan, inplace = True)
df2.replace('NULL', np.nan, inplace = True)
df2.replace('None', np.nan, inplace = True)

##Having NaN value in Volume doesn't affect the Dataframe
#so replace with 0 so it's not dropped
df2["volume"] = df2["volume"].fillna(0)

### Drop NaN-values
df2 = df2.dropna()

### Remove duplicates
df2 = df2.drop_duplicates()

### Remove any wrong info - Only info about NASDAQ using Filter with symbol
df2[df2.symbol == '^IXIC']

###Remove Outliers
# Define a function called "outliers" which returns a list of index of outliers
# Using IQR = Q3-Q1   Interquantile Range
# +/- 1.5*IQR
def outliers(df, value):
    Q1 = df[value].quantile(0.25)
    Q3 = df[value].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    ls = df.index[(df[value] < lower_bound) | (df[value] > upper_bound)]
    return ls
# create an empty list to store the output indices from multiple columns
index_list = []
for value in ['open', 'high', 'low', 'close', 'adjusted_close']:
    index_list.extend(outliers(df2, value))
# Define a function called "remove" which returns a cleaned dataframe without outliers
def remove(df, ls):
    ls = sorted(set(ls))
    df = df.drop(ls)
    return df

df3 = remove(df2, index_list)

##Change date from object to datetime64[ns]
df3['date'] = pd.to_datetime(df3['date'])

###Add missing dates w/ Index & Period range 'Daily'
groupby_day = df3.groupby(pd.PeriodIndex(data=df3.date, freq='D'))
results = groupby_day.sum()

idx = pd.period_range(min(df3.date), max(df3.date))
df4 = results.reindex(idx, fill_value="NaN")

##Replacing str "Nan" with missing values
df4.replace('NaN', np.nan, inplace = True)

#Defining dates & reseting index
df4.index.name = 'date'
df4.reset_index(level=0, inplace = True)

###Check missing values in the dataset, column per column ###
def check_missing_values(df):
    col_len = df.shape[1]
    lst_row_col = []
    for col in range(0, col_len):
        for index, row in df.iterrows():
            if pd.isna(row[col]):
                lst_row_col.append((index, col))
    return lst_row_col

missing_values_position = check_missing_values(df4)

### Replace missing values
def replace_missing_value_by_previous(df, lst_row_col):
    for pos in lst_row_col:
        row_n = pos[0]
        prev_row = row_n - 1
        prev_value = df.iloc[prev_row, pos[1]]
        df.iloc[pos[0], pos[1]] = prev_value
    return df

### Using a while loop to go through all rows
#since we have consecutive rows with missing data
is_there_missing_values = df4['close'].isna().sum()

while is_there_missing_values > 0:
    df4 = replace_missing_value_by_previous(df4, missing_values_position)
    missing_values_position = check_missing_values(df4)
    is_there_missing_values = df4['close'].isna().sum()

### Sort dataframe by date
df4 = df4.sort_values(by="date")

##Reset Index
df4.reset_index(drop=True, inplace=True)

### Add percentual change from count-values on a daily basis
# skip first row, because there is no value to compare
for i,row in df4[1:].iterrows():

    dt_day1 = df4.loc[i, 'date']
    dt_day2 = df4.loc[i - 1, 'date']

    # exclude rows which are not successively with their date
    if dt_day1 + timedelta(days=-1) == dt_day2:
        var_value1 = df4.loc[i, 'adjusted_close']
        var_value2 = df4.loc[i-1, 'adjusted_close']
        df4.at[i,'percent_change'] = (var_value1 / var_value2)-1

### Add column Name & source
df4['name'] = "NASDAQ"
df4['source'] = "Yahoo Finance"


### Save cleaned file
df4.to_csv('../data/stage/yahoo_nasdaq_stage.csv', index=False)