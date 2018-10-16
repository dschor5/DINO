from   time import *
import os
import sys

from DinoConstants import *  # Project constants
from DinoTestUtils import *  # Test utilities

printHeading("Start initialization (" + strftime("%Y%m%d-%H%M%S") + ")")

from DinoTime         import *  # Time keeping (Real-time + MET)
from DinoLog          import *  # Logging features
from DinoCamera       import *  # PiCamera interface
from DinoEnvirophat   import *  # Envirophat interface
from DinoSerial       import *  # Serial data interface
from DinoGpio         import *  # GPIO interface for servo, heater, and cooler
from DinoSpectrometer import *  # Spectrometer interface

printHeading("End initialization (" + strftime("%Y%m%d-%H%M%S") + ")")
printHeading("Start test (" + strftime("%Y%m%d-%H%M%S") + ")")


def testDinoTime():

   # Test variables
   testName = "DinoTime"
   testDesc = ""
 
   testDesc = "Initialize class"      
   obj1 = DinoTime()
   testNotNone(testName, testDesc, obj1)

   testDesc = "Test singleton"
   obj2 = DinoTime()
   testEquals(testName, testDesc, obj2, obj1)

   testDesc = "Check calculated METs at 10Hz."
   for i in range(10):
      refMet = DinoTime.getMET()
      sleep(i / 10)
      met = DinoTime.getMET()
      testEquals(testName, testDesc, met-refMet, i / 10, 0.01)

   testDesc = "Check calculated METs at 1Hz."
   for i in range(5):
      refMet = DinoTime.getMET()
      sleep(i)
      met = DinoTime.getMET()
      testEquals(testName, testDesc, met-refMet, float(i), 0.01)


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
   testNotNone(testName, testDesc, camObj)

   testDesc = "Test singleton"
   obj2 = DinoCamera(folder, "video-diff")
   testEquals(testName, testDesc, obj2, camObj)

   testDesc = "Check PiCamera default recording mode=OFF."
   testEquals(testName, testDesc, camObj.isRecording(), False) 

   testDesc = "Check number of recordings on boot."
   testEquals(testName, testDesc, camObj.getNumRecordings(), 0)  

   # Test invalid recording modes
   testDesc = "PiCamera start recording with duration < " + str(DinoCamera.MIN_DURATION) + "."
   status = camObj.startRecording(duration=(DinoCamera.MIN_DURATION-1))
   testEquals(testName, testDesc, status, False)  

   testDesc = "PiCamera start recording with duration > " + str(DinoCamera.MAX_DURATION) + "."
   status = camObj.startRecording(duration=(DinoCamera.MAX_DURATION+1))
   testEquals(testName, testDesc, status, False)  

   # Test single recording mode
   print()
   testDesc = "PiCamera start recording."
   startRecMET = DinoTime.getMET()
   status = camObj.startRecording(duration=5)
   testEquals(testName, testDesc, status, True)   
   
   testDesc = "PiCamera created file=[" + camObj.getFilename() + "]"
   status = os.path.exists(camObj.getFilename())
   testEquals(testName, testDesc, status, True)

   testDesc = "Check PiCamera recording mode."
   testEquals(testName, testDesc, camObj.isRecording(), True)   

   testDesc = "Don't start recording when one is already in progress."
   status = camObj.startRecording()
   testEquals(testName, testDesc, status, False)

   while(camObj.isRecording() == True):
      sleep(0.1)

   stopRecMET = DinoTime.getMET()
   testDesc = "PiCamera stop recording."
   camObj.stopRecording()
   testEquals(testName, testDesc, camObj.isRecording(), False)   

   testDesc = "Recorded for more than 5 sec."
   testGreaterThan(testName, testDesc, (stopRecMET - startRecMET), 5.0)

   testDesc = "Check number of recordings on boot."
   testEquals(testName, testDesc, camObj.getNumRecordings(), 1)  

   # Test single recording mode
   print()
   testDesc = "PiCamera start recording."
   startRecMET = DinoTime.getMET()
   status = camObj.startRecording(duration=60)
   testEquals(testName, testDesc, status, True)   
   
   testDesc = "Check PiCamera recording mode."
   testEquals(testName, testDesc, camObj.isRecording(), True)   

   sleep(1)

   stopRecMET = DinoTime.getMET()
   testDesc = "PiCamera stop recording."
   camObj.stopRecording()
   testEquals(testName, testDesc, camObj.isRecording(), False)   

   testDesc = "Recorded for less than 5 sec."
   testLessThan(testName, testDesc, (stopRecMET - startRecMET), 5.0)

   testDesc = "Check number of recordings on boot."
   testEquals(testName, testDesc, camObj.getNumRecordings(), 2) 

   # Test continuous recording mode
   print()
   testDesc = "PiCamera start continuous recording."
   startRecMET = DinoTime.getMET()   
   status = camObj.startRecording(single=False, duration=DinoCamera.MIN_DURATION)
   testEquals(testName, testDesc, status, True)   

   testDesc = "Check PiCamera recording mode."
   testEquals(testName, testDesc, camObj.isRecording(), True)   

   sleep(DinoCamera.MIN_DURATION * 4)

   testDesc = "Check PiCamera recording mode (after 5 * MIN_DURATION)."
   testEquals(testName, testDesc, camObj.isRecording(), True)   
      
   stopRecMET = DinoTime.getMET()
   testDesc = "PiCamera stop recording."
   camObj.stopRecording()
   testEquals(testName, testDesc, camObj.isRecording(), False)   

   testDesc = "Recorded for more than 20 sec."
   testGreaterThan(testName, testDesc, (stopRecMET - startRecMET), 20.0)

   testDesc = "Check number of recordings since boot."
   testEquals(testName, testDesc, camObj.getNumRecordings(), 6)  

   

def testDinoEnvirophat():
   # Test variables
   testName = "DinoEnvirophat"
   testDesc = ""
 
   testDesc = "Initialize class"      
   env = DinoEnvirophat()
   testNotNone(testName, testDesc, env)

   testDesc = "Test singleton"
   obj2 = DinoEnvirophat()
   testEquals(testName, testDesc, obj2, env)
 
   # Run through a loop of tests. 
   for i in range(10):
   
      value = env.getLightSensorReadings()
      testDesc = "Iteration #" + str(i) + " - Check light 'red' channel."
      testNotNone(testName, testDesc, value[0])
      testDesc = "Iteration #" + str(i) + " - Check light 'green' channel."
      testNotNone(testName, testDesc, value[1])
      testDesc = "Iteration #" + str(i) + " - Check light 'blue' channel."
      testNotNone(testName, testDesc, value[2])
      testDesc = "Iteration #" + str(i) + " - Check light 'clear' channel."
      testNotNone(testName, testDesc, value[3])
      
      value = env.getTemperature()
      testDesc = "Iteration #" + str(i) + " - Check temperature."
      testNotNone(testName, testDesc, value)      
      
      value = env.getPressure()
      testDesc = "Iteration #" + str(i) + " - Check pressure."
      testNotNone(testName, testDesc, value)
      
      value = env.getAcceleration()
      testDesc = "Iteration #" + str(i) + " - Check acceleration x channel."
      testNotNone(testName, testDesc, value[0])      
      testDesc = "Iteration #" + str(i) + " - Check acceleration y channel."
      testNotNone(testName, testDesc, value[1])
      testDesc = "Iteration #" + str(i) + " - Check acceleration z channel."
      testNotNone(testName, testDesc, value[2])   
   
      value = env.getMagReading()
      testDesc = "Iteration #" + str(i) + " - Check mag x channel."
      testNotNone(testName, testDesc, value[0])      
      testDesc = "Iteration #" + str(i) + " - Check mag y channel."
      testNotNone(testName, testDesc, value[1])
      testDesc = "Iteration #" + str(i) + " - Check mag z channel."
      testNotNone(testName, testDesc, value[2])   
      
      sleep(1)      

def testDinoSerial():
   print("No tests defined.")
   
def testDinoGpio():
   print("No tests defined.")
   
def testDinoSpectrometer():
   print("No tests defined.")

# Configuration for test
folder = "test_logs"

# Initialize time system
DinoTime()
DinoLog(folder, "results")

if((len(sys.argv) == 1) or ("DinoTime" in sys.argv)):
   printHeading("Test DinoTime class")
   testDinoTime()

if((len(sys.argv) == 1) or ("DinoLog" in sys.argv)):
   printHeading("Test DinoLog class")
   testDinoLog()
   
if((len(sys.argv) == 1) or ("DinoCamera" in sys.argv)):
   printHeading("Test DinoCamera class")
   testDinoCamera()
   
if((len(sys.argv) == 1) or ("DinoEnvirophat" in sys.argv)):
   printHeading("Test DinoEnvirophat class")
   testDinoEnvirophat()

if((len(sys.argv) == 1) or ("DinoSerial" in sys.argv)):
   printHeading("Test DinoSerial class")
   testDinoSerial()

if((len(sys.argv) == 1) or ("DinoGpio" in sys.argv)):
   printHeading("Test DinoGpio class")
   testDinoGpio()

if((len(sys.argv) == 1) or ("DinoSpectrometer" in sys.argv)):
   printHeading("Test DinoSpectrometer class")
   testDinoSpectrometer()

printHeading("End test (" + strftime("%Y%m%d-%H%M%S") + ")")
