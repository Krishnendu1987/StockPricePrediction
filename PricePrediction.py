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

def predictData(stock, days):
    print(stock)
    directory = os.path.join(os.path.abspath(os.getcwd()), "Exports/")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(os.path.abspath(os.getcwd()), "Exports/", file)
                stockname = os.path.splitext(os.path.basename(filename))[0]
                df = pd.read_csv(filename)
                df1 = pd.read_csv(filename)
                df1['Date'] = pd.to_datetime(df1.Date, format='%Y-%m-%d')
                df1.index = df1['Date']
                data1 = df1.sort_index(ascending=True, axis=0)
                del df1['Date']
                X1 = np.array(df1)
                df['Prediction'] = df['Close'].shift(-1)
                df.dropna(inplace=True)
                df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
                df.index = df['Date']
                data = df.sort_index(ascending=True, axis=0)
                del df['Date']
                forecast_time = int(days)
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
                last_row = df.tail(1)
                last_row1 = df1.tail(1)
                print("Company: ",stockname)
                print(last_row['Close'])
                print("Prediction based on last ", days," days of data: ", prediction[4])
                print(last_row1['Close'])
                print("Prediction based on last ", days, " days of data for the next day: ", prediction1[4])





if __name__ == '__main__':
    predictData('ACB', 5)