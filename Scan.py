import math, random
from Node import Node


class Scan:

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
