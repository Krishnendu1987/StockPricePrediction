import os

# Import warnings and add a filter to ignore them
import warnings
warnings.simplefilter('ignore')
# Import XGBoost
import xgboost
# XGBoost Classifier
from xgboost import XGBClassifier
# Classification report and confusion matrix
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# Cross validation
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
# Pandas datareader to get the data
from pandas_datareader import data
# To plot the graphs
#import matplotlib.pyplot as plt
#import seaborn as sn
# For data manipulation
import pandas as pd
import numpy as np

def testTrainSet():
    directory = os.path.join(os.path.abspath(os.getcwd()), "Exports/")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filename = os.path.join(os.path.abspath(os.getcwd()), "Exports/", file)
                stock_name = os.path.splitext(os.path.basename(filename))[0]
                # Create a placeholder to store the stock data
                stock_data_dictionary = {}
                df = pd.read_csv(filename)

                df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
                df.index = df['Date']
                df = df.sort_index(ascending=True, axis=0)
                # Calculate the daily percent change
                df['daily_pct_change'] = df['Adj Close'].pct_change()
                # create the predictors
                predictor_list = []
                for r in range(0, 2, 1):
                    df['pct_change_' + str(r)] = df.daily_pct_change.rolling(r).sum()
                df['std_' + str(r)] = df.daily_pct_change.rolling(r).std()
                predictor_list.append('pct_change_' + str(r))
                predictor_list.append('std_' + str(r))
                # Target Variable
                df['return_next_day'] = df.daily_pct_change.shift(-1)
                df['actual_signal'] = np.where(df.return_next_day > 0, 1, -1)
                #df = df.dropna(how='all', axis=1)
                # Add the data to dictionary
                print('Stock Name ', stock_name)
                #print(df)
                stock_data_dictionary.update({stock_name: df})

                # Create a placeholder for the train and test split data
                X_train = pd.DataFrame()
                X_test = pd.DataFrame()
                y_train = pd.Series()
                y_test = pd.Series()

                # Get predictor variables
                X = stock_data_dictionary[stock_name][predictor_list]
                # Get the target variable
                y = stock_data_dictionary[stock_name].actual_signal
                # Divide the dataset into train and test
                train_length = int(len(X) * 0.80)
                X_train = X_train.append(X[:train_length])
                X_test = X_test.append(X[train_length:])
                y_train = y_train.append(y[:train_length])
                y_test = y_test.append(y[train_length:])
                #print(X_train)
                #print(y_train)

                # Initialize the model and set the hyperparameter values
                model = XGBClassifier(max_depth=2, n_estimators=30)

                # Initialize the KFold parameters
                kfold = KFold(n_splits=5, random_state=7)
                # Perform K-Fold Cross Validation
                results = cross_val_score(model, X_train, y_train, cv=kfold)
                # Print the average results
                print("Accuracy: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))

                model.fit(X_train, y_train)
                # Predict the trading signal on test dataset
                y_pred = model.predict(X_test)
                print('Actual')
                print(y_test)
                print('Prediction')
                print(y_pred)
                # Get the classification report
                print(classification_report(y_test, y_pred))


if __name__ == '__main__':
    testTrainSet()