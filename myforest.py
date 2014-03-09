import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier
import time

def myforest(train, test, trees=250):
    #Training data prep-------------------------------------------------------------------------------------------
    csv_file_object = csv.reader(open(train, 'rb')) #Load in the training csv file
    header = csv_file_object.next() #Skip the fist line as it is a header
    output_header = header[0:2]
    train_data=[]
    for row in csv_file_object: #Skip through each row in the csv file
        train_data.append(row[1:]) #adding each row to the data variable
    train_data = np.array(train_data) #Then convert from a list to an array

    #Test data prep-----------------------------------------------------------------------------------------------
    test_file_object = csv.reader(open(test, 'rb')) #Load in the test csv file
    header = test_file_object.next() #Skip the fist line as it is a header
    test_data=[] #Create a variable called 'test_data'
    ids = []
    for row in test_file_object: #Skip through each row in the csv file
        ids.append(row[0])
        test_data.append(row[1:]) #adding each row to the data variable
    test_data = np.array(test_data) #Then convert from a list to an array

    #Train the forest
    print 'Training'
    forest = RandomForestClassifier(n_estimators=trees)
    forest = forest.fit(train_data[0::,1::], train_data[0::,0])

    print 'Predicting'
    output = forest.predict(test_data)

    open_file_object = csv.writer(open("result.csv", "wb"))
    open_file_object.writerow([output_header[0],output_header[1]])
    open_file_object.writerows(zip(ids, output))

start_time = time.time()
myforest('train.csv', 'test.csv', 2500)
print time.time() - start_time, "seconds"