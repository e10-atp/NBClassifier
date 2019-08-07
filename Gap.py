import numpy, copy

class Gap:

    @staticmethod
    def horizontal(image):
        splitImage = image.split('\n')
        del splitImage[-1]
        gapList = list()
        for i in splitImage:
            if i.strip() == '':
                continue
            flag = False
            count = 0
            prev = None
            gapList.append(0)
            for c in i:
                if c == ' ' and flag is False:
                    if prev != ' ' and prev is not None:
                        count += 1
                        flag = True
                elif c == ' ' and flag is True:
                    count += 1
                elif c != ' ' and flag is False:
                    prev = c
                    continue
                elif c != ' ' and flag is True:
                    flag = False
                    gapList[-1] = count
                else:
                    prev = c
                    continue
                prev = c
        #deltas = list()
        #for i in range(1, len(gapList)):
        #    deltas.append(gapList[i] - gapList[i - 1])
        return numpy.mean(gapList)

    @staticmethod
    def vertical(image):
        splitImage = image.split('\n')
        del splitImage[-1]
        lineCount = len(splitImage)
        lineSize = len(splitImage[0])
        gapList = list()
        for c in range(0, lineSize):
            if Gap.columnBlank(splitImage, c, lineCount):
                continue
            flag = False
            count = 0
            prev = None
            gapList.append(0)
            for i in range(0, lineCount):
                if splitImage[i][c] == ' ' and flag is False:
                    if prev != ' ' and prev is not None:
                        count += 1
                        flag = True
                elif splitImage[i][c] == ' ' and flag is True:
                    count += 1
                elif splitImage[i][c] != ' ' and flag is False:
                    prev = splitImage[i][c]
                    continue
                elif splitImage[i][c] != ' ' and flag is True:
                    flag = False
                    gapList[-1] = count
                else:
                    prev = splitImage[i][c]
                    continue
                prev = splitImage[i][c]
        #deltas = list()
        #for i in range(1, len(gapList)):
        #    deltas.append(gapList[i] - gapList[i - 1])
        return numpy.mean(gapList)

    @staticmethod
    def columnBlank(image, column, colSize):
        flag = True
        for i in range(0, colSize):
            if image[i][column] != ' ':
                flag = False
                return flag
        return flag