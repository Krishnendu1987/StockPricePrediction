import numpy as np
import os
import pandas as pd

import matplotlib.pyplot as plt

def dailyMACD():
    directory = os.path.join(os.path.abspath(os.getcwd()), "Exports/")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(os.path.abspath(os.getcwd()), "Exports/", file)
                stockname = os.path.splitext(os.path.basename(filename))[0]
                df = pd.read_csv(filename)

                df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
                df.index = df['Date']
                df = df.sort_index(ascending=True, axis=0)

                df_Test = pd.DataFrame(index=range(0, 28),columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
                j = 0
                for i in range(len(df) - 28, len(df)):

                    df_Test['Open'][j] = df['Open'][i]
                    df_Test['High'][j] = df['High'][i]
                    df_Test['Low'][j] = df['Low'][i]
                    df_Test['Close'][j] = df['Close'][i]
                    df_Test['Adj Close'][j] = df['Adj Close'][i]
                    df_Test['Volume'][j] = df['Volume'][i]

                    j = j + 1
                print("Test Set ")

                df_Test = df_Test[['Close']]
                df_Test.reset_index(level=0, inplace=True)
                #df_Test.cloumns=['Close']
                exp1 = df_Test.Close.ewm(span=12, adjust=False).mean()
                exp2 = df_Test.Close.ewm(span=26, adjust=False).mean()
                macd = exp1 - exp2
                exp3 = macd.ewm(span=9, adjust=False).mean()
                print(df_Test.head())
                plt.plot(df_Test.index, macd, label='MACD', color='#EBD2BE')
                plt.plot(df_Test.index, exp3, label='Signal Line', color='#E5A4CB')
                plt.plot(df_Test.index, df_Test.Close, label='Close Price', color='#EFA4CB')
                plt.legend(loc='upper left')
                plt.show()


if __name__ == '__main__':
    dailyMACD()