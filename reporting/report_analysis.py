import pandas as pd
import matplotlib.pyplot as plot
pd.options.display.float_format = '{:.2f}'.format

folder_path = '../data/{}'
gecko_data=pd.read_csv(folder_path.format('CoinGecko_Scrap.csv'), header=0)
google_data=pd.read_csv(folder_path.format('google_search.csv', hearder=0))


gecko_data['Date'] = pd.to_datetime(gecko_data['Date'])
gecko_data = gecko_data.set_index('Date')

google_data['date'] = pd.to_datetime(google_data['date'])
google_data = google_data.set_index('date')


print(gecko_data.head())
print(gecko_data.dtypes)
print(gecko_data.index)
print(google_data.dtypes)
print(google_data.head())
