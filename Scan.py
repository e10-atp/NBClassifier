import math, random
from Node import Node


class Scan:

    @staticmethod
    def scanIn(srcx, srcy, rate):
        data = list()
        labels = list()
        fx = open(str(srcx), 'r')
        emptyFlag = True
        for line in fx:
            if Scan.emptyLine(line):
                emptyFlag = True
                continue
            else:
                if emptyFlag:
                    emptyFlag = False
                    data.append(line)
                else:
                    data[-1] += line
        fx.close()
        Scan.sanitize(data)
        fy = open(str(srcy), 'r')
        for line in fy:
            labels.append(line.strip())
        fy.close()
        return Scan.randomSelect(data, labels, rate)

    @staticmethod
    def emptyLine(line):
        return line.strip() == ''

    @staticmethod
    def sanitize(data):
        for s in data:
            if len(s) < 28 * 6:  # 6-10 is a valid range for digit training
                data.remove(s)

    @staticmethod
    def randomSelect(data, labels, rate):  # insert number between 0 and 1
        samples = []
        lim = math.ceil(len(data) * rate)
        for i in range(0, lim):
            randnum = random.randint(0, len(data) - 1)
            samples.append(Node(data[randnum], labels[randnum]))
        return samples