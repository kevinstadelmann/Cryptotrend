"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""

import pandas as pd
from datetime import datetime

### EXTRACT ###
df_btc = pd.read_csv('../data/twitter_bitcoin.csv')

### TRANSFORM ##

# add column name
df_btc.columns = ['day', 'count']

# remove counts which are not numeric
# https://newbedev.com/finding-non-numeric-rows-in-dataframe-in-pandas
# 1. Try to convert to numeric, if not, make nan-value
print(len(df_btc))
a = pd.to_numeric(df_btc['count'], errors='coerce')
idx = a.isna()
print(idx==True)
#print(df_btc[idx])
# 2. remove all nan-values
#df_btc.drop(df_btc[idx])
print(len(df_btc))


#print(df_btc['count'].applymap(lambda x: isinstance(x, (int, float))))

# remove duplicate
#df_concat.drop_duplicates('name')

# date is wrong, months need to increase by one
for i,row in df_btc.iterrows():

    var_date = str(row['day'])

    if var_date.count('/') == 2:
        #print(var_date)
        new_var_date = str(var_date.split('/', 2)[0] + "/" + str(int(var_date.split('/', 2)[1]) + 1) + "/" + var_date.split('/', 2)[2])
        df_btc.at[i,'day'] = new_var_date

# add percentual change from count-values on a daily basis

#for i,row in range(df_btc.iterrows():

    #if i > 1 and str(row['count'][i]).isnumeric() == True and str(row['count'][i-1]).isnumeric() == True:
    #    var_count1 = int(row['count'][i])
    #    var_count2 = int(row['count'][i-1])
    #    var_change = var_count2 // var_count1
    #    print(type(var_count2))

# remove duplicate
#df_concat.drop_duplicates('name')
# add column asset / source / created_ts
#df_btc['asset'] = "BTC"
#df_btc['source'] = "Twitter"
#df_btc['created_ts'] = datetime.now(tz=None)




#print(df_btc.dtypes)

### LOAD ###
