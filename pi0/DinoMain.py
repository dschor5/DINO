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


DINO_STATE_INIT       = 0
DINO_STATE_ASCENT     = 1
DINO_STATE_EXPERIMENT = 2
DINO_STATE_DESCENT    = 3
DINO_STATE_FINISH     = 4


class DinoMain(object):

   # DinoMain Singleton instance 
   __instance = None

   """ Singleton instance. """
   def __new__(cls, filename="results"):
      if(DinoMain.__instance is None):
         DinoMain.__instance = object.__new__(cls)
         DinoThermalControl.__state = [False, False]

         # Initialize time keeping functions + log
         DinoTime()
         DinoLog(filename)   

         # Initialize all other interfaces
         DinoMain._dinoCamera  = DinoCamera("video")
         DinoMain._dinoEnv     = DinoEnvirophat()
         DinoMain._dinoThermal = DinoThermalControl(HEATER_PIN, COOLER_PIN)
         DinoMain._dinoServo   = DinoServo(SERVO_PIN)
         DinoMain._dinoSerial  = DinoSerial('/dev/ttyAMA0')

         # Initialize sensor data touple
         DinoMain._data        = [None,] * I_SIZE

         # Experiment state
         DinoMain._currState   = DINO_STATE_INIT
         DinoMain._prevState   = DINO_STATE_INIT

         # Flag to terminate the test
         DinoMain._endTest     = False

      return DinoMain.__instance


   def _readAllData(self):
      """
      Read/parse serial data and all sensors from Envirophat.
      Store a touple of sensor readings with "False" 
      for any fields that could not be read.
      """
      tempSerial = self._dinoSerial.readData()
      tempEnv    = self._dinoEnv.readData()

      self._data[I_FLIGHT_STATE]    = tempSerial[NR_FLIGHT_STATE]
      self._data[I_ALTITUDE]        = tempSerial[NR_ALTITUDE]
      self._data[I_VELOCITY_X]      = tempSerial[NR_VELOCITY_X]
      self._data[I_VELOCITY_Y]      = tempSerial[NR_VELOCITY_Y]
      self._data[I_VELOCITY_Z]      = tempSerial[NR_VELOCITY_Z]
      self._data[I_ACCELERATION]    = tempSerial[NR_ACCELERATION]
      self._data[I_ATTITUDE_X]      = tempSerial[NR_ATTITUDE_X]
      self._data[I_ATTITUDE_Y]      = tempSerial[NR_ATTITUDE_Y]
      self._data[I_ATTITUDE_Z]      = tempSerial[NR_ATTITUDE_Z]
      self._data[I_ANG_VEL_X]       = tempSerial[NR_ANG_VEL_X]
      self._data[I_ANG_VEL_Y]       = tempSerial[NR_ANG_VEL_Y]
      self._data[I_ANG_VEL_Z]       = tempSerial[NR_ANG_VEL_Z]
      self._data[I_WARNING_LIFTOFF] = tempSerial[NR_WARNING_LIFTOFF]
      self._data[I_WARNING_RCS]     = tempSerial[NR_WARNING_RCS]
      self._data[I_WARNING_ESCAPE]  = tempSerial[NR_WARNING_ESCAPE]
      self._data[I_WARNING_CHUTE]   = tempSerial[NR_WARNING_CHUTE]
      self._data[I_WARNING_LANDING] = tempSerial[NR_WARNING_LANDING]
      self._data[I_WARNING_FAULT]   = tempSerial[NR_WARNING_FAULT]
      self._data[I_LIGHT_RED]       = tempEnv[ENV_HAT_LIGHT_RED]
      self._data[I_LIGHT_GREEN]     = tempEnv[ENV_HAT_LIGHT_GREEN]
      self._data[I_LIGHT_BLUE]      = tempEnv[ENV_HAT_LIGHT_BLUE]
      self._data[I_LIGHT_CLEAR]     = tempEnv[ENV_HAT_LIGHT_CLEAR]
      self._data[I_TEMPERATURE]     = tempEnv[ENV_HAT_TEMPERATURE]
      self._data[I_PRESSURE]        = tempEnv[ENV_HAT_PRESSURE]
      self._data[I_ACCEL_X]         = tempEnv[ENV_HAT_ACCEL_X]
      self._data[I_ACCEL_Y]         = tempEnv[ENV_HAT_ACCEL_Y]
      self._data[I_ACCEL_Z]         = tempEnv[ENV_HAT_ACCEL_Z]
      self._data[I_MAG_X]           = tempEnv[ENV_HAT_MAG_X]
      self._data[I_MAG_Y]           = tempEnv[ENV_HAT_MAG_Y]
      self._data[I_MAG_Z]           = tempEnv[ENV_HAT_MAG_Z]
  

   def _determineState(self):
      """
      Determine the state of the experiment.
      """
      # Record previous state. 
      self._prevState = self._currState
      
      # Logic to determine the current experiment state
      

      # Capture state transitions in the log
      if(self._prevState != self._currState):
         DinoLog.logMsg("Transitioned to state=" + self._currState)
      return self._currState


   def _runThermalControl(self):
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
      # Determine temperature
      if(self._data[I_TEMPERATURE] is not None):
         temperature = self._data[I_TEMPERATURE]
      elif(self._data[I_ALTITUDE] is not None):
         temperature = 0 #TODO
      else:
         temperature = 0 #TODO

      # Control heater
      if(temperature < TURN_ON_HEATER):
         self._dinoThermal.setHeaterState(True)
      else:
         self._dinoThermal.setHeaterState(False)
      
      # Control cooler
      if(temperature > TURN_ON_COOLER):
         self._dinoThermal.setCoolerState(True)
      else:
         self._dinoThermal.setCoolerState(False)
   

   def run(self):



      while(self._endTest == False):

         # Read all sensor data and serial data
         self._readAllData()
         DinoLog.logData(self._data)

         # Determine experiment state
         self._determineState()

         # Run thermal algorithm
         self._runThermalControl()

         # Perform state specific tasks   
         if(self._currState == DINO_STATE_ASCENT or self._currState == DINO_STATE_DESCENT):
            self._dinoCamera.stopRecording()
            self._dinoServo.stopServo()
            #TODO Turn off spectrometer captures

         elif(self._currState == DINO_STATE_FINISH):
            self._endTest = True

         else: # currState == DINO_STATE_EXPERIMENT
            self._dinoCamera.startRecording(False, CAMERA_REC_DURATION)
            self._dinoServo.startServo(SERVO_AGITATION_INTERVAL)
            #TODO Turn on spectrometer captures
         
         # Sleep for 0.05sec. By the time it wakes up, 
         # there should be serial data readily available.
         sleep(0.05)
         
         #TODO 
         self._endTest = True

