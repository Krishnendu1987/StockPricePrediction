import pandas as pd
import os
import numpy as np
from DailyLogistic import dailyLogistic
from DailyMACD import dailyMACD
from DailyStochastic import dailyStochastic

def mergeDataSet():
    ds_Logistic = dailyLogistic(5)
    ds_MACD = dailyMACD(12,26,9)
    ds_Stochastic = dailyStochastic(14,3,3)

    result1 = pd.merge(ds_Stochastic,ds_Logistic[['Name', 'LogisticPrediction']], on='Name')
    result = pd.merge(result1,ds_MACD[['Name','exp1','exp2','macd','exp3']], on='Name')
    print(len(result))
    for i in range(len(result)):
        #print(i)
        #print(result.iloc[i]['macd'])
        rowindex = result.index[i]
        if result.iloc[i]['macd'] > result.iloc[i]['exp3']:
            result.loc[rowindex,'MacdCrossAboveSignal'] = "U"
            #print("U")
        else:
            result.loc[rowindex,'MacdCrossAboveSignal'] = "D"
            #print("D")

    print(result)


if __name__ == '__main__':
    mergeDataSet()

