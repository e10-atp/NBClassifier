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

    def perceptron(self, x, j, weightsList, numPass):#each feature is an array
        f1, f2, f3 = percepNum.feature(x)
        featureList  = [f1, f2, f3]
        equationList = [0,0,0,0,0,0,0,0,0,0]
        for a in range(10):
            equationList[a] = weightsList[a][0] + weightsList[a][1]*f1 + weightsList[a][2]*f2 + weightsList[a][3]*f3
        largestEquation = equationList[0]
        equationNum = 0
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
        f1, f2, f3 = percepNum.featureFace(x)
        featureList = [f1, f2, f3]
        equation = weights[0] + weights[1]*f1 + weights[2]*f2 + weights[3]*f3
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
        v = Gap.vertical(x.image)
        h = Gap.horizontal(x.image)
        im, s = ScaleDown.scale2(x.image, 7) 
        return v, h, s

    @staticmethod
    def featureFace(x):
        xList, yList = Regression.makeLists(x.image)
        m, b = Regression.findRegression(xList, yList)
        v = Gap.vertical(x.image)
        h = Gap.horizontal(x.image)
        #im, s = ScaleDown.scale2(x.image, 7) 
        return m, v, h

    def buildPhi(self):  # number of + and # over total pixels in line
        for node in self.samples:
            node.phiVector = {

                'm': None
            }
            xList, yList = Regression.makeLists(node.image)
            m, b = Regression.findRegression(xList, yList)
            node.phiVector['m'] = round(m, 1)

    def predict(self, x, weightsList):
        f1, f2, f3 = percepNum.feature2Face(x)
        equationList = [0,0,0,0,0,0,0,0,0,0]
        rand = random.randint(0,9)
        for a in range(10):
            equationList[a] = weightsList[a][0] + weightsList[a][1] *f1 + weightsList[a][2]*f2 + weightsList[a][3]*f3 
        largestEquation = equationList[0]
        equationNum = 0
        for q in range(10):
            if equationList[q] > largestEquation:
                largestEquation = equationList[0]
                equationNum = q
        return equationNum

    def predictFace(self, x, weights):
        f1, f2, f3 = percepNum.featureFace(x)
        equation = weights[0] + weights[1] *f1 + weights[2]*f2 + weights[3]*f3 
        if equation >= 0:
            return "1"
        else:
            return "0"


    @staticmethod
    def pDigit():
        weights0 = [0.01,0.01,0.01,0.01]
        weights1 = [0.01,0.01,0.01,0.01]
        weights2 = [0.01,0.01,0.01,0.01]
        weights3 = [0.01,0.01,0.01,0.01]
        weights4 = [0.01,0.01,0.01,0.01]
        weights5 = [0.01,0.01,0.01,0.01]
        weights6 = [0.01,0.01,0.01,0.01]
        weights7 = [0.01,0.01,0.01,0.01]
        weights8 = [0.01,0.01,0.01,0.01]
        weights9 = [0.01,0.01,0.01,0.01]
        weightsList = [weights0, weights1, weights2, weights3, weights4, weights5, weights6, weights7, weights8, weights9]
        j = len(weights0)
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
        while (endPoint == 0 or endPoint > numPass) and forceEnd < 5:
            forceEnd = forceEnd + 1
            #print(forceEnd)
            for x in instances:
                weightsList, numPass = percep.perceptron(x, j, weightsList, numPass)
                endPoint = endPoint + 1
            if endPoint != numPass:
                endPoint = 0
                numPass = 0
        print(weightsList)

        for x in testInstances:
            total += 1
            label = percep.predict(x, weightsList)
            labelstr = str(label)
            print(label)
            if (x.label == labelstr):
                correct += 1
        print(f"Numbers Percent Correct: {correct / total * 100}%")



    @staticmethod
    def pFace():
        weights = [0.01 0.01, 0.01, 0.01]
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
        while (endPoint == 0 or endPoint > numPass) and forceEnd < 1000:
            forceEnd = forceEnd + 1
            for x in instances:
                weights, numPass = percep.perceptronFace(x, j, weights, numPass)
                endPoint = endPoint + 1
            if endPoint != numPass:
                endPoint = 0
                numPass = 0

        for x in testInstances:
            total += 1
            label = percep.predictFace(x, weights)
            if (x.label == label):
                correct += 1
        print(f"Faces Percent Correct: {correct / total * 100}%")


if __name__ == '__main__':
    percepNum.pDigit()
    percepNum.pFace()
