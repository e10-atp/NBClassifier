import numpy, copy

class Gap:

    @staticmethod
    def horizontalAvg(image):
        splitImage = image.split('\n')
        del splitImage[-1]
        gapList = list()
        flag = False
        for i in splitImage:
            if i.strip() == '':
                continue
            count = 0
            prev = None
            gapList.append(0)
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
                    gapList[-1] = count
                else:
                    continue
                prev = c
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
            if Gap.columnBlank(splitImage, c, lineCount):
                continue
            count = 0
            prev = None
            gapList.append(0)
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
                    gapList[-1] = count
                else:
                    continue
                prev = c
        return numpy.mean(gapList)

    @staticmethod
    def columnBlank(image, column, colSize):
        flag = True
        for i in range(0, colSize):
            if image[i][column] != ' ':
                flag = False
        return flag