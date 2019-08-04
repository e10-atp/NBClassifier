from train import Train
import os, math, random

class percepNum:
	weights = [0,0,0,0,0]

	@staticmethod
    def perceptron(trainList, feature1, feature2, feature3, feature4):#each feature is an array
    	done = 0
    	featureList = [feature1, feature2, feature3, feature4]
    	for i in trainList:#trainList would be an array of all the training numbers
    		equation = weights[0] + weights[1]*feature1[i] + weights[2]*feature2[i] + weights[3]*feature3[i] + weights[4]*feature4[i]

    		if (equation >= 0 and y[i] == true) or (equation < 0 and y[i] == false) :
    			done = done + 1
    			if done >= numOfNumbers:
    				break
    		else if equation < 0 and y[i] == true:
    			weights[0] = weights[0] + 1
    			for j in weights:
    				if j>0:
    					weights[j] = weights[j] + featureList[j-1][i]
			else if equation >= 0 and y[i] == false:
    			weights[0] = weights[0] - 1
    			for j in weights:
    				if j>0:
    					weights[j] = weights[j] - featureList[j-1][i]