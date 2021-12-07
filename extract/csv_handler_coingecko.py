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
dirty_gecko = pd.read_csv('../data/dirty/coingecko_src_dirty.csv', header=0)

### CLEANING ###

## Part 1: Manual correction (visual impurities, open as a DataFrame in the consule) ##
print(dirty_gecko.head())
print(dirty_gecko.shape)
df_1 = dirty_gecko

# IGNORE (due to loading source file in mariadb, this function outdated)
# First we need to get rid of the dollar sign, the '\n' and replace the ',', so we can transform the number as float
def first_cleaning(df):
    for col in df.columns:
        row = 0
        for item in df[col]:
            try:
                clean_item = item.strip('\n').strip('$').strip(' ').strip('$').strip('\n')
                try:
                    number_item=float(clean_item.replace(',', ''))
                    df.loc[row,col]=number_item
                except ValueError:
                    df.loc[row, col] = clean_item
            except AttributeError:
                pass
            row += 1
    return df


df_2=df_1
# First column formatting, numeric, string, date --> Not possible due to impurities
# This function will be used at the end to confirm that the columns are in the right data type
def formating_column(df):
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='raise')
            print('{}: OK!'.format(col))
        except ValueError as e:
            print('{}: Not OK!'.format(col))
            print(e)
            try:
                df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='raise')
            except ValueError as e:
                print(e)


formating_column(df_2)

print('\n' * 2)


## Part 2:Impurities detection ##
# 1. Scroll each row in each column
# 2. Detect the type of the column (numeric vs string)
# 3. Detect impurities
# Input: DataFrame
# Output: Dictionary with information about 1) column type 2) row impurities 3) impurities
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


dict_info = detect_impurities_basic(df_2)

print('\n' * 2)


## Part 3: Now we notice some character were inserted in numbers. Let's clean that! ##
# 1. Select only the column with type numeric
# 2. Select only string impurities
# 3. Apply a cleaning algorithm
# Input: DataFrame and the dictionary from the function 'detect_impurities_basic()'
# Output: DataFrame
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


df_3 = clean_string_impurities(df_2, dict_info)
print('\n' * 2)
# Check with the function 'detect_column_type_and_impurities()', if we reduced the number of impurities.
dict_info = detect_impurities_basic(df_3)
print('\n' * 2)

# As we can see, there is still one impurity that the function couldn't solve, so we will do it by hand
# We are lucky on this one because the dots are at the same place, but let say it was 274.9.4 which dot is the right one
# So by precaution, we will take the previous value.
prev_value=df_3.iloc[2306,4]
df_3.iloc[2305,4]=prev_value

dict_info=detect_impurities_basic(df_3)
# Now we got rid of all the impurities
print('\n' * 2)


## Part 4.1: Clean string columns (Apply only to this  dataset)##
# That will also clean the impurities inserted in the column 'name'
# 1. Clean column 'Name', apply the same name to the all column to make sure we have the same format
# Input: DataFrame and coin_name (the one used in 'scraper_coingecko.py')
# Output: print statement with number of correction made
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


df_4 = format_coin_name(df_3, 'Bitcoin')

print('\n' * 2)


## Part 4.2: Format the date column
# 2. Check date format (so we can see potential typos or different format)
# Input: DataFrame and the name of the date column (so we can access the column without errors)
# Output: DataFrame and 2 list (list 1: row number of error with typos, list 2: row number error with
# exceptions like nan value)
def check_format_date(df, column_date_name):
    row = 0
    lst_ValueError, lst_exception = [], []
    for date in df[column_date_name]:
        try:
            date_time = datetime.strptime(date, '%Y-%m-%d')
            df.iloc[row, 1] = date_time
        except ValueError:
            print('row:{}, date: {}'.format(row, date))
            lst_ValueError.append(row)
        except:
            print('row:{}, date: {}'.format(row, date))
            lst_exception.append(row)
        row += 1
    return df, lst_ValueError, lst_exception


df_5, ValuesError, exceptions = check_format_date(df_4, 'date')
print(ValuesError)
print(exceptions)


# 2.1 Correct typos
# a. We want the format yyyy-mm-dd. So we need a total of 8 digits and two '-'. Let's rebuilt the date
# Input: DataFrame, list of typos error (so we can correct the typo at the row indicated in the previous function)
# Output: DataFrame, list of exceptions (the function couldn't correct for some reasons)
def correct_date_typo(df, lst_ValueError):
    lst_except = []
    for row in lst_ValueError:
        date = df.iloc[row, 1]
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


df_6, lst_except = correct_date_typo(df_5, ValuesError)
lst_except.extend(exceptions)      # Extend the list of exceptions (with row number) so we can manually correct the date
print(lst_except)
for row in lst_except:
    print('row: {}, date: {}'.format(row, df_6.iloc[row, 1]))

# 2.2 Manual cleaning, handling different date format
df_6.iloc[4, 1] = '2021-10-28'
df_6.iloc[38, 1] = '2021-09-24'
df_6.iloc[47, 1] = '2021-09-15'
# Deal manually with the missing date at row 449
# This can be extremely problematic if it's at the end of a month (30 or 31 or 28 in February)
# There is a way to correct this missing values with pandas.to_datetime() when it is set up as a column index,
# but I judge that it was not necessary for just one missing date.
prev_date = df_5.iloc[450, 1]
print(prev_date)
df_6.iloc[449, 1] = '2020-08-09'

# 2.3 Apply same format
df_6['date'] = pd.to_datetime(df_5['date'], format='%Y-%m-%d', errors='ignore')


## Part 5:Check missing values in the dataset, column per column ##
# Input: DataFrame
# Output: list of tuples (index_row, index_column) where missing values are
def check_missing_values(df):
    col_len = df.shape[1]
    lst_row_col = []
    for col in range(0, col_len):
        for index, row in df.iterrows():
            if pd.isna(row[col]):
                lst_row_col.append((index, col))
    return lst_row_col


missing_values_position = check_missing_values(df_5)
print(missing_values_position)


# 2. Relace missing values
# Input: DataFrame and list of missining values locations as tuples from the 'check_missing_values()'
# Output: DataFrame
def replace_missing_value_by_previous(df, lst_row_col):
    for pos in lst_row_col:
        row_n = pos[0]
        prev_row = row_n + 1
        prev_value = df.iloc[prev_row, pos[1]]
        print('Before: {}'.format(df.iloc[pos[0], pos[1]]))
        df.iloc[pos[0], pos[1]] = prev_value
        print('After: {}\n'.format(df.iloc[pos[0], pos[1]]))
    return df


df_7 = replace_missing_value_by_previous(df_6, missing_values_position)

missing_values_position = check_missing_values(df_7)
print(missing_values_position)

# Remove duplicates
df_8 = df_7.drop_duplicates()
before = df_7.shape[0]
after = df_8.shape[0]
print('{} duplicates removed!'.format(before - after))


def final_formating_nummeric(df):
    for col in df.columns:
        if col == 'date' or col == 'name':
            pass
        else:
            try:
                df[col] = pd.to_numeric(df[col], errors='raise')
                print('{}: OK!'.format(col))
            except ValueError as e:
                print('{}: Not OK!'.format(col))
                print(e)
    return df


df_clean = final_formating_nummeric(df_8)
print(df_clean.dtypes)

df_date_index = df_clean.set_index('date')


# Final: Plotting each column to notice any outliers (fake entry)!
# Input: DataFrame, and list of column names where values are numeric
def plotting_df(df, lst_numeric_col):
    time = df.index
    for col in lst_numeric_col:
        y = df[col]
        plt.plot(time, y, label=col)
        plt.xlabel('Time')
        plt.ylabel(col)
        plt.title("Test plot ({})".format(col), fontsize=18)
        plt.show(block=True)
        plt.interactive(False)
        plt.show()


lst_numeric_col = ['market_cap', 'volume', 'open', 'close']
plotting_df(df_date_index, lst_numeric_col)

# Correct that by hand, because machine are not able (yet!) to decide/quantify if a value is outlier or not.
outlier = True
if outlier == True:
    max_market_cap = df_clean['market_cap'].max()
    row_max_market = df_clean.index[df_clean['market_cap'] == max_market_cap].tolist()[0]
    print('Outlier: [market_cap]\nmax: {} (row: {})'.format(max_market_cap, row_max_market))
    prev_value_max = df_clean.at[row_max_market + 1, 'market_cap']
    df_clean.at[row_max_market, 'market_cap'] = prev_value_max
    print('New value (use previous value): {}\n'.format(prev_value_max))

    min_open = df_clean['open'].min()
    row_min_open = df_clean.index[df_clean['open'] == min_open].tolist()[0]
    print('Outlier: [open]\nmin: {} (row: {})'.format(min_open, row_min_open))
    prev_value_min = df_clean.at[row_min_open + 1, 'open']
    df_clean.at[row_min_open, 'open'] = prev_value_min
    print('New value min (use previous value): {}\n'.format(prev_value_min))

    min_close = df_clean['close'].min()
    row_min_close = df_clean.index[df_clean['close'] == min_close].tolist()[0]
    print('Outlier: [close]\nmin: {} (row: {})'.format(min_close, row_min_close))
    prev_value_min = df_clean.at[row_min_close + 1, 'close']
    df_clean.at[row_min_close, 'close'] = prev_value_min

    print('New value min (use previous value): {}\n'.format(prev_value_min))
else:
    pass

df_date_index2 = df_clean.set_index('date')
plotting_df(df_date_index2, lst_numeric_col)
df_date_index2.to_csv('../data/stage/coingecko_clean.csv', index=True)
print('DONE!')
