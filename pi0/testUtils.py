from time import *

firstTime = True

def printHeading(msg):
	global firstTime
	if(firstTime != True):
		print()
	else:
		firstTime = False
	print("***")
	print("* " + str(msg))
	print("***")

def testResult(testName, testDesc, status):
	statusStr = "FAILED"
	if((status is not None) and (status == True)):
		statusStr = "PASSED"
	print(testName + " - " + statusStr + " - " + testDesc)


def testNotNone(testName, testDesc, measured):
	passFail = (measured != None)
	testDesc = testDesc + " " + \
		"Measured=[" + str(measured) + "] "
	testResult(testName, testDesc, passFail)	



def testGreaterThan(testName, testDesc, measured, expected):
	passFail = None
	passFail = (measured > expected)
	testDesc = testDesc + " " + \
		"Measured=[" + str(measured) + "] > " + \
		"Expected=[" + str(expected) + "]"
	testResult(testName, testDesc, passFail)	


def testLessThan(testName, testDesc, measured, expected):
	passFail = None
	passFail = (measured < expected)
	testDesc = testDesc + " " + \
		"Measured=[" + str(measured) + "] < " + \
		"Expected=[" + str(expected) + "]"
	testResult(testName, testDesc, passFail)	


def testInRange(testName, testDesc, measured, minExpected, maxExpected):
	passFail = None
	passFail = (minExpected < measured) and (measured < maxExpected)
	testDesc = testDesc + " " + \
		"MinExpected=[" + str(minExpected) + "] < " \
		"Measured=[" + str(measured) + "] < " + \
		"MaxExpected=[" + str(maxExpected) + "]"
	testResult(testName, testDesc, passFail)	


def testEquals(testName, testDesc, measured, expected, tolerance=0.05):
	passFail = None
	if(isinstance(expected, float) or isinstance(measured, float)):
		passFail = (abs(measured - expected) < tolerance)
		testDesc = testDesc + " " + \
			"Measured=[" + "{0:.4f}".format(measured) + "] " + \
			"Expected=[" + "{0:.4f}".format(expected) + "] " + \
			"Tolerance=[" + "{0:.4f}".format(tolerance) + "]"
	else:
		passFail = (measured == expected)
		testDesc = testDesc + " " + \
			"Measured=[" + str(measured) + "] " + \
			"Expected=[" + str(expected) + "]"
	testResult(testName, testDesc, passFail)	


def testNotEquals(testName, testDesc, measured, expected, tolerance=0.05):
	passFail = None
	if(isinstance(expected, float) or isinstance(measured, float)):
		passFail = (abs(measured - expected) > tolerance)	
		testDesc = testDesc + " " + \
			"Measured=[" + "{0:.4f}".format(measured) + "] " + \
			"Expected=[" + "{0:.4f}".format(expected) + "] " + \
			"Tolerance=[" + "{0:.4f}".format(tolerance) + "]"
	else:
		passFail = (measured != expected)
		testDesc = testDesc + " " + \
			"Measured=[" + str(measured) + "] " + \
			"Expected=[" + str(expected) + "]"
	testResult(testName, testDesc,passFail)
