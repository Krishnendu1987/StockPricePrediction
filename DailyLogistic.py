import iexfinance
import numpy as np
from datetime import datetime
import smtplib
from selenium import webdriver
import os
import pandas_datareader.data as web
import yfinance as yf
import csv
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def dailyLogistic( days):

    directory = os.path.join(os.path.abspath(os.getcwd()), "Exports/")
    for root, dirs, files in os.walk(directory):
        df_final = pd.DataFrame(index=range(0, 0),columns=['Name', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(os.path.abspath(os.getcwd()), "Exports/", file)
                stockname = os.path.splitext(os.path.basename(filename))[0]
                df = pd.read_csv(filename)
                df1 = pd.read_csv(filename)
                df1['Date'] = pd.to_datetime(df1.Date, format='%Y-%m-%d')
                df1.index = df1['Date']
                data1 = df1.sort_index(ascending=True, axis=0)
                forecast_time = int(days)

                del df1['Date']
                data1_prediction = data1[-forecast_time:]
                X1 = np.array(df1)
                df['Prediction'] = df['Close'].shift(-1)
                df.dropna(inplace=True)
                df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
                df.index = df['Date']
                data = df.sort_index(ascending=True, axis=0)
                del df['Date']

                # Predicting the Stock price in the future
                X = np.array(df.drop(['Prediction'], 1))
                Y = np.array(df['Prediction'])
                #print("+++++++++ X +++++++++")
                #print(X)
                #print("+++++++++ Y +++++++++")
                #print(Y)
                X = preprocessing.scale(X)
                X1 = preprocessing.scale(X1)
                #print("+++++++++ X +++++++++")
                #print(X)
                X_prediction = X[-forecast_time:]
                X1_prediction = X1[-forecast_time:]
                #print("Forecast : ")
                #print(X_prediction)
                X_train, X_test,Y_train, Y_test = train_test_split(X, Y, test_size=0.5)
                clf = LinearRegression()
                clf.fit(X_train, Y_train)
                prediction = (clf.predict(X_prediction))
                prediction1 = (clf.predict(X1_prediction))
                #for i in range(len(data1_prediction)):
                #    rowindex = data1_prediction.index[i]
                #    trend = prediction1[i] - data1_prediction.loc[rowindex, 'Close']
                #    data1_prediction.loc[rowindex, 'LogisticPrediction'] = trend
                data1_prediction['LogisticPrediction'] = prediction1 - data1_prediction['Close']

                data1_prediction.insert(0,'Name',stockname)
                data1_prediction.reset_index(drop=True,inplace=True)
                del data1_prediction['Date']
                print(prediction1)
                #last_row1['Name'] = stockname
                #print("Company: ",stockname)
                #print(last_row1['Close'])
                #print("Prediction based on last ", days, " days of data for the next day: ", last_row1)
                df_final = df_final.append(data1_prediction.tail(1))

        return df_final






if __name__ == '__main__':
    df_logistic = dailyLogistic(10)
    print(df_logistic)