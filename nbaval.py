import pandas as pd
from pandas import DataFrame
from pandas import Series
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv('final.csv')
m = RandomForestClassifier(n_estimators = 5, n_jobs=1)

predictions = []

for i in range(0,len(data.ix[:,0])):
    train = data.drop(i, axis = 0)
    test = DataFrame(data.ix[i,:]).T

    m.fit(train.ix[:,4:], train.ix[:,'WL'])
    predictions.append(m.predict(test.ix[:,4:])[0])
    print str(round((float(i)/len(data.ix[:,0]) * 100), ndigits=1)) + '%'

preds = Series(predictions)
wl = Series(data.ix[:,'WL'])

correct = float((preds == wl).sum())
percent_correct = round(correct / (len(wl)) * 100, ndigits=2)

print "Predictions were " + str(percent_correct) + "% correct."