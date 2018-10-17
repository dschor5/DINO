from time import *
from DinoConstants import *

countPass = 0
countFail = 0

def printHeading(msg):
   global COLORS 
   print("\n" + COLORS['HEADING'] + "*** " + str(msg) + COLORS['NORMAL'])

def printSubheading(testName, msg):
   global COLORS 
   print(COLORS['SUBHEADING'] + "*** " + testName + " - " + str(msg) + COLORS['NORMAL'])

def printResults():
   global countPass
   global countFail
   total = countPass + countFail
   percent = 0
   if(total > 0):
      percent = countPass / total * 100
   print("Total " + formatValue(countPass) + " / " + formatValue(total) + " (" + formatValue(percent) + "%) tests passed.")

def formatValue(value):
   valueStr = ""
   if(value is None):
      valueStr = "None"
   elif(type(value) == float or isinstance(value, float)):
      valueStr = '{0:.4f}'.format(value)
   elif(type(value) == bool or type(value) == str or type(value) == int):
      valueStr = str(value)
   elif(isinstance(value, object)):
      valueStr = "0x" + '{:02X}'.format(id(value))
   else:
      valueStr = str(value)
   return COLORS['VALUE'] + valueStr + COLORS['NORMAL']


def testResult(testName, testDesc, status):
   global COLORS
   global countPass
   global countFail
   if((status is not None) and (status == True)):
      statusStr = COLORS['TEST_PASS'] + "PASSED" + COLORS['NORMAL']
      countPass = countPass + 1
   else:
      statusStr = COLORS['TEST_FAIL'] + "FAILED" + COLORS['NORMAL']
      countFail = countFail + 1
   print(testName + " - " + statusStr + " - " + testDesc)


def testNotNone(testName, testDesc, measured):
   global COLORS
   passFail = (measured != None)
   testDesc = testDesc + " Measured=[" + formatValue(measured) + "] "
   testResult(testName, testDesc, passFail)   

def testIsTrue(testName, testDesc, measured):
   global COLORS
   passFail = (measured == True)
   testDesc = testDesc + " Measured=[" + formatValue(measured) + "] "
   testResult(testName, testDesc, passFail)   

def testIsFalse(testName, testDesc, measured):
   global COLORS
   passFail = (measured == False)
   testDesc = testDesc + " Measured=[" + formatValue(measured) + "] "
   testResult(testName, testDesc, passFail)   

def testGreaterThan(testName, testDesc, measured, expected):
   passFail = None
   passFail = (measured > expected)
   if(isinstance(measured, float) or isinstance(expected, float)):
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] > " + \
         "Expected=[" + formatValue(expected) + "]"
   else:
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] > " + \
         "Expected=[" + formatValue(expected) + "]"      
   testResult(testName, testDesc, passFail)   
   
   
def testGreaterThanOrEquals(testName, testDesc, measured, expected):
   passFail = None
   passFail = (measured >= expected)
   if(isinstance(measured, float) or isinstance(expected, float)):
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] >= " + \
         "Expected=[" + formatValue(expected) + "]"
   else:
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] >= " + \
         "Expected=[" + formatValue(expected) + "]"      
   testResult(testName, testDesc, passFail)         


def testLessThan(testName, testDesc, measured, expected):
   passFail = None
   passFail = (measured < expected)
   if(isinstance(measured, float) or isinstance(expected, float)):
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] < " + \
         "Expected=[" + formatValue(expected) + "]"
   else:
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] < " + \
         "Expected=[" + formatValue(expected) + "]"      
   testResult(testName, testDesc, passFail)   


def testLessThanOrEquals(testName, testDesc, measured, expected):
   passFail = None
   passFail = (measured <= expected)
   if(isinstance(measured, float) or isinstance(expected, float)):
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] <= " + \
         "Expected=[" + formatValue(expected) + "]"
   else:
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] <= " + \
         "Expected=[" + formatValue(expected) + "]"      
   testResult(testName, testDesc, passFail)  

def testInRange(testName, testDesc, measured, minExpected, maxExpected):
   passFail = None
   passFail = (minExpected < measured) and (measured < maxExpected)
   if(isinstance(measured, float) or isinstance(minExpected, float) or isinstance(maxExpected, float)):
      testDesc = testDesc + " " + \
         "MinExpected=[" + formatValue(minExpected) + "] < " \
         "Measured=[" + formatValue(measured) + "] < " + \
         "MaxExpected=[" + formatValue(maxExpected) + "]"
   else:
      testDesc = testDesc + " " + \
         "MinExpected=[" + formatValue(minExpected) + "] < " \
         "Measured=[" + formatValue(measured) + "] < " + \
         "MaxExpected=[" + formatValue(maxExpected) + "]"
   testResult(testName, testDesc, passFail)   


def testEquals(testName, testDesc, measured, expected, tolerance=0.05):
   passFail = None
   if(isinstance(expected, float) or isinstance(measured, float)):
      passFail = (abs(measured - expected) < tolerance)
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] " + \
         "Expected=[" + formatValue(expected) + "] " + \
         "Tolerance=[" + formatValue(tolerance) + "]"
   else:
      passFail = (measured == expected)
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] " + \
         "Expected=[" + formatValue(expected) + "]"
   testResult(testName, testDesc, passFail)   


def testNotEquals(testName, testDesc, measured, expected, tolerance=0.05):
   passFail = None
   if(isinstance(expected, float) or isinstance(measured, float)):
      passFail = (abs(measured - expected) > tolerance)   
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] " + \
         "Expected=[" + formatValue(expected) + "] " + \
         "Tolerance=[" + formatValue(tolerance) + "]"
   else:
      passFail = (measured != expected)
      testDesc = testDesc + " " + \
         "Measured=[" + formatValue(measured) + "] " + \
         "Expected=[" + formatValue(expected) + "]"
   testResult(testName, testDesc,passFail)
