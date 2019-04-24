from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
import pickle
import numpy as np 
import argparse
import sys

option = len(sys.argv)

X_train = None
X_test = None
y_train = None
y_test = None

clf = MLPClassifier(hidden_layer_sizes=(100,50), max_iter=500)

def split():
    global X_train
    global X_test
    global y_train
    global y_test
    
    X = np.load("X.npy")
    y = np.load("Y.npy")
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)
    np.save("X_train", X_train)
    np.save("X_test", X_test)
    np.save("y_train", y_train)
    np.save("y_test", y_test)

def train():
    global X_train
    global X_test
    global y_train
    global y_test
    
    if (X_train is None) or (X_test is None) or (y_train is None) or (y_test is None):
        try:
            X_train = np.load("X_train")
            X_test = np.load("X_test")
            y_train = np.load("y_train")
            y_test = np.load("y_test")
        except FileNotFoundError:
            if not (X_train and X_test and y_train and y_test):
                split()
    
    scaler = StandardScaler()
    
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    clf.fit(X_train, y_train)
    pickle.dump(clf, open("model", 'wb'))

def test():
    global X_train
    global X_test
    global y_train
    global y_test
    
    if (X_train is None) or (X_test is None) or (y_train is None) or (y_test is None):
        try:
            X_train = np.load("X_train")
            X_test = np.load("X_test")
            y_train = np.load("y_train")
            y_test = np.load("y_test")
        except FileNotFoundError:
            if not (X_train and X_test and y_train and y_test):
                split()
        if not (X_train and X_test and y_train and y_test):
            print("X_train, X_test, y_train, and y_test do not exist")
            exit()
    
    clf = pickle.load(open("model", 'rb'))
    predictions = clf.predict(X_test)
    sum = 0
    for i in range(len(predictions)):
        if predictions[i] == y_test[i]:
            sum += 1
    print(sum/len(predictions))

if option == 1:
    print("test")
    test()
else:
    print("train and test")
    train()
    test()

print("done")