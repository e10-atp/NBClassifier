from Node import Node
from Scan import Scan
import os, math, random, collections
from Regression import Regression
from Gap import Gap
from ScaleDown import ScaleDown

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

    def buildPhi(self):  # number of + and # over total pixels in line
        for node in self.samples:
            scaled = ScaleDown.scale(node.image, 0.25)
            i = 0
            scaledLines = scaled.split('\n')
            del scaledLines[-1]
            for line in scaledLines:
                node.phiVector['scaled' + str(i)] = line
                i += 1

    def perceptron(self, x, j, weightsList, numPass):#each feature is an array
        featureList  = percepNum.feature(x)
        equationList = [0,0,0,0,0,0,0,0,0,0]
        for a in range(10):
            #equationList[a] = weightsList[a][0]
            for b in range(j):
                #if b >0:
                equationList[a] = equationList[a] + weightsList[a][b]*featureList[b]
        equationNum = 0
        largestEquation = equationList[0]
        for q in range(10):
            if equationList[q] > largestEquation:
                largestEquation = equationList[0]
                equationNum = q
        if x.label == equationNum:
            numPass = numPass + 1
        else:
            for k in range(j):
                if k>0:
                    weightsList[equationNum][k] = weightsList[equationNum][k] - featureList[k-1]
                    weightsList[int(x.label)][k] = weightsList[int(x.label)][k] + featureList[k-1]
        return weightsList, numPass

    def perceptronFace(self, x, j, weights, numPass):
        featureList = percepNum.featureFace(x)
        equation = weights[0]
        for b in range(j):
            if b>0:
                equation = equation + featureList[b-1]*weights[b]
        if (equation >= 0 and x.label == "1") or (equation <0 and x.label == "0"):
            numPass = numPass + 1
        elif equation <0 and x.label == "1":
            for i in range(j):
                if i >0:
                    weights[i] = weights[i] + featureList[i-1]
            weights[0] = weights[0] + 1
        elif equation >=0 and x.label == "0":
            for i in range(j):
                if i >0:
                    weights[i] = weights[i] - featureList[i-1]
            weights[0] = weights[0] - 1
        return weights, numPass

    @staticmethod
    def feature(x):
        #xList, yList = Regression.makeLists(x.image)
        #m, b = Regression.findRegression(xList, yList)
        #v = Gap.vertical(x.image)
        #h = Gap.horizontal(x.image)
        #m, s = ScaleDown.scale2(x.image, 7) 
        featureList = []
        
        scaled = ScaleDown.scale(x.image, 0.25)
        
        scaledLines = scaled.split('\n')
        del scaledLines[-1]
        #print(scaledLines)
        for k in range(28):
            for z in range(28):
                i = 0
                if scaledLines[k][z] == '1':
                    i += 1
                featureList.append(i)
        return featureList

    @staticmethod
    def featureFace(x):
        xList, yList = Regression.makeLists(x.image)
        m, b = Regression.findRegression(xList, yList)
        v = Gap.vertical(x.image)
        h = Gap.horizontal(x.image)
        #im, s = ScaleDown.scale2(x.image, 7) 
        return [m, v, h]

    def predict(self, x,j, weightsList):
        featureList  = percepNum.feature(x)
        equationList = [0,0,0,0,0,0,0,0,0,0]
        for a in range(10):
            equationList[a] = weightsList[a][0]
            for b in range(j):
                if b >0:
                    equationList[a] = equationList[a] + weightsList[a][b]*featureList[b]
        equationNum = 0
        largestEquation = equationList[0]
        for q in range(10):
            if equationList[q] > largestEquation:
                largestEquation = equationList[0]
                equationNum = q
        return equationNum

    def predictFace(self, x,j,  weights):
        featureList = percepNum.featureFace(x)
        equation = weights[0]
        for b in range(j):
            if b>0:
                equation = equation + featureList[b-1]*weights[b]
        if equation >= 0:
            return "1"
        else:
            return "0"


    @staticmethod
    def pDigit():
        weightsList = [0]*10
        for q in range(10):
            weights = [0]*49
            for w in range(49):
                weights[w] = random.random()
            weightsList[q] = weights
        j = len(weightsList[0])
        digitHeight = 28
        relpath = os.path.dirname(__file__)
        srcx = os.path.join(relpath, r'data/digitdata/trainingimages')
        srcy = os.path.join(relpath, r'data/digitdata/traininglabels')
        instances = Scan.scanIn(srcx, srcy, digitHeight, 1)
        percep = percepNum(instances)

        srcTestX = os.path.join(relpath, r'data/digitdata/validationimages')
        srcTestY = os.path.join(relpath, r'data/digitdata/validationlabels')
        testInstances = Scan.scanIn(srcTestX, srcTestY, digitHeight, 1)
        testPercep = percepNum(testInstances)
        total = 0
        correct = 0

        endPoint = 0
        numPass = 0
        forceEnd = 0
        while (endPoint == 0 or endPoint > numPass) and forceEnd < 50:
            forceEnd = forceEnd + 1
            #print(forceEnd)
            for x in instances:
                weightsList, numPass = percep.perceptron(x, j, weightsList, numPass)
                endPoint = endPoint + 1
            if endPoint != numPass:
                endPoint = 0
                numPass = 0
        #print(weightsList)
        for x in testInstances:
            total += 1
            label = percep.predict(x, j, weightsList)
            labelstr = str(label)
            #print(label)
            if (x.label == labelstr):
                correct += 1
        print(f"Numbers Percent Correct: {correct / total * 100}%")



    @staticmethod
    def pFace():
        weights = [0]*4
        for w in range(4):
            weights[w] = random.random()
        j = len(weights)
        relpath = os.path.dirname(__file__)
        facex = os.path.join(relpath, r'data/facedata/facedatatrain')
        facey = os.path.join(relpath, r'data/facedata/facedatatrainlabels')
        faceHeight = 70
        instances = Scan.scanIn(facex, facey, faceHeight, 1)
        percep = percepNum(instances)
        ftestx = os.path.join(relpath, r'data/facedata/facedatavalidation')
        ftesty = os.path.join(relpath, r'data/facedata/facedatavalidationlabels')
        testInstances = Scan.scanIn(ftestx, ftesty, faceHeight, 1)
        testPercep = percepNum(testInstances)

        total = 0
        correct = 0
        endPoint = 0
        numPass = 0
        forceEnd = 0
        while (endPoint == 0 or endPoint > numPass) and forceEnd < 50:
            forceEnd = forceEnd + 1
            for x in instances:
                weights, numPass = percep.perceptronFace(x, j, weights, numPass)
                endPoint = endPoint + 1
            if endPoint != numPass:
                endPoint = 0
                numPass = 0
        print(weights)
        for x in testInstances:
            total += 1
            label = percep.predictFace(x,j, weights)
            if (x.label == label):
                correct += 1
        print(f"Faces Percent Correct: {correct / total * 100}%")


if __name__ == '__main__':
    #percepNum.pDigit()
    percepNum.pFace()
