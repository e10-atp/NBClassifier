import os, math, random, collections
from Node import Node

class Train:

    @staticmethod
    def scanIn(srcx, srcy, data, labels):

        def emptyLine(line):
            return line.strip() == ''

        def sanitize(data):
            for s in data:
                if len(s) < 28 * 6:  # 6-10 is a valid range for digit training
                    data.remove(s)

        fx = open(str(srcx), 'r')
        emptyFlag = True
        for line in fx:
            if emptyLine(line):
                emptyFlag = True
                continue
            else:
                if emptyFlag:
                    emptyFlag = False
                    data.append(line)
                else:
                    data[-1] += line
        sanitize(data)
        fx.close()
        fy = open(str(srcy), 'r')
        for line in fy:
            labels.append(line.strip())
        fy.close()

    @staticmethod
    def randomSelect(rate, data, labels, instances):  # insert number between 0 and 1
        lim = math.ceil(len(data) * rate)
        for i in range(0, lim):
            randnum = random.randint(0, len(data) - 1)
            instances.append(Node(data[randnum], labels[randnum]))


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
    def mapPsiVectors(instances):
        for node in instances:
            node.psiList.append(NaiveBayes.psiFunc(node))

    @staticmethod
    def psiFunc(node): #number of + and # over total pixels in line
        psiVector = {
            'blankPix': 0,
            'filledPix': 0
        }
        for c in node.image:
            if c == '+' or c == '#':
                psiVector['filledPix'] += 1
            elif c == '\n':
                continue
            else: #if it's a space
                psiVector['blankPix'] += 1
        return psiVector

    @staticmethod
    def xGivenY(psiList, yEstimate):
        #this needs to be rewritten
        values = collections.OrderedDict()
        for vector in psiList:
            for index in vector:
                if index not in values:
                    values[str(index)] = 1
                else:
                    values[str(index)] += 1
        return values



if __name__ == '__main__':
    relpath = os.path.dirname(__file__)
    srcx = os.path.join(relpath, r'data/digitdata/trainingimages')
    srcy = os.path.join(relpath, r'data/digitdata/traininglabels')
    data = list()  # complete dataset
    labels = list()
    Train.scanIn(srcx, srcy, data, labels)
    instances = list()
    Train.randomSelect(0.001, data, labels, instances)
    yEstimate = NaiveBayes.estimateYTrue(instances)
    NaiveBayes.mapPsiVectors(instances)
    for i in instances:
        for j in i.psiList:
            print(j)
    print(yEstimate)
