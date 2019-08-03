import os, math, random, collections
from Node import Node
from Scan import Scan


class NaiveBayes:

    def __init__(self, instances):
        self.instances = instances
        self.p_Y = {}
        self.learnedList = []

    def probY(self):
        for node in self.instances:
            if node.label not in self.p_Y:
                self.p_Y[node.label] = 1
            else:
                self.p_Y[node.label] += 1

    def psiFunc(self):  # number of + and # over total pixels in line
        for node in self.instances:
            node.psiVector = {
                'blankPix': 0,
                'filledPix': 0
            }
            for c in node.image:
                if c == '+' or c == '#':
                    node.psiVector['filledPix'] += 1
                elif c == '\n':
                    continue
                else:  # if it's a space
                    node.psiVector['blankPix'] += 1


    def xGivenYTrue(self, node):
        xGivenYTrue = 0
        for j in node.psiVector:
            if xGivenYTrue == 0:
                xGivenYTrue = self.psiXandYTrue(node, j) / self.p_Y[node.label]
            else:
                xGivenYTrue *= self.psiXandYTrue(node, j) / self.p_Y[node.label]
        return xGivenYTrue

    def psiXandYTrue(self, node, j):
        count = 0
        for n in self.instances:
            if n.psiVector[j] == node.psiVector[j] and n.label == node.label:
                count += 1
        return count

    def xGivenYFalse(self, node):
        xGivenYFalse = 0
        for j in node.psiVector:
            if xGivenYFalse == 0:
                xGivenYFalse = self.psiXandYFalse(instances, node, j) /self.complement(instances, self.p_Y[node.label])
            else:
                xGivenYFalse *= self.psiXandYFalse(instances, node, j) / self.complement(instances, self.p_Y[node.label])
        return xGivenYFalse

    def psiXandYFalse(self, node, j):
        count = 0
        for n in self.instances:
            if n.psiVector[j] == node.psiVector[j] and n.label != node.label:
                count += 1
        return count

    def complement(self, num):
        return len(self.instances) - float(num)

    @staticmethod
    def liklihoodRatio(xGivenYTrue, yTrue, xGivenYFalse, yFalse):
        liklihoodRatio = (xGivenYTrue * yTrue) / (xGivenYFalse * yFalse)
        return liklihoodRatio >= 1

    def train(self):
        print("placeholder")

if __name__ == '__main__':
    relpath = os.path.dirname(__file__)
    srcx = os.path.join(relpath, r'data/digitdata/trainingimages')
    srcy = os.path.join(relpath, r'data/digitdata/traininglabels')
    data = list()  # complete dataset
    labels = list()
    Scan.scanIn(srcx, srcy, data, labels)
    instances = Scan.randomSelect(0.001, data, labels)
    bayes = NaiveBayes(instances)
    yEstimate = bayes.probY()
    bayes.psiFunc()
    for i in bayes.instances:
        print(i.psiVector)
    print(bayes.p_Y)
    for u in bayes.p_Y:
        print(bayes.complement(bayes.p_Y[u]))
    #for i in instances:


