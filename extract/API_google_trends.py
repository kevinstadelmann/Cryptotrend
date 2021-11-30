"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""

###IMPORT###
import pytrends
import pandas as pd
import time
from pytrends.request import TrendReq
from pytrends import dailydata

# connect to google
pytrends = TrendReq(hl='en-US', tz=360)

# build payload
kw_list = ["machine learning"] # list of keywords to get data
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')

#df = dailydata.get_daily_data('cinema', 2019, 1, 2019, 10, geo = 'BR')

#1 Interest over Time
#ata = pytrends.interest_over_time()
#data = data.reset_index()

def collect_trend_score(keyword):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword])
    df = pytrend.interest_over_time()
    return df

def resample_trend_score_df(df, keyword):
    trends = df[keyword].resample('D', convention = 'start').pad()
    trends = pd.DataFrame(trends)
    trends.rename(columns = {keyword:'trend_score'}, inplace = True)
    return trends

df = collect_trend_score("bitcoin")
df2 = resample_trend_score_df(df, "bitcoin")
#print(df)
print(df2)

#df2.to_csv('../data/src/google_trends_bitcoin_srv', index=False)


