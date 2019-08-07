from Node import Node
from Scan import Scan
import os, math, random, collections
from Regression import Regression

class percepNum:
    
    def __init__(self, samples):
        self.samples = samples
        self.cntY = {}#labels

        self.countY()
        self.buildPhi()
        self.nLabels = len(self.cntY)
        
    def countY(self):
        for node in self.samples:
            if node.label not in self.cntY:
                self.cntY[node.label] = 1
            else:
                self.cntY[node.label] += 1

    def perceptron(self, x, y, j, weightsList, numPass):#each feature is an array
    	#try to replace i with x here
        #e.g. feature1[i] should be the feature for x
        xList, yList = Regression.makeLists(x.image)
        m, b = Regression.findRegression(xList, yList)
        equationList = [0,0,0,0,0,0,0,0,0,0]
        for a in range(10):
            equationList[a] = weightsList[a][0]*m
		
        largestEquation = equationList[0]
        equationNum = 0
        for q in equationList[0]:
            if equationList[q] > largestEquation:
                largestEquation = equationList[0]
                equationNum = q


        if y == equationNum:
            numPass = numPass + 1

           # weightsList[equationNum][0] = weightsList[equationNum][0] + 1
            #for k in :
                #if k>0:
                    #weightsList[equationNum][k] = weightsList[equationNum][k] + featureList[k-1][i]
        else:
            #weightsList[equationNum][0] = weightsList[equationNum][0] - 1
            for k in range(j):
                if k>0:
                    weightsList[equationNum][k] = weightsList[equationNum][k] - m
                    weightsList[y][k] = weightsList[y][k] + m

        return weightsList, numPass
    def buildPhi(self):  # number of + and # over total pixels in line
        for node in self.samples:
            node.phiVector = {

                'm': None
            }
            xList, yList = Regression.makeLists(node.image)
            m, b = Regression.findRegression(xList, yList)
            node.phiVector['m'] = round(m, 1)

    def predict(self, x, weightsList):
        xList, yList = Regression.makeLists(x.image)
        m, b = Regression.findRegression(xList, yList)
        equationList = [0,0,0,0,0,0,0,0,0,0]
        for a in weightsList:
            equationList[a] = eights[0] + weightsList[a][1]*m
        largestEquation = equationList[0]
        equationNum = 0
        for q in equationList[0]:
            if equationList[q] > largestEquation:
                largestEquation = equationList[0]
                equationNum = q
        return equationNum

if __name__ == '__main__':

    weights0 = [0]
    weights1 = [0]
    weights2 = [0]
    weights3 = [0]
    weights4 = [0]
    weights5 = [0]
    weights6 = [0]
    weights7 = [0]
    weights8 = [0]
    weights9 = [0]
    weightsList = [weights0, weights1, weights2, weights3, weights4, weights5, weights6, weights7, weights8, weights9]
    j = weights0.len()
    digitHeight = 28
    relpath = os.path.dirname(__file__)
    srcx = os.path.join(relpath, r'data/digitdata/trainingimages')
    srcy = os.path.join(relpath, r'data/digitdata/traininglabels')
    instances = Scan.scanIn(srcx, srcy, digitHeight, 1)
    percep = percepNum(instances)


    #print(percep.cntY)
    srcTestX = os.path.join(relpath, r'data/digitdata/validationimages')
    srcTestY = os.path.join(relpath, r'data/digitdata/validationlabels')
    testInstances = Scan.scanIn(srcTestX, srcTestY, digitHeight, 1)
    testPercep = percepNum(testInstances)
    total = 0
    correct = 0

    endPoint = 0
    numPass = 0
    while endPoint ==0 or endPoint > numPass:
        for x in testInstances:
            weightsList, numPass = percep.perceptron(x, weightsList, numPass)
            endPoint = endPoint + 1
        if endPoint != numPass:
            endPoint = 0
            numPass = 0


    for x in testInstances:
        total += 1
        label = percep.predict(x, y, j, weightsList)
        if (x.label == label):
            correct += 1
    print(f"Percent Correct: {correct / total * 100}%")
