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
pytrends = TrendReq(hl='en-US', tz=360)
startTime = time.time()


def get_data_google_trends(keyword):
    pytrends.build_payload(keyword, cat=0, timeframe='2020-01-01 2020-12-31')
    data=pytrends.interest_over_time()
    data.to_csv('google_search.csv')



