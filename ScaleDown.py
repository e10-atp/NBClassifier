import math

class ScaleDown:
    @staticmethod
    def scale(image, rate):
        splitImage = image.split('\n')
        del splitImage[-1]
        lineCount = len(splitImage)
        lineSize = len(splitImage[0])
        scaledLines = math.ceil(lineCount * rate)
        scaledSize = math.ceil(lineSize * rate)
        scaledImage = [] #+1 for the newline char
        for i in range(0, scaledLines):
            scaledImage.append([])
            for j in range(0, scaledSize):
                scaledImage[i].append('-1')
        for i in range(0, scaledLines):
            for j in range(0, scaledSize):
                filledCount = 0
                blankCount = 0
                for k in range(int(i / rate), int(i / rate + 1 / rate)):
                    for l in range(int(j / rate), int(j / rate + 1 / rate)):
                        if splitImage[k][l] != ' ':
                            filledCount += 1
                        else:
                            blankCount += 1
                if filledCount >= blankCount:
                    scaledImage[i][j] = '1'
                else:
                    scaledImage[i][j] = '0'
            scaledImage[i].append('\n')
        return scaledImage
