import os, math, random, collections
from Node import Node
from Scan import Scan
from Regression import Regression

class NaiveBayes:

    def __init__(self, samples):
        self.samples = samples
        self.cntY = {}

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
            node.phiVector = {
                '+': 0,
                '#': 0,
                'blank': 0,
                'm': None
            }
            for c in node.image:
                if c == '+':
                    node.phiVector['+'] += 1
                elif c == '\n':
                    continue
                elif c == '#':
                    node.phiVector['#'] += 1
                else:  # if it's a space
                    node.phiVector['blank'] += 1
            xList, yList = Regression.makeLists(node.image)
            m, b = Regression.findRegression(xList, yList)
            node.phiVector['m'] = round(m)

    def buildPhiRegression(self):  # number of + and # over total pixels in line
        for node in self.samples:
            node.phiVector = {
                'm': 0
            }
            xList, yList = Regression.makeLists(node.image)
            m, b = Regression.findRegression(xList, yList)
            node.phiVector['m'] = round(1)

    def p_feature(self, x, j, y):
        return self.p_phiXandYTrue(x, j, y) / self.cntY[y]

    def p_featureFalse(self, x, j, y):
        return self.p_phiXandYFalse(x, j, y) / self.complement(self.cntY[y])

    def p_xGivenYTrue(self, x, y):
        prod = 1.0
        for j in x.phiVector:
            prod *= self.p_feature(x, j, y)
        return prod

    def p_phiXandYTrue(self, x, j, y):
        count = 0
        for n in self.samples:
            if n.phiVector[j] == x.phiVector[j] and n.label == y:
                count += 1
        return count

    def p_xGivenYFalse(self, x, y):
        prod = 1.0
        for j in x.phiVector:
            prod *= self.p_featureFalse(x, j, y)  # p feature false is 0
        return prod

    def p_phiXandYFalse(self, x, j, y):
        # what happens when this never occurs?
        count = 0
        for n in self.samples:
            if n.phiVector[j] == x.phiVector[j] and n.label != y:
                count += 1
        return count

    def complement(self, num):
        return len(self.samples) - float(num)

    def liklihoodRatio(self, x, y):
        top = self.p_xGivenYTrue(x, y) * self.cntY[y]
        bottom = self.p_xGivenYFalse(x, y) * self.complement(self.cntY[y])
        if bottom == 0:
            bottom = 0.00000001
        liklihoodRatio = top / bottom
        # liklihoodRatio = (self.p_xGivenYTrue(x) * self.cntY[x.label]) / (self.p_xGivenYFalse(x) * self.complement(self.cntY[x.label]))
        return liklihoodRatio

    def predict(self, x):
        max_p = 0
        max_label = None
        for l in self.cntY:
            p = self.liklihoodRatio(x, l)
            if p >= 1 and p > max_p:
                max_p = p
                max_label = l
        return max_p, max_label


if __name__ == '__main__':
    relpath = os.path.dirname(__file__)
    srcx = os.path.join(relpath, r'data/digitdata/trainingimages')
    srcy = os.path.join(relpath, r'data/digitdata/traininglabels')
    instances = Scan.scanIn(srcx, srcy, 1)
    bayes = NaiveBayes(instances)
    print(bayes.cntY)
    srcTestX = os.path.join(relpath, r'data/digitdata/validationimages')
    srcTestY = os.path.join(relpath, r'data/digitdata/validationlabels')
    testInstances = Scan.scanIn(srcTestX, srcTestY, 1)
    testBayes = NaiveBayes(testInstances) #assigns psivalues to all the test images
    total = 0
    correct = 0
    for x in testInstances:
        total += 1
        p, label = bayes.predict(x)
        if (x.label == label):
            correct += 1
    print(f"Percent Correct: {correct / total * 100}%")
    print(len(bayes.samples))
    print()
