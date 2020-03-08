import iexfinance
import numpy as np
from datetime import datetime
import smtplib
from selenium import webdriver
import os
import pandas_datareader.data as web
import yfinance as yf

# For Prediction
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

# For Stock Data
from iexfinance.stocks import get_historical_data


def getStock(n):
    # Navigsting to Yahoo Stock Screener
    driver = webdriver.Chrome(executable_path=r"C:/PATH_TO_CHROME_DRIVER/chromedriver_win32/chromedriver.exe")
    url = "https://finance.yahoo.com/screener/predefined/aggressive_small_caps?offset=0&count=202/html"
    driver.get(url)
    # Creating a stock list and iterating through the ticker name on that list
    stock_list = []
    n += 1
    for i in range(1, n):
        ticker = driver.find_element_by_xpath(
            '//*[@id = "scr-res-table"]/div[1]/table/tbody/tr[' + str(i) + ']/td[1]/a')
        stock_list.append(ticker.text)

    driver.quit()
    # Using the stock list to predict the future price of the stock a specificed amount of days
    number = 0
    for i in stock_list:
        print("Number: " + str(number))
        print("Stock: " + i)
        predictData(i)
        number += 1


def predictData(stock):
    print(stock)

    start = datetime(2020, 1, 1)
    end = datetime.now()

    # print(df)
    if os.path.exists('./Exports'):
        csv_name = ('Exports/' + stock + '_Export.csv')
    else:
        os.mkdir("Exports")
        csv_name = ('Exports/' + stock + '_Export.csv')

        # Outputting the Historical data into a .csv for later use
    try:

       # df = web.DataReader(stock, "quandl", start, end, api_key='LmyQyxFdyfBDTGG1wn')
        df = yf.download(stock, start, end)
        print(df.head())
        df.to_csv(csv_name)
        print(stock, 'downloaded')
    except Exception as e:
        print(e, 'error')


if __name__ == '__main__':
    getStock(3)
