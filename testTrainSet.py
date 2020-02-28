import numpy as np
import os
import pandas as pd

def testTrainSet():
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

                df_Test = pd.DataFrame(index=range(0, 15),columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
                j = 0
                for i in range(len(df) - 15, len(df)):
                    df_Test['Open'][j] = df['Open'][i]
                    df_Test['High'][j] = df['High'][i]
                    df_Test['Low'][j] = df['Low'][i]
                    df_Test['Close'][j] = df['Close'][i]
                    df_Test['Adj Close'][j] = df['Adj Close'][i]
                    df_Test['Volume'][j] = df['Volume'][i]

                    j = j + 1
                print("Test Set ")
                print(df_Test)

                df['Prediction'] = df['Close'].shift(-1)
                df.dropna(inplace=True)

                #print(df)
                del df['Date']
                df_Train = pd.DataFrame(index=range(0, 15), columns=['Open','High','Low','Close','Adj Close','Volume','Prediction'])
                j = 0
                for i in range(len(df)-15, len(df)):
                    df_Train['Open'][j] = df['Open'][i]
                    df_Train['High'][j] = df['High'][i]
                    df_Train['Low'][j] = df['Low'][i]
                    df_Train['Close'][j] = df['Close'][i]
                    df_Train['Adj Close'][j] = df['Adj Close'][i]
                    df_Train['Volume'][j] = df['Volume'][i]
                    df_Train['Prediction'][j] = df['Prediction'][i]
                    j = j + 1
                print("Train Set ")
                print(df_Train)


if __name__ == '__main__':
    testTrainSet()