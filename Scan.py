import math, random
from Node import Node
from itertools import islice


class Scan:

    @staticmethod
    def scanIn(srcx, srcy, height, rate):
        data = list()
        with open(str(srcx), 'r') as fx:
            while True:
                image = list(islice(fx, height))
                if not image: #EOF
                    break
                image = ''.join(image)
                data.append(image)
        fx.close()
        fy = open(str(srcy), 'r')
        labels = list()
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
            if len(s.split('\n')) < 7:  # 7-10 is a valid range for digit training
                data.remove(s)

    @staticmethod
    def randomSelect(data, labels, rate):  # insert number between 0 and 1
        samples = []
        lim = math.ceil(len(data) * rate)
        for i in range(0, lim):
            randnum = random.randint(0, len(labels) - 1)
            samples.append(Node(data[randnum], labels[randnum]))
        return samples