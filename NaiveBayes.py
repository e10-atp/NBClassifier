import os, math, random, collections
from Node import Node
from Scan import Scan


class NaiveBayes:

    def __init__(self, samples):
        self.samples = samples
        self.cntY = {}

        self.train()
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

    def p_feature(self, x, j):
        return self.p_phiXandYTrue(x, j) / self.cntY[x.label]

    def p_featureFalse(self, x, j):
        return self.p_phiXandYFalse(x, j) / self.complement(self.cntY[x.label])

    def p_xGivenYTrue(self, x):
        prod = 1.0
        for j in x.phiVector:
            prod *= self.p_feature(x, j)
        return prod

    def p_phiXandYTrue(self, x, j):
        count = 0
        for n in self.samples:
            if n.phiVector[j] == x.phiVector[j] and n.label == x.label:
                count += 1
        return count

    def p_xGivenYFalse(self, x):
        prod = 1.0
        for j in x.phiVector:
            prod *= self.p_featureFalse(x, j) #p feature false is 0
        return prod

    def p_phiXandYFalse(self, x, j):
        #what happens when this never occurs?
        count = 0
        for n in self.samples:
            if n.phiVector[j] == x.phiVector[j] and n.label != x.label:
                count += 1
        if count == 0:
            count = 0.0000000000001
        return count

    def complement(self, num):
        return len(self.samples) - float(num)

    def liklihoodRatio(self, x):
        top = self.p_xGivenYTrue(x) * self.cntY[x.label]
        bottom = self.p_xGivenYFalse(x) * self.complement(self.cntY[x.label])
        liklihoodRatio = top / bottom
        #liklihoodRatio = (self.p_xGivenYTrue(x) * self.cntY[x.label]) / (self.p_xGivenYFalse(x) * self.complement(self.cntY[x.label]))
        return liklihoodRatio

    def train(self):
        self.countY()
        self.buildPhi()

    def predict(self, x):
        #check this
        max_p = 0
        max_label = None
        for key, val in self.cntY.items():
            x.label = key #this is wrong
            p = self.liklihoodRatio(x)
            if p >= 1 and p > max_p:
                max_p = p
                max_label = key
        return max_p, max_label


if __name__ == '__main__':
    relpath = os.path.dirname(__file__)
    srcx = os.path.join(relpath, r'data/digitdata/trainingimages')
    srcy = os.path.join(relpath, r'data/digitdata/traininglabels')
    data = list()  # complete dataset
    labels = list()
    Scan.scanIn(srcx, srcy, data, labels)
    instances = Scan.randomSelect(1, data, labels)
    bayes = NaiveBayes(instances)
    for i in bayes.samples:
        print(i.phiVector)
    print(bayes.cntY)
    for u in bayes.cntY:
        print(bayes.complement(bayes.cntY[u]))
    #for i in instances:
    for x in instances:
        bayes.predict(x)


