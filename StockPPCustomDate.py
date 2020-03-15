
from datetime import datetime
import smtplib

import UtilityTool as util


# For Prediction
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing



from yahoo_fin import stock_info as si

def getStock(startDay,endDay,stockName):
    
    dateformat = "%d/%m/%Y"
    if datetime.strptime(startDay,dateformat).date() > datetime.strptime(endDay,dateformat).date() :
        print("Invalid Start date!!")
        return 
    else:
        try:
            #default interval is 1 day
            stockData = si.get_data(stockName, start_date = startDay , end_date = endDay)
            util.printToCSV(stockName, stockData)
            print("_____END_____")
        except Exception as e:
            print(e, 'error')
    


if __name__ == '__main__':
    startDay = input("Enter start date in dd/mm/yyyy format :: ")
    endDay = input ("Enter end date in [Min gap of 2 day needed] dd/mm/yyyy format :: ")
    stockName = input("Enter the Stock name - Example : ['nflx' , 'msft' , 'goog' etc ] :: ")
    getStock(startDay,endDay,stockName)
  
