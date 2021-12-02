"""CSV handler for extracted Twitter data

Extracts data out of csv file, transforms it ... blabla

"""

# Question 1
# Do cryptocurrencies depend on popularity?
# Correlation + Regression Analysis

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data =

corr = data.corr()
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(corr,cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,len(data.columns),1)
ax.set_xticks(ticks)
plt.xticks(rotation=90)
ax.set_yticks(ticks)
ax.set_xticklabels(data.columns)
ax.set_yticklabels(data.columns)
plt.show()