import numpy, math


class Regression:

    @staticmethod
    def makeLists(image):
        xList = list()
        yList = list()
        lines = image.split('\n')
        for y in range(0, len(lines)):
            for x in range(0, len(lines[y])):
                if lines[y][x] != ' ':
                    xList.append(x)
                    yList.append(y)
        return xList, yList

    @staticmethod
    def findRegression(xList, yList):
        if len(xList) != len(yList):
            raise Exception('Regression: List lengths not equal')
        xBar = numpy.mean(xList)
        yBar = numpy.mean(yList)
        xyBar = Regression.xyBar(xList, yList)
        x2Bar = Regression.x2Bar(xList)
        xBar2 = math.pow(xBar, 2)
        m = (xBar * yBar - xyBar) / (xBar2 - x2Bar)
        yIntercept = yBar - m * xBar
        return m, yIntercept

    @staticmethod
    def xyBar(xList, yList):
        xy = list()
        for i in range(0, len(xList)):
            xy.append(xList[i] * yList[i])
        return numpy.mean(xy)

    @staticmethod
    def x2Bar(xList):
        x2 = list()
        for x in xList:
            x2.append(math.pow(x, 2))
        return numpy.mean(x2)
