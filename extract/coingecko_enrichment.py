"""
More meaningful data
"""

### IMPORT ###
import pandas as pd
import numpy as np
from datetime import datetime

pd.options.display.float_format = '{:.2f}'.format
### EXTRACT ###
PATH = '../data/stage/'
abs_path = 'C:/Users/natr/Desktop/HSLU_S2/CIP/project/cryptotrendanalyzer/data/stage/'
gecko_df = pd.read_csv(PATH + 'coingecko_clean.csv', header=0)


### ENRICHMENT ###
# 1. Percentage in change (start from the bottom)
def percentage_in_change(df, col_names=('market_cap', 'volume', 'open', 'close')):
    for col in col_names:
        column = df[col]
        last_index = len(column) - 1  # index start at 0
        percent_column = []
        while last_index > 0:
            last_index -= 1         # the last element will be 0, it has no element to be compared with
            t = column.iloc[last_index]
            t_1 = column.iloc[last_index+1]  # compared with the element before (bigger is the index, later is the date)
            if t_1==0:                         # some column ('volume') has a lot of 0 at the beginning (division by 0)
                percent_column.insert(0, 0)
            else:
                perc = round(((t - t_1) / t_1), 5)
                percent_column.insert(0, perc)
        percent_column.append(0)
        index_no = df.columns.get_loc(col)
        df.insert(index_no + 1, 'perc_{}'.format(col), percent_column)
    return df


gecko_enrich = percentage_in_change(gecko_df)

# 2. Price Gain/Loss
price_diff = gecko_df['close'] - gecko_df['open']
gecko_enrich.insert(10, 'gain_loss', price_diff)
gecko_enrich['gain_loss'] = gecko_df['gain_loss'].astype(float).round(4)

# 3. Time Stamps
gecko_enrich['time_stamps'] = datetime.now(tz=None).date()

gecko_enrich.set_index('date', inplace=True)
print(gecko_enrich)

gecko_enrich.to_csv(PATH + 'coingecko_stage.csv', index=True)
print('DONE!')
