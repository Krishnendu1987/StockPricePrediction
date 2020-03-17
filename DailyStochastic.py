import numpy as np
import os
import pandas as pd

import matplotlib.pyplot as plt

def dailyStochastic(a,b,c):
    directory = os.path.join(os.path.abspath(os.getcwd()), "Exports/")
    for root, dirs, files in os.walk(directory):
        #file_count = len(files)
        df_final = pd.DataFrame(index=range(0, 0),columns=['Name','Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(os.path.abspath(os.getcwd()), "Exports/", file)
                stockname = os.path.splitext(os.path.basename(filename))[0]
                df = pd.read_csv(filename)
                d = a+b+c+2
                df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
                df.index = df['Date']
                df = df.sort_index(ascending=True, axis=0)

                df_Test = pd.DataFrame(index=range(0, d),columns=['Name','Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
                j = 0
                for i in range(len(df) - d, len(df)):
                    df_Test['Name'] = stockname
                    df_Test['Open'][j] = df['Open'][i]
                    df_Test['High'][j] = df['High'][i]
                    df_Test['Low'][j] = df['Low'][i]
                    df_Test['Close'][j] = df['Close'][i]
                    df_Test['Adj Close'][j] = df['Adj Close'][i]
                    df_Test['Volume'][j] = df['Volume'][i]

                    j = j + 1
                print("Test Set ")
                # Create the "L14" column in the DataFrame
                df_Test['L14'] = df_Test['Low'].rolling(window=a).min()

                # Create the "H14" column in the DataFrame
                df_Test['H14'] = df_Test['High'].rolling(window=a).max()

                # Create the "Slow %K" column in the DataFrame
                df_Test['Slow%K'] = 100 * ((df_Test['Close'] - df_Test['L14']) / (df_Test['H14'] - df_Test['L14']))

                # Create the "Fast %K" column in the DataFrame
                df_Test['Fast%D'] = df_Test['Slow%K'].rolling(window=b).mean()

                # Create the "Fast %D" column in the DataFrame
                df_Test['Slow%D'] = df_Test['Fast%D'].rolling(window=c).mean()
                df_Train = df_Test.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
                #print(df_Test.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False))
                for i in range(len(df_Train)):
                    rowIndex = df_Train.index[i]
                    if df_Train.iloc[i]['Slow%K'] > df_Train.iloc[i]['Fast%D']:
                        df_Train.loc[rowIndex,'SlowStochCrossUP'] = "Y"
                    else:
                        df_Train.loc[rowIndex, 'SlowStochCrossUP'] = "N"
                    if df_Train.iloc[i]['Fast%D'] > df_Train.iloc[i]['Slow%D']:
                        df_Train.loc[rowIndex, 'FastStochCrossUP'] = "Y"
                    else:
                        df_Train.loc[rowIndex, 'FastStochCrossUP'] = "N"

                    if df_Train.iloc[i]['Slow%K'] < 20 or df_Train.iloc[i]['Fast%D'] < 20:
                        df_Train.loc[rowIndex,'SlowStochOverSold'] = "Y"
                    else:
                        df_Train.loc[rowIndex, 'SlowStochOverSold'] = "N"

                    if df_Train.iloc[i]['Slow%K'] > 75 or df_Train.iloc[i]['Fast%D'] > 75:
                        df_Train.loc[rowIndex,'SlowStochOverBought'] = "Y"
                    else:
                        df_Train.loc[rowIndex, 'SlowStochOverBought'] = "N"

                    if df_Train.iloc[i]['Fast%D'] < 20 or df_Train.iloc[i]['Slow%D'] < 20:
                        df_Train.loc[rowIndex, 'FastStochOverSold'] = "Y"
                    else:
                        df_Train.loc[rowIndex, 'FastStochOverSold'] = "N"

                    if df_Train.iloc[i]['Fast%D'] > 75 or df_Train.iloc[i]['Slow%D'] > 75:
                        df_Train.loc[rowIndex, 'FastStochOverBought'] = "Y"
                    else:
                        df_Train.loc[rowIndex, 'FastStochOverBought'] = "N"



                df_final = df_final.append(df_Train.tail(1))
        return df_final



if __name__ == '__main__':
    df_stoch = dailyStochastic(14,3,3)
    print(df_stoch)