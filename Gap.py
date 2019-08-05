import numpy

class Gap:

    @staticmethod
    def horizontalAvg(image):
        gapList = list()
        flag = False
        for i in image:
            count = 0
            prev = None
            for c in i:
                if c == ' ' and flag is False:
                    if prev != ' ':
                        count += 1
                        flag = True
                elif c == ' ' and flag is True:
                    count += 1
                elif c != ' ' and flag is False:
                    continue
                elif c != ' ' and flag is True:
                    flag = False
                else:
                    continue
                prev = c
            gapList.append(count)
        return numpy.mean(gapList)

    @staticmethod
    def verticalAvg(image):
        splitImage = image.split('\n')
        del splitImage[-1]
        lineCount = len(splitImage)
        lineSize = len(splitImage[0])
        flag = False
        gapList = list()
        for c in range(0, lineSize):
            count = 0
            prev = None
            for i in range(0, lineCount):
                if splitImage[i][c] == ' ' and flag is False:
                    if prev != ' ':
                        count += 1
                        flag = True
                elif splitImage[i][c] == ' ' and flag is True:
                    count += 1
                elif splitImage[i][c] != ' ' and flag is False:
                    continue
                elif splitImage[i][c] != ' ' and flag is True:
                    flag = False
                else:
                    continue
                prev = c
            gapList.append(count)
        return numpy.mean(gapList)
