"""CSV handler for extracted Twitter data

Extracts data out of csv file, transforms it ... blabla
https://medium.com/@szabo.bibor/how-to-create-a-seaborn-correlation-heatmap-in-python-834c0686b88e
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import seaborn as sns

# Question 2
# Do people invest in cryptocurrencies in opposition to stock market?
# Regression Analysis

### load prepared data
df_q2 = pd.read_csv('../data/merged/data_question_two.csv')


#print(df_q2.corr())
def correlation_heatmap():
    sns.heatmap(df_q2.corr())
    np.triu(np.ones_like(df_q2.corr()))

    plt.figure(figsize=(16, 6))
    # define the mask to set the values in the upper triangle to True
    mask = np.triu(np.ones_like(df_q2.corr(), dtype=np.bool))
    heatmap = sns.heatmap(df_q2.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')
    heatmap.set_title('Triangle Correlation Heatmap', fontdict={'fontsize': 18}, pad=16);
    plt.show()

correlation_heatmap()
# prepare data
### loading and preparing data ###

def graphical_analysis():
    # Method to plot the bitcoin valuation together with the google trend and twitter count data.

    #df_q2['bitcoin_value'] = df_q2['bitcoin_value']

    fig, ax = plt.subplots()
    ax.plot(df_q2['bitcoin_value'], label='Bitcoin', color='y', linewidth=1.0)
    ax.plot(df_q2['gold_value'], label='Gold', color='r', linewidth=1.0)
    ax.plot(df_q2['oil_value'], label='Oil', color='b', linewidth=1.0)
    ax.plot(df_q2['nasdaq_value'], label='NASDAQ', color='g', linewidth=1.0)
    ax.set_xlabel('Time')
    ax.set_ylabel('Values')
    ax.set_yscale('log')
    ax.set_title("Graphical analysis: Bitcoin vs Stockmarket")
    ax.legend()
    plt.show()

#graphical_analysis()