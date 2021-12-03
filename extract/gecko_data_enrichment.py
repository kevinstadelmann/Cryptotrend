"""
More meaningful data
"""

### IMPORT ###
import pandas as pd
from datetime import datetime
pd.options.display.float_format = '{:.2f}'.format
### EXTRACT ###
PATH='data/stage/coingecko_clean.csv'
abs_path='C:/Users/natr/Desktop/HSLU_S2/CIP/project/cryptotrendanalyzer/data/stage/'
gecko_df=pd.read_csv(abs_path+'coingecko_clean.csv', header=0)


### ENRICHMENT ###
# 1. Percentage in change (start from the bottom)
def percentage_in_change(df, col_names=('market_cap','volume','open','close')):
    for col in col_names:
        column=df[col]
        last_index=len(column)-1
        percent_column=[]
        while last_index>0:
            t_1=column.iloc[last_index]
            last_index-=1
            t=column.iloc[last_index]
            perc=round(((t-t_1)/t_1)*100,3)
            percent_column.insert(0,perc)
        percent_column.append(0)
        df["%_{}".format(col)] = percent_column
    return df

gecko_perc=percentage_in_change(gecko_df)

# 2. Time Stamps
gecko_perc['time_stamps']=datetime.now(tz=None).date()

gecko_perc.set_index('date', inplace=True)
print(gecko_perc)

gecko_perc.to_csv(abs_path+'coingecko_stage_nathan.csv',index=True)
print('DONE!')

