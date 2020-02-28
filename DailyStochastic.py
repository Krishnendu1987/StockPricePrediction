import numpy as np
import os
import pandas as pd

import matplotlib.pyplot as plt

def dailyStochastic():
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
                # Create the "L14" column in the DataFrame
                df_Test['L14'] = df_Test['Low'].rolling(window=14).min()

                # Create the "H14" column in the DataFrame
                df_Test['H14'] = df_Test['High'].rolling(window=14).max()

                # Create the "%K" column in the DataFrame
                df_Test['%K'] = 100 * ((df_Test['Close'] - df_Test['L14']) / (df_Test['H14'] - df_Test['L14']))

                # Create the "%D" column in the DataFrame
                df_Test['%D'] = df_Test['%K'].rolling(window=3).mean()
                df_Train = df_Test.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
                #print(df_Test.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False))



                print(df_Train)



if __name__ == '__main__':
    dailyStochastic()