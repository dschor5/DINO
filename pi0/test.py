from time       import *
import os
import sys
from testUtils  import *

printHeading("Start test (" + strftime("%Y%m%d-%H%M%S") + ")")
from DinoTime   import *
from DinoLog    import *
from DinoCamera import *


def testDinoTime():

	# Test variables
	testName = "DinoTime"
	testDesc = ""
 
	testDesc = "Initialize class"		
	obj1 = DinoTime()
	testNotEquals(testName, testDesc, obj1, None)

	testDesc = "Test singleton"
	obj2 = DinoTime()
	testEquals(testName, testDesc, obj2, obj1)

	testDesc = "Check calculated METs at 10Hz."
	for i in range(10):
		refMet = DinoTime.getMET()
		sleep(i / 10)
		met = DinoTime.getMET()
		testEquals(testName, testDesc, met-refMet, i / 10, 0.1)

	testDesc = "Check calculated METs at 1Hz."
	for i in range(5):
		refMet = DinoTime.getMET()
		sleep(i)
		met = DinoTime.getMET()
		testEquals(testName, testDesc, met-refMet, i, 0.01)


def testDinoLog():
	global folder

	# Test variables
	testName = "DinoLog"
	testDesc = ""

	# Already initialized.  
	testDesc = "Test singleton"
	obj1 = DinoLog(folder, "results-diff-1")
	obj2 = DinoLog(folder, "results-diff-2")
	testEquals(testName, testDesc, obj1, obj2)

	# Log message + data files
	# Attempt to close the file and ensure it is re-opened
	# Parse back last 5 entries of each type and confirm they are working
	

def testDinoCamera():
	global folder

	# Test variables
	testName = "DinoCamera"
	testDesc = ""
 
	testDesc = "Initialize class"		
	camObj = DinoCamera(folder, "video")
	testNotEquals(testName, testDesc, camObj, None)

	testDesc = "Test singleton"
	obj2 = DinoCamera(folder, "video-diff")
	testEquals(testName, testDesc, obj2, camObj)

	testDesc = "Check PiCamera default recording mode=OFF."
	testEquals(testName, testDesc, camObj.isRecording(), False)	

	testDesc = "PiCamera start recording."
	status = camObj.startRecording()
	testEquals(testName, testDesc, status, True)	

	testDesc = "PiCamera created file=[" + camObj.getFilename() + "]"
	status = os.path.exists(camObj.getFilename())
	testEquals(testName, testDesc, status, True)

	testDesc = "Check PiCamera recording mode."
	testEquals(testName, testDesc, camObj.isRecording(), True)	

	testDesc = "Don't start recording when one is already in progress."
	status = camObj.startRecording()
	testEquals(testName, testDesc, status, False)

	sleep(5)

	testDesc = "PiCamera stop recording."
	recTime = camObj.stopRecording()
	testEquals(testName, testDesc, camObj.isRecording(), False)	

	testDesc = "Recorded for more than 5 sec."
	testGreaterThan(testName, testDesc, recTime, 5)

	# Start and stop recordings every 5 seconds to baseline
	# the overhead for creating/saving files. 
	recStartStatus = []
	recStartTime = []
	recDuration  = []
	recStopTime  = []
	duration = 5	

	for i in range(6):
		recStartStatus.append(camObj.startRecording())
		recStartTime.append(DinoTime.getMET())
		sleep(duration)
		recDuration.append(camObj.stopRecording())
		recStopTime.append(DinoTime.getMET())
	
	# Check the results of the previous tests.
	for i in range(5):
		testDesc = "PiCamera started rec #" + str(i) + "."
		testEquals(testName, testDesc, recStartStatus[i], True)
		testDesc = "PiCamera stopped rec #" + str(i) + "."
		testEquals(testName, testDesc, recDuration[i]>0, True)
		testDesc = "PiCamera rec #" + str(i) + " duration. "
		testInRange(testName, testDesc, recDuration[i], duration-0.01, duration+0.01)
		testDesc = "Check time between recordings."
		testLessThan(testName, testDesc, recStartTime[i+1]-recStopTime[i], 0.01)


# Configuration for test
folder = "test_logs"

# Initialize time system
DinoTime()
DinoLog(folder, "results")

printHeading("Test DinoTime class")
testDinoTime()

printHeading("Test DinoLog class")
testDinoLog()

printHeading("Test DinoCamera class")
testDinoCamera()

