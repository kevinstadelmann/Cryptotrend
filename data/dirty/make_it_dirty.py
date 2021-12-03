"""
Insert random character, in random row, in a random column, randomly in a value
--> 10 impurities for 100 rows --> 1000 rows, around 20 impurities should be enough
Warnings 1: We INSERT an not delete, because if we delete, there is no way to correct/clean the impurities.
Warnings 2: We insert LETTERS and SPECIAL CHARACTER. Not numbers because we wouldn't if the modified number
is correct or not.

1098 rows & 6 columns
-> row index: [0:1097]
-> col index: [0:5]
"""
### IMPORT ###
import random
import string
import pandas as pd

### EXTRACT ###
gecko_data = pd.read_csv('../data/src/coingecko_src.csv', header=0)

### FUNCTION ###
lst_character = list(string.ascii_letters+string.punctuation)
len_lst = len(lst_character)
lst_impurities, lst_row_col, lst_before, lst_after = [], [], [], []

def make_it_dirty(df,n):
    for i in range(0,n+1):
        random_number = random.randint(0,len_lst-1)
        random_char = lst_character[random_number]
        row_len, col_len = df.shape
        random_row = random.randint(0, row_len - 1)
        random_col = random.randint(0, col_len - 1)
        random_value = str(df.iloc[random_row, random_col])  # if we want to insert a character, the value needs to be a str
        print('Before: ', random_value)
        value_len = len(random_value)
        i = random.randint(0, value_len-1)
        random_value_modified = random_value[:i]+random_char+random_value[i:]
        print('At position (row x column): ', random_row, 'x', random_col)
        print('Impurities: ', random_char)
        print('After: ', random_value_modified, '\n')
        df.iloc[random_row, random_col] = random_value_modified

        # Create a DataFrame with all those information
        lst_impurities.append(random_char)
        row_col = str(random_row) + ' x ' + str(random_col)
        lst_row_col.append(row_col)
        lst_before.append(random_value)
        lst_after.append(random_value_modified)
    data={'impurities':lst_impurities, 'row x column': lst_row_col, 'before': lst_before, 'after': lst_after}
    df_info=pd.DataFrame(data)
    return df, df_info

### MAKE IT DIRTY ###
# Part 1: apply dirty function #
# There is 1098 rows, around 20 impurities should be enough --> why not 30?
gecko_dirty, dirty_info = make_it_dirty(gecko_data, 30)

# Part 2: Input impurities manually (see actions in documentation) #
...

### EXPORT ###
gecko_dirty.to_csv('..data/dirty/coingecko_1_src_dirty.csv', index=False)
dirty_info.to_csv('..data/dirty/dirty_info_coingecko.csv', index=False)