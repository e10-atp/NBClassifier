import os, math, random, collections


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
            labels.append(line)
        fy.close()

    @staticmethod
    def randomSelect(rate, data, labels, selData, selLabels):  # insert number between 0 and 1
        lim = math.ceil(len(data) * rate)
        for i in range(0, lim):
            randnum = random.randint(0, len(data))
            selData.append(data[randnum])
            selLabels.append(labels[randnum])


class NaiveBayes:

    @staticmethod
    def estimateYTrue(selLabels):
        n = len(selLabels)
        yList = collections.Counter(selLabels)
        for c in yList:
            yList[c] = yList[c] / n
        return yList

    @staticmethod
    def psiVector(selData):
        psiList = list()
        for x in selData:
            psiList.append(NaiveBayes.psiFunc(x))
        return psiList

    @staticmethod
    def psiFunc(x): #number of + and # over total pixels in line
        psiVector = list()
        totalPix = 0
        filledPix = 0
        for c in x:
            if c == '+' or c == '#':
                filledPix += 1
            if c == '\n':
                psiVector.append(filledPix/totalPix)
                filledPix = 0
                totalPix = 0
                continue
            totalPix += 1
        return psiVector


if __name__ == '__main__':
    relpath = os.path.dirname(__file__)
    srcx = os.path.join(relpath, r'data/digitdata/trainingimages')
    srcy = os.path.join(relpath, r'data/digitdata/traininglabels')
    data = list()  # complete dataset
    labels = list()
    selData = list()  # randomly selected data
    selLabels = list()
    Train.scanIn(srcx, srcy, data, labels)
    Train.randomSelect(0.001, data, labels, selData, selLabels)
    yEstimate = NaiveBayes.estimateYTrue(labels)
    psiList = NaiveBayes.psiVector(selData)
    for i in psiList:
        print(i)
