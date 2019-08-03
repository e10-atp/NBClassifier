import os, math, random, collections
from Node import Node
from Scan import Scan


class NaiveBayes:

    @staticmethod
    def estimateYTrue(instances):
        yList = {}
        for node in instances:
            if node.label not in yList:
                yList[str(node.label)] = 1
            else:
                yList[str(node.label)] += 1
        return yList

    @staticmethod
    def psiFunc(instances):  # number of + and # over total pixels in line
        for node in instances:
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

    @staticmethod
    def xGivenYTrue(instances, yEstimate, node):
        xGivenYTrue = 0
        for j in node.psiVector:
            if xGivenYTrue == 0:
                xGivenYTrue = NaiveBayes.psiXandYTrue(instances, node, j) / yEstimate[str(node.label)]
            else:
                xGivenYTrue *= NaiveBayes.psiXandYTrue(instances, node, j) / yEstimate[str(node.label)]
        return xGivenYTrue

    @staticmethod
    def psiXandYTrue(instances, node, j):
        # need to make false equivalents for these methods
        count = 0
        for n in instances:
            if n.psiVector[j] == node.psiVector[j] and n.label == node.label:
                count += 1
        return count

    @staticmethod
    def xGivenYFalse(instances, yEstimate, node):
        xGivenYFalse = 0
        for j in node.psiVector:
            if xGivenYFalse == 0:
                xGivenYFalse = NaiveBayes.psiXandYTrue(instances, node, j) / NaiveBayes.complement(instances, yEstimate[
                    str(node.label)])
            else:
                xGivenYFalse *= NaiveBayes.psiXandYTrue(instances, node, j) / NaiveBayes.complement(instances,
                                                                                                    yEstimate[str(
                                                                                                        node.label)])
        return xGivenYFalse

    @staticmethod
    def psiXandYFalse(instances, node, j):
        count = 0
        for n in instances:
            if n.psiVector[j] == node.psiVector[j] and n.label != node.label:
                count += 1
        return count

    @staticmethod
    def complement(instances, num):
        return len(instances) - float(num)

    @staticmethod
    def liklihoodRatio(xGivenYTrue, yTrue, xGivenYFalse, yFalse):
        return (xGivenYTrue * yTrue) / (xGivenYFalse * yFalse)

    @staticmethod
    def decideY(liklihoodRatio):
        if liklihoodRatio >= 1:
            return True
        else:
            return False

    @staticmethod
    def yGivenX(xGivenYTrue, yTrue, xGivenYFalse, yFalse):
        Lx = NaiveBayes.liklihoodRatio(xGivenYTrue, yTrue, xGivenYFalse, yFalse)
        if NaiveBayes.decideY(Lx):
            yGivenX = xGivenYTrue * yTrue / Lx
        else:
            yGivenX = xGivenYFalse * yFalse / Lx
        return yGivenX

if __name__ == '__main__':
    relpath = os.path.dirname(__file__)
    srcx = os.path.join(relpath, r'data/digitdata/trainingimages')
    srcy = os.path.join(relpath, r'data/digitdata/traininglabels')
    data = list()  # complete dataset
    labels = list()
    Scan.scanIn(srcx, srcy, data, labels)
    instances = list()
    Scan.randomSelect(0.001, data, labels, instances)
    yEstimate = NaiveBayes.estimateYTrue(instances)
    NaiveBayes.psiFunc(instances)
    for i in instances:
        print(i.psiVector)
    print(yEstimate)
    for u in yEstimate:
        print(NaiveBayes.complement(instances, yEstimate[u]))
