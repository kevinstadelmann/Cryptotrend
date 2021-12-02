"""
Let's clean this mess!
"""

### IMPORT ###
import pandas as pd
import numpy as np
from datetime import datetime
import datetime as dt
import matplotlib.pyplot as plt

### EXTRACT ###
dirty_gecko = pd.read_csv('../data/dirty/coingecko_dirty_part2.csv')

### CLEANING ###

## Part 1: Manual correction (visual impurities) ##
print(dirty_gecko.head())
print(dirty_gecko.shape)
# 1. delete the first column (double index)
dirty_gecko.drop(dirty_gecko.columns[0], axis=1, inplace=True)

# 2. delete the first raw and set the correct index
dirty_gecko.drop(0,inplace=True)
df_1=dirty_gecko
df_1.columns=['name','date','market_cap','volume','open','close']

# check output and save the modification in a new DataFrame
print(df_1.head())
print(df_1.shape)


## Part 2:Impurities detection ##
# 1. Scroll each row in each column
# 2. Detect the type of the column (numeric vs string)
# 3. Detect impurities
def detect_impurities_basic(df):
    row_len, col_len = df.shape
    nested_dict = {}
    for col in range(0, col_len):
        count_num, count_str = 0, 0
        row_num, row_num_str = [], []
        col_name = {}
        for row in range(0, row_len):
            item = df.iloc[row, col]
            try:
                if isinstance(float(item), float) or isinstance(int(item), int):
                    count_num += 1
                    row_num.append(row)
            except ValueError:
                count_str += 1
                row_num_str.append(row)
        if count_num > count_str:
            type = 'numeric'
            col_name['type'] = type
            col_name['string_impurities:(num_row)'] = row_num_str
            lst_impurities = []
            for row in col_name['string_impurities:(num_row)']:
                item = df.iloc[row, col]
                lst_impurities.append(item)
            col_name['string_impurities:(item)'] = lst_impurities
        else:
            type = 'string'
            col_name['type'] = type
            col_name['numeric_impurities:(num_row)'] = row_num
            lst_impurities = []
            for row in col_name['numeric_impurities:(num_row)']:
                item = df.iloc[row, col]
                lst_impurities.append(item)
            col_name['numeric_impurities:(item)'] = lst_impurities
        nested_dict['col_{}'.format(col)] = col_name
    for dict in nested_dict:
        print('Information about {}:\n{}'.format(dict, nested_dict[dict]))
    return nested_dict


dict_info = detect_impurities_basic(df_1)


## Part 3: Now we notice some character were inserted in numbers. Let's clean that! ##
# 1. Select only the column with type integer or float
# 2. Select only string impurities
# 3. Apply a cleaning algorithm
def clean_string_impurities(df, nested_dictionary):
    col_num = 0
    for dict in nested_dictionary:
        if nested_dictionary[dict]['type'] == 'numeric':
            for row in nested_dictionary[dict]['string_impurities:(num_row)']:
                item = df.iloc[row, col_num]
                print('Before: ', item)
                if item in ['N/A', 'NaN', 'nan', 'None', 'NULL', '-', '']:
                    df.iloc[row, col_num] = np.nan  # If NaN value, apply same value for nan value
                    print('After: ', df.iloc[row, col_num])
                else:
                    lst_char = []
                    for char in item:
                        try:
                            int_char = str(int(char))
                            lst_char.append(int_char)
                        except ValueError:
                            if char == '.':  # Be careful with the dot, in case of a float number
                                lst_char.append(char)
                            else:
                                pass
                    character = ''.join(lst_char)
                    print('After: ', character)
                    df.iloc[row, col_num] = character
        else:
            pass
        col_num += 1
    return df


df_2 = clean_string_impurities(df_1, dict_info)

# Check with the function 'detect_column_type_and_impurities()', if we reduced the number of impurities.
# As we can see, we cleaned all the impurities in the numeric column
dict_info = detect_impurities_basic(df_2)


## Part 4.1: Clean string columns (Apply only to this  dataset)##
# 1. Clean column 'Name', apply the same name to the all column to make sure we have the same format
def format_coin_name(df, coin_name):
    count = 0
    row_len, col_len = df.shape
    for row in range(0, row_len):
        if df.iloc[row, 0] == coin_name:
            pass
        else:
            count += 1
            df.iloc[row, 0] = coin_name
    print('\nSolved {} mistakes in the column name.\n'.format(count))
    return df


df_3 = format_coin_name(df_2, 'Bitcoin')


## Part 4.2: Format the date column
# 2. Check date format (so we can see potential typos or different format)
def check_format_date(df,column_date_name):
    row=0
    lst_ValueError, lst_exception = [], []
    for date in df[column_date_name]:
        try:
            date_time = datetime.strptime(date, '%Y-%m-%d')
            df.iloc[row,1] = date_time
        except ValueError:
            print('row:{}, date: {}'.format(row, date))
            lst_ValueError.append(row)
        except:
            print('row:{}, date: {}'.format(row, date))
            lst_exception.append(row)
        row += 1
    return df, lst_ValueError, lst_exception


df_4, ValuesError, exceptions=check_format_date(df_3,'date')
print(ValuesError)
print(exceptions)   #No exceptions
# 2.1 Correct typos
# a. We want the format yyyy-mm-dd. So we need a total of 8 digits and two '-'. Let's rebuilt the date
def correct_date_typo(df,lst_ValueError):
    lst_except=[]
    for row in lst_ValueError:
        date=df.iloc[row,1]
        lst_char = []
        for char in date:
            try:
                int_char = str(int(char))
                lst_char.append(int_char)
            except ValueError:
                if char == '-':
                    lst_char.append(char)
                else:
                    pass
        date_without_typo = ''.join(lst_char)
        try:
            date_time = datetime.strptime(date_without_typo, '%Y-%m-%d')
            df.iloc[row, 1] = date_time
            print('Before: {} // After: {}'.format(date, df.iloc[row, 1]))
        except ValueError:
            lst_except.append(row)
    return df, lst_except

df_5, lst_except=correct_date_typo(df_4,ValuesError)
lst_except.extend(exceptions)
print(lst_except)
for row in lst_except:
    print('row: {}, date: {}'.format(row, df_5.iloc[row,1]))

# 2.2 Manual cleaning, handling different date format
df_5.iloc[4,1]='2021-10-28'
df_5.iloc[38,1]='2021-09-24'
df_5.iloc[47,1]='2021-09-15'
print(df_5)
# 2.3 Apply same format
df_5['date'] = pd.to_datetime(df_5['date'], format='%Y-%m-%d', errors='ignore')


## Part 5:Check missing values in the dataset, column per column ##
def check_missing_values(df):
    col_len = df.shape[1]
    lst_row_col = []
    for col in range(0, col_len):
        for index, row in df.iterrows():
            if pd.isna(row[col]):
                lst_row_col.append((index-1, col))
    return lst_row_col


missing_values_position = check_missing_values(df_5)
print(missing_values_position)

# 2. Relace missing values
def replace_missing_value_by_previous(df, lst_row_col):
    for pos in lst_row_col:
        row_n = pos[0]
        prev_row = row_n + 1
        prev_value = df.iloc[prev_row, pos[1]]
        print('Before: {}'.format(df.iloc[pos[0], pos[1]]))
        df.iloc[pos[0], pos[1]] = prev_value
        print('After: {}\n'.format(df.iloc[pos[0], pos[1]]))
    return df

df_6=replace_missing_value_by_previous(df_5, missing_values_position)

missing_values_position = check_missing_values(df_6)
print(missing_values_position)


# Remove duplicates
df_7=df_6.drop_duplicates()
before=df_6.shape[0]
after=df_7.shape[0]
print('{} duplicates removed!'.format(before-after))

def final_formating_nummeric(df):
    for col in df.columns:
        if col=='date' or col=='name':
            pass
        else:
            try:
                df[col] = pd.to_numeric(df[col], errors='raise')
                print('{}: OK!'.format(col))
            except ValueError as e:
                print(e)
                print('{}: Not OK!'.format(col))
    return df


df_clean=final_formating_nummeric(df_7)
print(df_clean.dtypes)

df_date_index=df_clean.set_index('date')

#Final: Plotting each column to notice any outliner (fake entry)!
def plotting_df(df,lst_numeric_col):
    time=df.index
    for col in lst_numeric_col:
        y=df[col]
        plt.plot(time, y, label=col)
        plt.xlabel('Time')
        plt.ylabel(col)
        plt.title("Test plot ({})".format(col), fontsize=18)
        plt.show(block=True)
        plt.interactive(False)
        plt.show()


lst_numeric_col=['market_cap', 'volume', 'open', 'close']
#plotting_df(df_date_index,lst_numeric_col)

# Correct that by hand, because machine are not able (yet!) to evaluate such decision.
max_market_cap=df_clean['market_cap'].max()
row_max_market=df_clean.index[df_clean['market_cap'] == max_market_cap].tolist()[0]
print('Outlier: [market_cap]\nmax: {} (row: {})'.format(max_market_cap,row_max_market))
prev_value_max=df_clean.at[row_max_market+1,'market_cap']
df_clean.at[row_max_market,'market_cap']=prev_value_max
print('New value (use previous value): {}\n'.format(prev_value_max))

min_open=df_clean['open'].min()
row_min_open=df_clean.index[df_clean['open'] == min_open].tolist()[0]
print('Outlier: [open]\nmin: {} (row: {})'.format(min_open,row_min_open))
prev_value_min=df_clean.at[row_min_open+1,'open']
df_clean.at[row_min_open,'open']=prev_value_min
print('New value min (use previous value): {}\n'.format(prev_value_min))


max_close=df_clean['close'].max()
row_max_close=df_clean.index[df_clean['close'] == max_close].tolist()[0]
min_close=df_clean['close'].min()
row_min_close=df_clean.index[df_clean['close'] == min_close].tolist()[0]
print('Outlier: [close]\nmax: {} (row: {})'.format(max_close,row_max_close,min_close,row_min_close))
prev_value_max=df_clean.at[row_max_close+1,'close']
df_clean.at[row_max_close,'close']=prev_value_max
prev_value_min=df_clean.at[row_min_close+1,'close']
df_clean.at[row_min_close,'close']=prev_value_min
print('New value max (use previous value): {}'.format(prev_value_max))
print('New value min (use previous value): {}\n'.format(prev_value_min))


df_date_index2=df_clean.set_index('date')
plotting_df(df_date_index2, lst_numeric_col)
df_date_index2.to_csv('../data/stage/coingecko_clean_2013_2021.csv', index=False)
print('DONE!')