import pandas as pd
import os
import numpy as np
from DailyLogistic import dailyLogistic
from DailyMACD import dailyMACD
from DailyStochastic import dailyStochastic

def mergeDataSet():
    ds_Logistic = dailyLogistic(10)
    ds_MACD = dailyMACD(12,26,9)
    ds_Stochastic = dailyStochastic(14,3,3)

    result1 = pd.merge(ds_Stochastic,ds_Logistic[['Name', 'LogisticPrediction']], on='Name')
    result = pd.merge(result1,ds_MACD[['Name','exp1','exp2','macd','exp3','histogram','MacdCrossAboveSignal','MacdCrossAboveZero','MacdCrossAboveHist']], on='Name')

    print(result)


if __name__ == '__main__':
    mergeDataSet()

