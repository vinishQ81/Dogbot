import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

def dog_prediction(answers):
    data = pd.read_csv('dataset.csv')
    X = np.array(data.loc[:, 'Агрессивность':'Время затратность']) / 10
    y_mass = {}
    y = []
    for i in range(len(data['породы'])):
        y.append(i)
        d = {i: data['породы'][i]}
        y_mass.update(d)
    y = np.array(y)

    clf = DecisionTreeClassifier()
    clf.fit(X, y)

    predict = np.array(answers) / 10
    out = clf.predict([answers])
    return y_mass[out[0]]
