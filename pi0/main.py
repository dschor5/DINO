# Python libraries
from time               import *  # Time library
import os
import sys

# Project interfaces
from DinoConstants      import *  # Project constants
from DinoTime           import *  # Time keeping (Real-time + MET)
from DinoLog            import *  # Logging features
from DinoCamera         import *  # PiCamera interface
from DinoEnvirophat     import *  # Envirophat interface
from DinoServo          import *  # Servo interface
from DinoSerial         import *  # Serial data interface
from DinoThermalControl import *  # GPIO interface for heater and cooler
from DinoSpectrometer   import *  # Spectrometer interface


class DinoMain(object):

   # DinoMain Singleton instance 
   __instance = None

   """ Singleton instance. """
   def __new__(cls):
      if(DinoMain.__instance is None):
         DinoMain.__instance = object.__new__(cls)
         DinoThermalControl.__state = [False, False]

         # Initialize time keeping functions + log
         DinoMain.__dinoTime    = DinoTime()
         DinoMain.__dinoLog     = DinoLog("results")    

         # Initialize all other interfaces
         DinoMain.__dinoCamera  = DinoCamera("video")
         DinoMain.__dinoEnv     = DinoEnvirophat()
         DinoMain.__dinoThermal = DinoThermalControl(HEATER_PIN, COOLER_PIN)
         DinoMain.__dinoServo   = DinoServo(SERVO_PIN)
         DinoMain.__dinoSerial  = DinoSerial('/dev/ttyAMA0')

         # Initialize sensor data touple
         DinoMain.__data        = (None, ) * 21 #TODO Use constant

         # Experiment state
         DinoMain.__currState   = "@"
         DinoMain.__prevState   = "@"

         # Flag to terminate the test
         DinoMain.__endTest     = False

      return DinoMain.__instance


   def __readAllData(self):
      """
      Read/parse serial data and all sensors from Envirophat.
      Store a touple of sensor readings with "False" 
      for any fields that could not be read.
      """
      print(self.__dinoSerial.readData())
      #self.__data = self.__dinoSerial.readData() + self.__dinoEnv.readData()


   def __determineState(self):

      # Determine the state and if there was a state transition
      self.__prevState = self.__currState
      
      # Logic to determine the current experiment state
      #TODO

      # Capture state transitions in the log
      self.__currState = "@"
      if(self.__prevState != self.__currState):
         DinoLog.logMsg("Transitioned to state=" + self.__currState)
      return "@"

   def __runThermalControl(self):
      """
      Determine temperature and run thermal control algorithm.

      In case of a sensor failure, the temperature is obtained
      from sensors in priority order:
         1. Envirophat
         2. Computed from elevation received from the serial data
            per https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html.
         3. Estimated from CPU temperature
      
      This function serves as a wrapper for the DinoThermalControl.run()
      so that is can incorporate trending information if needed.
      """
      

      self.__dinoThermal.run()


   def run(self):

      DINO_STATE_ASCENT = "1"
      DINO_STATE_EXPERIMENT = "2"
      DINO_STATE_DESCENT = "3"
      DINO_STATE_FINISH = "4"

      while(self.__endTest == False):

         # Read all sensor data and serial data
         self.__readAllData()
         DinoLog.logdata(self.__data)

         # Determine experiment state
         self.__determineState()

         # Run thermal algorithm
         self.__runThermalControl()

         # Perform state specific tasks   
         if(self.__currState == DINO_STATE_ASCENT or self.__currState == DINO_STATE_DESCENT):
            self.__dinoCamera.stopRecording()
            self.__dinoServo.stopServo()
            #TODO Turn off spectrometer captures

         elif(self.__currState == DINO_STATE_FINISH):
            self.__endTest = True

         else: # currState == DINO_STATE_EXPERIMENT
            self.__dinoCamera.startRecording(False, 60.0)
            self.__dinoServo.startServo(4.0)
            #TODO Turn on spectrometer captures
         
         # Sleep for 0.05sec. By the time it wakes up, 
         # there should be serial data readily available.
         sleep(0.05)
         
         #TODO 
         self.__endTest = True


if(__name__ == "__main__"):
   print("Start test...")
   DinoMain().run()
   print("End test...")

