from Node import Node
from Scan import Scan
import os, math, random, collections

class percepNum:
    def __init__(self, samples):
        self.samples = samples
        self.cntY = {}#labels

        self.countY()
        self.buildPhi()
        self.nLabels = len(self.cntY)
        weights0 = [0,0,0,0,0]
        weights1 = [0,0,0,0,0]
        weights2 = [0,0,0,0,0]
        weights3 = [0,0,0,0,0]
        weights4 = [0,0,0,0,0]
        weights5 = [0,0,0,0,0]
        weights6 = [0,0,0,0,0]
        weights7 = [0,0,0,0,0]
        weights8 = [0,0,0,0,0]
        weights9 = [0,0,0,0,0]
        weightsList = [weights0, weights1, weights2, weights3, weights4, weights5, weights6, weights7, weights8, weights9]

     def countY(self):
        for node in self.samples:
            if node.label not in self.cntY:
                self.cntY[node.label] = 1
            else:
                self.cntY[node.label] += 1

    def buildPhi(self):  # number of + and # over total pixels in line
        for node in self.samples:
            node.phiVector = {
                'blankPix': 0,
                'filledPix': 0
            }
            for c in node.image:
                if c == '+' or c == '#':
                    node.phiVector['filledPix'] += 1
                elif c == '\n':
                    continue
                else:  # if it's a space
                    node.phiVector['blankPix'] += 1

    def p_feature(self, x, j, y):
        return self.p_phiXandYTrue(x, j, y) / self.cntY[y]

    def p_featureFalse(self, x, j, y):
        return self.p_phiXandYFalse(x, j, y) / self.complement(self.cntY[y])

	@staticmethod
    def perceptron(self, x, y , feature1, feature2, feature3, feature4):#each feature is an array
    	done = 0
    	featureList = [feature1, feature2, feature3, feature4]
    	#try to replace i with x here
        #e.g. feature1[i] should be the feature for x
        equationList = [0,0,0,0,0,0,0,0,0,0]
        for a in weightsList:
            equationList[a] = eights[0] + weightsList[a][1]*feature1[i] + weightsList[a][2]*feature2[i] + weightsList[a][3]*feature3[i] + weightsList[a][4]*feature4[i]
		
        largestEquation = equationList[0]
        equationNum = 0
        for b in equationList[0]:
            if equationList[b] > largestEquation:
                largestEquation = equationList[0]
                equationNum = b


		if y[i] == equationNum:
			weightsList[equationNum][0] = weightsList[equationNum][0] + 1
			for j in weights:
				if j>0:
					weightsList[equationNum][j] = weightsList[equationNum][j] + featureList[j-1][i]
		else:
			weightsList[equationNum][0] = weightsList[equationNum][0] - 1
			for j in weights:
				if j>0:
					weightsList[equationNum][j] = weightsList[equationNum][j] - featureList[j-1][i]


if __name__ == '__main__':
    relpath = os.path.dirname(__file__)
    srcx = os.path.join(relpath, r'data/digitdata/trainingimages')
    srcy = os.path.join(relpath, r'data/digitdata/traininglabels')
    instances = Scan.scanIn(srcx, srcy, 1)
    percep = percepNum(instances)


    print(bayes.cntY)
    srcTestX = os.path.join(relpath, r'data/digitdata/validationimages')
    srcTestY = os.path.join(relpath, r'data/digitdata/validationlabels')
    testInstances = Scan.scanIn(srcTestX, srcTestY, 1)
    testBayes = NaiveBayes(testInstances)
    total = 0
    correct = 0
    for x in testBayes.samples:
        total += 1
        p, label = bayes.predict(x)
        if (x.label == label):
            correct += 1
    print(f"Percent Correct: {correct / total * 100}%")
