'''
Author: Satrio Husodo
Uses spark to perform svm on eeg data
data format:
file#, window#, sleepstage#, <List of all unfiltered features>
'''

import sys
from pyspark.mllib.classification import SVMWithSGD, SVMModel
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext
from pyspark.mllib.evaluation import BinaryClassificationMetrics
from pyspark.mllib.util import MLUtils

# Load and parse the data
def parsePoint(line):
	values = [float(x) for x in line.split(' ')]
	return LabeledPoint(values[0], values[1:])

def parseFeatures(row):
	# print("Parsing raw_feats_concat_filteredatures...")
	row = row.split(";")
	fileInfo = row[0].split(",")
	features = row[1].split(",")
	if fileInfo[2] == 'W':
		sleepStage = float(0)
	elif fileInfo[2] == 'R':
		sleepStage = float(5)
	else:
		sleepStage = float(fileInfo[2])
	features = [float(x) for x in features]
	return LabeledPoint(sleepStage, features)
	

def oldParse(row):
	row = row.split()
	fileInfo = row[0].split(",")
	features = row[1].split(",")

	if fileInfo[2] == 'W':		# Wake
		sleepStage = float(0)
	else:
		sleepStage = float(fileInfo[2])
	features = [float(x) for x in features]
	return LabeledPoint(sleepStage, features)

def getModel(currentLabel, parsedData):
	'''
		Return SVM model based on current label and input data
		parsedData is an RDD
	'''
	def changeLabel(dataPoint):
		'''
			Necessary for allowing multiclass SVM
			Points with currentLabel will be labeled as 0
			Points with other labels will be labeled as 1
		'''
		if dataPoint.label == currentLabel:
			return LabeledPoint(0.0, dataPoint.features)
		else:
			return LabeledPoint(1.0, dataPoint.features)
	model = SVMWithSGD.train(parsedData.map(changeLabel)) #Error: changeLabel takes 2 values
	# model = SVMWithSGD.train(changeLabel(currentLabel, row) for row in parsedData)   #Error: Can't iterate RDD
	# model.clearThreshold()
	return model

def main():
	print("Starting svm.py...")
	# inpath = "random_examples.csv"
	# Input file path in the hadoop FS (not local)
	inpath = "svm/4pts_50feats.txt" 
	# inpath = "svm/raw_feats_concat.txt" 
	sc = SparkContext("local", "Simple App")

	data = sc.textFile(inpath)
	parsedData = data.map(parseFeatures)
	# svm = SVMWithSGD.train(parsedData, iterations=10)
	# print(svm.predict(sc.parallelize([testpoint])).collect())

	# Split data into training (60%) and test (40%)
	training, test = parsedData.randomSplit([0.6, 0.4], seed=11L)
	training.cache()


	# All possible sleep stages in the input file
	labels = [0.0,1.0,2.0,3.0,4.0,5.0]
	# labels = [0.0,1.0,2.0,3.0]
	# labels = [0.0,1.0,2.0]

	# Run training algorithm to build the model
	# model = SVMWithSGD.train(training)
	models = [getModel(lab, training) for lab in labels]
	# model = getModel('0', training)
	x = 0
	projectID = "171214_2105"
	metricsLog = open(projectID+"_metrics.txt", "a")
	for m in models:
		predictionAndLabels = test.map(lambda lp: (float(m.predict(lp.features)), lp.label))
		# Save results as this filename (will be saved in local dir)
		predictionAndLabels.saveAsTextFile(projectID+"_preds_"+ str(x))
		x += 1
		metrics = BinaryClassificationMetrics(predictionAndLabels)
		metricsLog.write("\n\nClass = %s" % str(x))
		metricsLog.write("\nArea under PR = %s" % metrics.areaUnderPR)
		metricsLog.write("\nArea under ROC = %s" % metrics.areaUnderROC)

	print("End of program...")

main()
