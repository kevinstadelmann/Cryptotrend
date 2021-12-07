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
df_gold = pd.read_csv('../data/dirty/yahoo_gold_src_dirty.csv', header=None)

### TRANSFORM ###

### Assigning the first row as Column Headers & drop this row
df1_gold = df_gold.rename(columns=df_gold.iloc[0])
df2_gold = df1_gold.drop([0], axis=0)

### Remove values which are not numeric & convert to numeric, if not possible, make nan-value
#Any string or text to be replaced with Nan + replace comma so we can convert string to float
df2_gold['open'] = pd.to_numeric(df2_gold['open'].str.replace(',',''), errors='coerce')
df2_gold['high'] = pd.to_numeric(df2_gold['high'].str.replace(',',''), errors='coerce')
df2_gold['low'] = pd.to_numeric(df2_gold['low'].str.replace(',',''), errors='coerce')
df2_gold['close'] = pd.to_numeric(df2_gold['close'].str.replace(',',''), errors='coerce')
df2_gold['adjusted_close'] = pd.to_numeric(df2_gold['adjusted_close'].str.replace(',',''), errors='coerce')
df2_gold['volume'] = pd.to_numeric(df2_gold['volume'].str.replace(',',''), errors='coerce')

### Format Date
df2_gold['date'] = pd.to_datetime(df2_gold['date'], errors='coerce').dt.date

### Replacing NULL, NA, Missing with nan values to drop them
df2_gold.replace('NA', np.nan, inplace = True)
df2_gold.replace('NULL', np.nan, inplace = True)
df2_gold.replace('None', np.nan, inplace = True)

##Having NaN value in Volume doesn't affect the Dataframe
#so replace with 0 so it's not dropped
df2_gold["volume"] = df2_gold["volume"].fillna(0)

### Drop NaN-values
df2_gold = df2_gold.dropna()

### Remove duplicates
df2_gold = df2_gold.drop_duplicates()

### Remove any wrong info - Only info about Gold using Filter with symbol
df2_gold[df2_gold.symbol == 'GC=F']

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
    index_list.extend(outliers(df2_gold, value))
# Define a function called "remove" which returns a cleaned dataframe without outliers
def remove(df, ls):
    ls = sorted(set(ls))
    df = df.drop(ls)
    return df

df3_gold = remove(df2_gold, index_list)

##Change date from object to datetime64[ns]
df3_gold['date'] = pd.to_datetime(df3_gold['date'])

###Add missing dates w/ Index & Period range 'Daily'
groupby_day = df3_gold.groupby(pd.PeriodIndex(data=df3_gold.date, freq='D'))
results = groupby_day.sum()

idx = pd.period_range(min(df3_gold.date), max(df3_gold.date))
df4_gold = results.reindex(idx, fill_value="NaN")

##Replacing str "Nan" with missing values
df4_gold.replace('NaN', np.nan, inplace = True)

#Defining dates & reseting index
df4_gold.index.name = 'date'
df4_gold.reset_index(level=0, inplace = True)

###Check missing values in the dataset, column per column ###
def check_missing_values(df):
    col_len = df.shape[1]
    lst_row_col = []
    for col in range(0, col_len):
        for index, row in df.iterrows():
            if pd.isna(row[col]):
                lst_row_col.append((index, col))
    return lst_row_col

missing_values_position = check_missing_values(df4_gold)

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
is_there_missing_values = df4_gold['close'].isna().sum()

while is_there_missing_values > 0:
    df4_gold = replace_missing_value_by_previous(df4_gold, missing_values_position)
    missing_values_position = check_missing_values(df4_gold)
    is_there_missing_values = df4_gold['close'].isna().sum()

### Sort dataframe by date
df4_gold = df4_gold.sort_values(by="date")

##Reset Index
df4_gold.reset_index(drop=True, inplace=True)

### Add percentual change from count-values on a daily basis
# skip first row, because there is no value to compare
for i,row in df4_gold[1:].iterrows():

    dt_day1 = df4_gold.loc[i, 'date']
    dt_day2 = df4_gold.loc[i - 1, 'date']

    # exclude rows which are not successively with their date
    if dt_day1 + timedelta(days=-1) == dt_day2:
        var_value1 = df4_gold.loc[i, 'adjusted_close']
        var_value2 = df4_gold.loc[i-1, 'adjusted_close']
        df4_gold.at[i,'percent_change'] = (var_value1 / var_value2)-1

### Add column Name & source
df4_gold['name'] = "Gold"
df4_gold['source'] = "Yahoo Finance"


### Save cleaned file
df4_gold.to_csv('../data/stage/yahoo_gold_stage.csv', index=False)