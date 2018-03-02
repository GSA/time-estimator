import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
import pandas as pd
import math

from config import *

train_set=pd.read_csv(training_path).fillna(0)
print("train_set:", train_set)

label = "duration"

model = LinearRegression()


Y = train_set[label]
print("Y:", Y)

difference = train_set.columns.difference([label])
print("difference:", difference)

X = train_set[difference]
#X = train_set["count_additions"].reshape(-1, 1)
print("X:", X)

model.fit(X, Y)

print("fitted")

test_set=pd.read_csv(testing_path).fillna(0)

Y_test = test_set[label]
print("Y_test:", Y_test)

X_test = test_set[test_set.columns.difference([label])]
#X_test = test_set["count_additions"].reshape(-1, 1)


score = model.score(X_test, Y_test)
print("score:", score)

testing_results = []

predictions = model.predict(X_test)
print("predictions", len(predictions))

for index, prediction in list(enumerate(predictions))[:100]:
    try:
        print(prediction, "vs", Y_test[index])
    except Exception as e:
        print(e)