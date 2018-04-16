import csv
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics , linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.isotonic import IsotonicRegression
from random import shuffle
from math import *

train_rows = []
test_rows = []
fields = []
Xtrain = []				# features for training
Ytrain = []				# target for training
Xtest = []				# features for training
Ytest = []				# test for training

def DivideTestandTrain():

	global train_rows , test_rows , fields ,Xtrain , Ytest , Xtest , Ytrain

	trainfile = 'train_data.csv'
	testfile = 'test_data.csv'

	with open(trainfile , 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		#fields = next(csvreader)
		for row in csvreader:
			train_rows.append(row)
	csvfile.close()
	with open(testfile , 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		#next(csvreader)
		for row in csvreader:
			test_rows.append(row)
	csvfile.close()
	# done making lists from files

	shuffle(train_rows)
	shuffle(test_rows)

	# divide into Xtrain , Ytrain & Xtest and Ytest
	for i in range(0 , len(train_rows) , 1):
		Xtrain.append(list(map(float , train_rows[i][0:len(fields) - 1])))
		Ytrain.append(int(train_rows[i][len(fields) - 1]))
	for i in range(0 , len(test_rows) , 1):
		Xtest.append(list(map(float , test_rows[i][0:len(fields) - 1])))
		Ytest.append(int(test_rows[i][len(fields) - 1]))

	
	Xtrain = np.array(Xtrain)
	Ytrain = np.array(Ytrain)
	Xtest = np.array(Xtest)
	Ytest = np.array(Ytest)
	
	# test
	#print(Xtrain[0] , Ytrain[0])
	#print(Xtest[0] , Ytest[0])

def Accuracy(tar , pred):
	lst = []
	for i in range(0 , len(pred) , 1):	
		tmp = abs(tar[i] - pred[i])
		tmp = 10 - (tmp/4) 
		lst.append(tmp)

	tot = sum(lst) * 100
	tot /= (10 * len(lst))
	print("%.2f"%(tot))

def plotGraph(X , Y , pred):
	plt.scatter(X , Y , color = 'black')
	plt.plot(X , pred , color = 'blue' , linewidth = 1)
	plt.xticks(())
	plt.yticks(())
	plt.show()

def LinearRegression():
   print("Linear Regression")
   regr = linear_model.LinearRegression()
   regr.fit(Xtrain , Ytrain)
   predictions = regr.predict(Xtest)
   #for i in range(0 , 150 , 1):
    # print(predictions[i] , Ytest[i])
   Accuracy(Ytest , predictions)
   #plotGraph(Xtest[:,0] , Ytest , predictions)


def Lasso():
	print("Lasso");
	regr = linear_model.Lasso()
	regr.fit(Xtrain , Ytrain)
	predictions = regr.predict(Xtest)
	#for i in range(0 , 150 , 1):
	#	print(predictions[i] , Ytest[i])
	Accuracy(Ytest , predictions)

def Ridge():
   print("Ridge");
   regr = linear_model.Ridge()
   regr.fit(Xtrain , Ytrain)
   predictions = regr.predict(Xtest)
   #for i in range(0 , 150 , 1):
   #  print(predictions[i] , Ytest[i])
   Accuracy(Ytest , predictions)


def ElasticNet():
	print("ElasticNet");
	regr = linear_model.ElasticNet()
	regr.fit(Xtrain , Ytrain)
	predictions = regr.predict(Xtest)
	#for i in range(0 , 150 , 1):
	#	print(predictions[i] , Ytest[i])
	Accuracy(Ytest , predictions)	

def Polynomial():
	print("polynomial")
	poly = PolynomialFeatures(degree=2)
	XtrainD = poly.fit_transform(Xtrain)
	XtestD = poly.fit_transform(Xtest)

	regr = linear_model.LinearRegression()
	regr.fit(XtrainD , Ytrain)
	predictions = regr.predict(XtestD)
	#for i in range(0 , 150 , 1):
	#	print(predictions[i] , Ytest[i])
	Accuracy(Ytest , predictions)
	

	
def solver():
	LinearRegression()
	#Ridge()
	#Lasso()
	#ElasticNet()
	#Polynomial()

if __name__== '__main__':
	#['run_rate' , 'score' , 'wickets' , 'home_ground' , 'balls' , 'batting_order' , 'momentum' , 'total_balls' , 'target']
	DivideTestandTrain()
	solver()
