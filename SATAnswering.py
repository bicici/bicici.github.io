
'''
Author: Mehmet Ergun Bicici
This program uses a matrix of frequency/entopy/data conversion values and a table for mapping
SAT question pairs to rows. 

Reads newrow2pair.out and entroDenseClean.out files and attempts to answer the SAT similarity
questions found in SAT-package2.txt by using the cosine measure. 

'''

import sys
import string
import re
import os
#import sets
import random
import time
import math

def tokenizeString (str, StrTokenTerms):
	lenTokens = len(StrTokenTerms)
	index = 0
	while (index < lenTokens):
		char = StrTokenTerms[index:index+1]
		wordlist = str.split(char)
		str = ""
		for word in wordlist:
			str = str + word
		index = index + 1
	return str
	
def Set2List(aSet):
	aList = []
	for item in aSet:
		aList.append(item)
	return aList

# Allows the use of multiple values per key in a dictionary    
def keyplus(dic,key,value):
	dic.setdefault(key, [])
	if value not in dic[key]:
		dic[key].append(value)

# For the sorting of attributes to work, 
# we need the same number of digits for numbering
def clearAttribute(attribute):
	#print attribute
	if (attribute == '') or (attribute == ';'):
		return ''
	attrTemp = attribute.split('attr')
	# attrTemp = ['', 'num']
	#print attrTemp
	addZero = 4 - len(attrTemp[1]) # 4 digits are used for attribute numbering
	if addZero == 3:
		attr = '000' + attrTemp[1]
	elif addZero == 2:
		attr = '00' + attrTemp[1]
	elif addZero == 1:
		attr = '0' + attrTemp[1]
	else:
		attr = attrTemp[1]
	attr = 'attr' + attr
	return attr
	
# For the sorting of objects to work, 
# we need the same number of digits for numbering
def clearObject(object):
	objTemp = object.split('obj')
	# attrTemp = ['', 'num']
	addZero = 5 - len(objTemp[1]) # 5 digits are used for attribute numbering
	if addZero == 4:
		obj = '0000' + objTemp[1]
	elif addZero == 3:
		obj = '000' + objTemp[1]
	elif addZero == 2:
		obj = '00' + objTemp[1]
	elif addZero == 1:
		obj = '0' + objTemp[1]
	else:
		obj = objTemp[1]
	obj = 'obj' + obj
	
	return obj

# In case the memory is not enough for loading the entire file, getLine function might be needed. 
'''
def getLine(filename, lineNum):

'''

# Finds the cosinus of the angle between two vectors
# u.v = |u|.|v|.cos(Theta)
def cosScore(qwp, awp):
	global dictRowPairs
	global dictMatrix

	# Need to check if the value is found in the dictionary
	# If not, return 0
	print 'qwp: ' + qwp + ' -- ' + 'awp: ' + awp 
	try:
		rowQ = dictMatrix[int(dictRowPairs[qwp])]
		print 'QrowNum: ' + dictRowPairs[qwp]
		#print rowQ
		rowQList = rowQ.split(' ')
	except KeyError: 
		print 'Error'
		return 0

	try: 
		rowA = dictMatrix[int(dictRowPairs[awp])]
		print 'ArowNum: ' + dictRowPairs[awp]
		#print rowA
		rowAList = rowA.split(' ')
	except KeyError:
		print 'Error'
		return 0
	
	# Vector multiplication
	vmult = 0.0
	# Vectors are the same length
	for i in range(len(rowQList)):
		vmult = vmult + float(rowQList[i]) * float(rowAList[i])
	
	cosTheta = vmult / (vectorNorm2(rowQList) * vectorNorm2(rowAList))

	return cosTheta

# Returns the Vector 2 Norm
def vectorNorm2(vect):
	norm = 0
	for i in range(len(vect)):
		norm = norm + float(vect[i]) * float(vect[i])

	return math.sqrt(norm)

# Calculate the average of the scores of the alternate word pairs that are greater
# of equal to the score of the original pair. 
def cosAvgScore(Qwp, Awp):
	global dictPairAlter
	global RowPairsKeys

	thresholdScore = cosScore(Qwp, Awp)
	print 'threshold: ' + str(thresholdScore)
	
	Qalter = dictPairAlter[Qwp]
	try: 
		Aalter = dictPairAlter[Awp]
	except KeyError:
		Aalter = []

	#Qalter.append(Qwp)
	#Aalter.append(Awp)
	
	sum = 0
	count = 0
	#print str(Qalter) + ' === ' + str(Aalter)
	for qalt in Qalter:
		if qalt not in RowPairsKeys:
			continue
		for aalt in Aalter:
			if aalt not in RowPairsKeys:
				continue
			score = cosScore(qalt, aalt)
			print 'Score: ' + str(score)
			if score >= thresholdScore:
				sum = sum + score
				count = count + 1

	if count > 0:
		return sum / count
	else :
		return thresholdScore


# For each file in the current path
#currpath = os.getcwd()
#print currpath
#path = currpath + '\HTMLFiles'
#outpath = currpath + '\CleanedHTMLFiles'
#print 'Cleaned HTML files'

#global WordSet
#global AllWordSet

#AllWordSet = sets.Set([])

#print "Usage: SparseMatrixConversionSubsets outputFilename.con threshold"
#filename = sys.argv[1] 
# For discretizing the data
#threshold = float(sys.argv[2])
#subsets = int(sys.argv[3])

#outfp = open('results.out', 'wb')


# Data matrix: 8128 x 8000
inputFileMatrix = open("entroDenseClean.out", 'rb')
# Row -> wordpair mapping
inputFileRows = open("newrow2pair.out", 'rb')
# List of SAT questions
inputFileSAT = open("SAT-package2.txt", 'rb')
# List of alternate word pairs
inputFileAlter = open("filter_alternates.out", 'rb')

# Read wordpairs to rows mapping
# Stores the new mapping of keys
dictRowPairs = {}

while 1:
	s = inputFileRows.readline()
	if not s:
		break

	s = s.strip()
	lst = s.split(' ')
	dictRowPairs[lst[1] + ' ' + lst[2]] = lst[0]
	

inputFileRows.close()

RowPairsKeys = dictRowPairs.keys()

# Stores SAT questions in the form: 
# [[question, answer1, answer2, answer3, answer4, answer5, correctChoice], [], ...]
listSATQuestions = []

while 1:
	s = inputFileSAT.readline() # Redundant line
	if not s:
		break

	question = []
	# Question
	s = inputFileSAT.readline()
	s = s.strip()
	lst = s.split('\t')
	question.append(lst[0] + ' ' + lst[1])

	# Answer a
	s = inputFileSAT.readline()
	s = s.strip()
	lst = s.split('\t')
	question.append(lst[0] + ' ' + lst[1])
	
	# Answer b
	s = inputFileSAT.readline()
	s = s.strip()
	lst = s.split('\t')
	question.append(lst[0] + ' ' + lst[1])

	# Answer c
	s = inputFileSAT.readline()
	s = s.strip()
	lst = s.split('\t')
	question.append(lst[0] + ' ' + lst[1])

	# Answer d
	s = inputFileSAT.readline()
	s = s.strip()
	lst = s.split('\t')
	question.append(lst[0] + ' ' + lst[1])

	# Answer e
	s = inputFileSAT.readline()
	s = s.strip()
	lst = s.split('\t')
	question.append(lst[0] + ' ' + lst[1])
	
	# Correct Answer
	s = inputFileSAT.readline()
	s = s.strip()
	question.append(s)

	listSATQuestions.append(question)
	s = inputFileSAT.readline()

inputFileSAT.close()

# Read alternative word pairs
# Stores the new mapping of keys
dictPairAlter = {}

while 1:
	
	s = inputFileAlter.readline()
	if not s:
		break
	
	s = s.strip()
	lst = s.split(' ')
	origPair = lst[0] + ' ' + lst[1]
	keyplus(dictPairAlter, origPair, origPair)
	
	while not (s == '-----'):
		s = inputFileAlter.readline()
		#print s	
		s = s.strip()
		if s == '-----':
			break
		lst = s.split(' ')
		#print origPair + ' **** ' + lst
		keyplus(dictPairAlter, origPair, lst[0] + ' ' + lst[1])

inputFileAlter.close()

# Read the wordpair vectors
# Stores the data matrix (8128 x 8000)
dictMatrix = {}

rowNum = 0
while 1:
	s = inputFileMatrix.readline()
	if not s:
		break

	s = s.strip()
	dictMatrix[rowNum] = s
	rowNum = rowNum + 1

inputFileMatrix.close()

''' TEST FOR ERRORS
question = listSATQuestions[0]
for i in range(len(question)-1):
	qwp = question[i]
	try: 
		rowNum = dictRowPairs[qwp]
		print qwp + ' is in row ' + str(rowNum)
		rowQ = dictMatrix[int(dictRowPairs[qwp])]	
		print rowQ + '+++'
	except KeyError:
		print qwp + ' is not found'

'''

questNum = 0
correctNum = 0
# Answer Questions
for quest in listSATQuestions:
	print 'Question: ' + str(questNum)
	print quest
	scores = {}
	Qwp = quest[0]
	Aawp = quest[1]
	Abwp = quest[2]
	Acwp = quest[3]
	Adwp = quest[4]
	Aewp = quest[5]
	ans = quest[6]

	'''
	# If the original pair is not in the newrow2Pair matrix, 
	# then calculate an average vector by calculating the average
	# vector out of the alternate pairs. 
	if Qwp not in RowPairsKeys:
		
	'''
	
	scores['a'] = cosAvgScore(Qwp, Aawp)
	scores['b'] = cosAvgScore(Qwp, Abwp)
	scores['c'] = cosAvgScore(Qwp, Acwp)
	scores['d'] = cosAvgScore(Qwp, Adwp)
	scores['e'] = cosAvgScore(Qwp, Aewp)
	
	maxScore = 0
	maxAns = ''
	for key in scores.iterkeys():
		print key + ': ' + str(scores[key])
		if scores[key] > maxScore:
			maxScore = scores[key]
			maxAns = key
	
	print maxAns + ' - ' + ans
	if maxAns == ans:
		correctNum = correctNum + 1
		print 'Correct'
	else:
		print 'Incorrect'

	questNum = questNum + 1
	
print "Correct answers: " + str(correctNum) + " out of " + str(questNum) + " questions"
print "Percentage correct: " + str(100 * correctNum / questNum)

#outfp.close()
