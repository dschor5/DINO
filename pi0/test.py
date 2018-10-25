from   time import *
import os
import sys

from DinoConstants import *  # Project constants
from DinoTestUtils import *  # Test utilities

printHeading("Start initialization (" + strftime("%Y%m%d-%H%M%S") + ")")

from DinoTime           import *  # Time keeping (Real-time + MET)
from DinoLog            import *  # Logging features
from DinoCamera         import *  # PiCamera interface
from DinoEnvirophat     import *  # Envirophat interface
from DinoServo          import *  # Servo interface
from DinoSerial         import *  # Serial data interface
from DinoThermalControl import *  # GPIO interface for heater and cooler
from DinoSpectrometer   import *  # Spectrometer interface

printHeading("End initialization (" + strftime("%Y%m%d-%H%M%S") + ")")
printHeading("Start test (" + strftime("%Y%m%d-%H%M%S") + ")")


def testDinoTime():

   # Test variables
   testName = "DinoTime"
   testDesc = ""
 
   printSubheading(testName, "Initialization") 

   testDesc = "Initialize class"      
   obj1 = DinoTime()
   testNotNone(testName, testDesc, obj1)

   testDesc = "Test singleton"
   obj2 = DinoTime()
   testEquals(testName, testDesc, obj2, obj1)

   printSubheading(testName, "Test 10Hz timing")
   testDesc = "Check calculated METs at 10Hz."
   for i in range(10):
      refMet = DinoTime.getMET()
      sleep(i / 10)
      met = DinoTime.getMET()
      testEquals(testName, testDesc, met-refMet, i / 10, 0.01)

   printSubheading(testName, "Test 1Hz timing")
   testDesc = "Check calculated METs at 1Hz."
   for i in range(5):
      refMet = DinoTime.getMET()
      sleep(i)
      met = DinoTime.getMET()
      testEquals(testName, testDesc, met-refMet, float(i), 0.01)

   printSubheading(testName, "Test time jump.")
   
   testDesc = "Reject backwards time jump."
   status = DinoTime.setTime(DinoTime.getMET() - 10.0)
   testIsFalse(testName, testDesc, status)
   
   testDesc = "Jump by 0sec < threshold for applying jump."
   status = DinoTime.setTime(DinoTime.getMET())
   testIsFalse(testName, testDesc, status)
   
   testDesc = "Jump time 10sec into the future."
   refMet = DinoTime.getMET()
   status = DinoTime.setTime(DinoTime.getMET() + 10.0)
   newMet = DinoTime.getMET()
   testEquals(testName, testDesc, newMet-refMet, 10.0, 0.01)


def testDinoLog():

   # Test variables
   testName = "DinoLog"
   testDesc = ""

   printSubheading(testName, "Initialization")

   # Already initialized.  
   testDesc = "Test singleton"
   obj1 = DinoLog("results-diff-1")
   obj2 = DinoLog("results-diff-2")
   testEquals(testName, testDesc, obj1, obj2)

   # Log message + data files
   # Attempt to close the file and ensure it is re-opened
   # Parse back last 5 entries of each type and confirm they are working
   

def testDinoCamera():

   # Test variables
   testName = "DinoCamera"
   testDesc = ""
   
   printSubheading(testName, "Initialization") 

   testDesc = "Initialize class"      
   camObj = DinoCamera("video")
   testNotNone(testName, testDesc, camObj)

   testDesc = "Test singleton"
   obj2 = DinoCamera("video-diff")
   testEquals(testName, testDesc, obj2, camObj)

   testDesc = "Check PiCamera default recording mode=OFF."
   testEquals(testName, testDesc, camObj.isRecording(), False) 

   testDesc = "Check number of recordings on boot."
   testEquals(testName, testDesc, camObj.getNumRecordings(), 0)  

   printSubheading(testName, "Invalid recording modes")
   testDesc = "PiCamera start recording with duration < " + str(DinoCamera.MIN_DURATION) + "."
   status = camObj.startRecording(duration=(DinoCamera.MIN_DURATION-1))
   testEquals(testName, testDesc, status, False)  

   testDesc = "PiCamera start recording with duration > " + str(DinoCamera.MAX_DURATION) + "."
   status = camObj.startRecording(duration=(DinoCamera.MAX_DURATION+1))
   testEquals(testName, testDesc, status, False)  

   stopRecMET = DinoTime.getMET()
   testDesc = "PiCamera stop recording when nothing is in progress."
   status = camObj.stopRecording()
   testEquals(testName, testDesc, status, False)   

   printSubheading(testName, "Test single recording mode")
   testDesc = "PiCamera start recording."
   startRecMET = DinoTime.getMET()
   status = camObj.startRecording(duration=5)
   testEquals(testName, testDesc, status, True)   
   
   sleep(1)
   
   testDesc = "Check PiCamera recording in progress."
   testEquals(testName, testDesc, camObj.isRecording(), True)   

   testDesc = "Don't start recording when one is already in progress."
   status = camObj.startRecording()
   testEquals(testName, testDesc, status, False)

   while(camObj.isRecording() == True):
      sleep(1)

   stopRecMET = DinoTime.getMET()
   testDesc = "PiCamera stop recording."
   status = camObj.stopRecording()
   testEquals(testName, testDesc, status, False)   

   testDesc = "Recorded for more than 5 sec."
   testGreaterThan(testName, testDesc, (stopRecMET - startRecMET), 5.0)

   testDesc = "Check number of recordings on boot."
   testEquals(testName, testDesc, camObj.getNumRecordings(), 1)  

   printSubheading(testName, "Test command to stop recording.")

   testDesc = "PiCamera start recording."
   startRecMET = DinoTime.getMET()
   status = camObj.startRecording(duration=60)
   testEquals(testName, testDesc, status, True)   
   
   testDesc = "Check PiCamera recording mode."
   testEquals(testName, testDesc, camObj.isRecording(), True)   

   sleep(1)

   stopRecMET = DinoTime.getMET()
   testDesc = "PiCamera stop recording."
   status = camObj.stopRecording()
   testEquals(testName, testDesc, status, False)   

   testDesc = "Recorded for less than 5 sec."
   testLessThan(testName, testDesc, (stopRecMET - startRecMET), 5.0)

   testDesc = "Check number of recordings on boot."
   testEquals(testName, testDesc, camObj.getNumRecordings(), 2) 

   while(camObj.isRecording() == True):
      sleep(1)

   printSubheading(testName, "Test continuous recording mode")

   testDesc = "PiCamera start continuous recording."
   startRecMET = DinoTime.getMET()   
   status = camObj.startRecording(single=False, duration=DinoCamera.MIN_DURATION)
   testEquals(testName, testDesc, status, True)   

   testDesc = "Check PiCamera recording mode."
   testEquals(testName, testDesc, camObj.isRecording(), True)   

   if(status == True):
      sleep(DinoCamera.MIN_DURATION * 4)

   testDesc = "Check PiCamera recording mode (after 5 * MIN_DURATION)."
   testEquals(testName, testDesc, camObj.isRecording(), True)   
      
   stopRecMET = DinoTime.getMET()
   testDesc = "PiCamera stop recording."
   status = camObj.stopRecording()
   testEquals(testName, testDesc, status, False)   

   testDesc = "Recorded for more than 20 sec."
   testGreaterThan(testName, testDesc, (stopRecMET - startRecMET), 20.0)

   testDesc = "Check number of recordings since boot."
   testEquals(testName, testDesc, camObj.getNumRecordings(), 6)  

   
   

def testDinoEnvirophat():
   # Test variables
   testName = "DinoEnvirophat"
   testDesc = ""
 
   printSubheading(testName, "Initialization")

   testDesc = "Initialize class"      
   env = DinoEnvirophat()
   testNotNone(testName, testDesc, env)

   testDesc = "Test singleton"
   obj2 = DinoEnvirophat()
   testEquals(testName, testDesc, obj2, env)
 
   # Run through a loop of tests. 
   numTests = 4
   delayBetweenTests = 2.5
   for i in range(1, numTests+1):
   
      printSubheading(testName, "Test reading sensors " + str(i) + " of " + str(numTests) + ".")

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

   
def testDinoThermalControl():
   # Test variables
   testName = "DinoThermalControl"
   testDesc = ""
   
   IDLE_TEMP = (TURN_OFF_HEATER + TURN_OFF_COOLER) / 2

   printSubheading(testName, "Initialization")

   testDesc = "Initialize class"      
   thermal = DinoThermalControl(HEATER_PIN, COOLER_PIN)
   testNotNone(testName, testDesc, thermal)

   testDesc = "Test singleton"
   obj2 = DinoThermalControl(HEATER_PIN, COOLER_PIN)
   testEquals(testName, testDesc, obj2, thermal)

   thermalState = thermal.getState()
   testDesc = "Default state for "
   testEquals(testName, testDesc + " heater is OFF", thermalState[DinoThermalControl.STATE_HEATER], False)
   testEquals(testName, testDesc + " cooler is OFF", thermalState[DinoThermalControl.STATE_COOLER], False)

   printSubheading(testName, "Turn heater ON for 10 seconds")

   thermalState = thermal.run(TURN_ON_HEATER - 1)
   testDesc = "Temperature=" + '{0:.1f}'.format(TURN_ON_HEATER - 1)
   testEquals(testName, testDesc + " heater is ON ",  thermalState[DinoThermalControl.STATE_HEATER], True)
   testEquals(testName, testDesc + " cooler is OFF", thermalState[DinoThermalControl.STATE_COOLER], False)

   sleep(1)

   thermalState = thermal.run(IDLE_TEMP)
   testDesc = "Temperature=" + '{0:.1f}'.format(IDLE_TEMP)
   testEquals(testName, testDesc + " heater is OFF", thermalState[DinoThermalControl.STATE_HEATER], False)
   testEquals(testName, testDesc + " cooler is OFF", thermalState[DinoThermalControl.STATE_COOLER], False)

   printSubheading(testName, "Turn cooler ON for 10 seconds")

   thermalState = thermal.run(TURN_ON_COOLER + 1)
   testDesc = "Temperature=" + '{0:.1f}'.format(TURN_ON_COOLER + 1)
   testEquals(testName, testDesc + " heater is OFF", thermalState[DinoThermalControl.STATE_HEATER], False)
   testEquals(testName, testDesc + " cooler is ON ",  thermalState[DinoThermalControl.STATE_COOLER], True)

   sleep(1)

   thermalState = thermal.run(IDLE_TEMP)
   testDesc = "Temperature=" + '{0:.1f}'.format(IDLE_TEMP)
   testEquals(testName, testDesc + " heater is OFF", thermalState[DinoThermalControl.STATE_HEATER], False)
   testEquals(testName, testDesc + " cooler is OFF", thermalState[DinoThermalControl.STATE_COOLER], False)
  
   printSubheading(testName, "Test thermal control logic")

   for i in range(3):
      currTemp  = round(TURN_ON_HEATER - 2)
      while(currTemp < round(TURN_ON_COOLER + 2)):
         currTemp = currTemp + 0.5
         thermalState = thermal.run(currTemp)
         print(testName + " - Temperature=" + '{0:.1f}'.format(currTemp) + " --> " + \
            "HeaterOn=" + str(thermalState[DinoThermalControl.STATE_HEATER]) + ", " + \
            "CoolerOn=" + str(thermalState[DinoThermalControl.STATE_COOLER]))

      currTemp  = round(TURN_ON_COOLER + 2)
      while(currTemp < round(TURN_ON_HEATER - 2)):
         currTemp = currTemp - 0.5
         thermalState = thermal.run(currTemp)
         print(testName + " - Temperature=" + '{0:.1f}'.format(currTemp) + " --> " + \
            "HeaterOn=" + str(thermalState[DinoThermalControl.STATE_HEATER]) + ", " + \
            "CoolerOn=" + str(thermalState[DinoThermalControl.STATE_COOLER]))

def testDinoServo():
   # Test variables
   testName = "DinoServo"
   testDesc = ""
   period = 4
   
   printSubheading(testName, "Initialization")

   testDesc = "Initialize class"      
   srv = DinoServo(SERVO_PIN)
   testNotNone(testName, testDesc, srv)

   testDesc = "Test singleton"
   obj2 = DinoServo(SERVO_PIN)
   testEquals(testName, testDesc, obj2, srv)   
   
   testDesc = "Check servo default agitating=OFF."
   testEquals(testName, testDesc, srv.isAgitating(), False) 

   printSubheading(testName, "Invalid agitating periods")
   testDesc = "Agitate servo with period < " + str(DinoServo.MIN_PERIOD) + "."
   status = srv.startServo(period=(DinoServo.MIN_PERIOD-1))
   testEquals(testName, testDesc, status, False)  

   testDesc = "Agitate servo with period > " + str(DinoServo.MAX_PERIOD) + "."
   status = srv.startServo(period=(DinoServo.MAX_PERIOD+1))
   testEquals(testName, testDesc, status, False)  

   stopRecMET = DinoTime.getMET()
   testDesc = "Stop servo when nothing is in progress."
   status = srv.stopServo()
   testEquals(testName, testDesc, status, False)   

   printSubheading(testName, "Test servo operation")

   testDesc = "Start servo with period = " + str(period) + "."
   startRecMET = DinoTime.getMET()   
   status = srv.startServo(period)
   testEquals(testName, testDesc, status, True)   

   testDesc = "Check servo is agitating."
   testEquals(testName, testDesc, srv.isAgitating(), True)   

   if(status == True):
      sleep(period * 3)

   testDesc = "Check servo is still agitating (after 3 * period)."
   testEquals(testName, testDesc, srv.isAgitating(), True)   
      
   stopRecMET = DinoTime.getMET()
   testDesc = "Stop servo."
   status = srv.stopServo()
   testEquals(testName, testDesc, status, False)   

   testDesc = "Check servo is not agitating."
   testEquals(testName, testDesc, srv.isAgitating(), False)  


def testDinoSerial():
   # Test variables
   testName = "DinoSerial"
   testDesc = ""
 
   printSubheading(testName, "Initialization")

   testDesc = "Initialize class"      
   rPort = DinoSerial('/dev/ttyAMA0')
   testNotNone(testName, testDesc, rPort)

   testDesc = "Test singleton"
   obj2 = DinoSerial('/dev/ttyAMA0')
   testEquals(testName, testDesc, obj2, rPort)   
   
   printSubheading(testName, "Fail to read sync byte.")
   #TODO - Start loopback program that writes numbers
      
   
   
def testDinoSpectrometer():
   # Test variables
   testName = "DinoSpectrometer"
   testDesc = ""
   print("No tests defined.")


# Initialize time system
DinoTime()
DinoLog("test", debugEnable=True)

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

if((len(sys.argv) == 1) or ("DinoThermalControl" in sys.argv)):
   printHeading("Test DinoThermalControl class")
   testDinoThermalControl()

if((len(sys.argv) == 1) or ("DinoServo" in sys.argv)):
   printHeading("Test DinoServo class")
   testDinoServo()

if((len(sys.argv) == 1) or ("DinoSerial" in sys.argv)):
   printHeading("Test DinoSerial class")
   testDinoSerial()

if((len(sys.argv) == 1) or ("DinoSpectrometer" in sys.argv)):
   printHeading("Test DinoSpectrometer class")
   testDinoSpectrometer()

printHeading("End test (" + strftime("%Y%m%d-%H%M%S") + ")")
printResults()
