
from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils

sc = SparkContext.getOrCreate()
raw_rdd = sc.textFile("./raw_feats_concat.txt")

def parseData(line):
    dataRow = [x for x in line.split('\t')]
    sleepStage = dataRow[0].split(',')[-1]
    if sleepStage == '?':
        sleepStage = float(0)
    elif sleepStage == 'W':
        sleepStage = float(3)
    else:
        sleepStage = float(sleepStage)
    features = [float(x) for x in dataRow[1].split(',')]
    return LabeledPoint(sleepStage, features)

parsedData = raw_rdd.map(parseData)

(trainingData, testData) = parsedData.randomSplit([0.7, 0.3])

####################################
# Testing numTree:

def test_numTree(n):
    model1 = RandomForest.trainClassifier(trainingData, numClasses=4, categoricalFeaturesInfo={},
                                     numTrees=n, featureSubsetStrategy="auto",
                                     impurity='gini', maxDepth=5, maxBins=32)
    predictions1 = model1.predict(testData.map(lambda x: x.features))
    labelsAndPredictions1 = testData.map(lambda lp: lp.label).zip(predictions1)
    testErr1 = labelsAndPredictions1.filter(lambda (v, p): v != p).count() / float(testData.count())
    return testErr1 


error_numTree = []
for i in range(3, 501):
    error_numTree.append(test_numTree(i))
with open("error_numTree.txt", "w") as output:
    output.write(str(error_numTree))

####################################
# Testing maxDepth
def test_maxDepth(n):
    model1 = RandomForest.trainClassifier(trainingData, numClasses=4, categoricalFeaturesInfo={},
                                     numTrees=46, featureSubsetStrategy="auto",
                                     impurity='gini', maxDepth=n, maxBins=32)
    predictions1 = model1.predict(testData.map(lambda x: x.features))
    labelsAndPredictions1 = testData.map(lambda lp: lp.label).zip(predictions1)
    testErr1 = labelsAndPredictions1.filter(lambda (v, p): v != p).count() / float(testData.count())
    return testErr1

error_maxDepth = []
for i in range(3, 31):
    error_maxDepth.append(test_maxDepth(i))

with open("error_maxDepth.txt", "w") as output:
    output.write(str(error_maxDepth))

####################################
# Testing impurity
def test_impurity(n):
    model1 = RandomForest.trainClassifier(trainingData, numClasses=4, categoricalFeaturesInfo={},
                                     numTrees=n, featureSubsetStrategy="auto",
                                     impurity='entropy', maxDepth=5, maxBins=32)
    predictions1 = model1.predict(testData.map(lambda x: x.features))
    labelsAndPredictions1 = testData.map(lambda lp: lp.label).zip(predictions1)
    testErr1 = labelsAndPredictions1.filter(lambda (v, p): v != p).count() / float(testData.count())
    return testErr1


error_impurity = []
for i in range(3, 51):
    error_impurity.append(test_impurity(i))

with open("error_impurity.txt", "w") as output:
    output.write(str(error_impurity))