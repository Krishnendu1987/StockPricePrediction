import os
from datetime import datetime

def printToCSV(stockName, stockData):
    # print(df)
    if os.path.exists('./Exports'):
        print("Folder Exists")
    else:
        os.mkdir("Exports")
        print("Folder Created")

    csv_name = ('Exports/'+stockName+'-'+datetime.now().strftime("%d-%m-%Y")+ '_Export.csv')
    

        # Outputting the Historical data into a .csv for later use
    try:
        stockData.to_csv(csv_name)
        print(stockData)
        print('Downloaded to -> ', csv_name)
    except Exception as e:
        print(e, 'error')