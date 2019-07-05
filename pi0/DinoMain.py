# Python libraries
from time               import *  # Time library
import os
import sys
import serial

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

try:
   from gpiozero   import CPUTemperature
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - CPUTemperature library not loaded.")


THERMAL_CONTROL_PERIOD = 10 # Unit: 1/10 sec 
MAXBUFFER = 200
NUMDATAFIELDS = 21
PORTNAME = '/dev/serial0'
BAUDRATE = 115200
TIMEOUT = 0.02


DINO_STATE_INIT       = 0
DINO_STATE_START_EXP  = 1
DINO_STATE_EXPERIMENT = 2
DINO_STATE_END_EXP    = 3
DINO_STATE_FINISHED   = 4


FLIGHT_DATA = {'flight_event': 0, 
                'exptime': 0,
                'altitude': 0,
                'gps_altitude': 0,
                'velocity': [0,0,0],
                'acc_magnitude': 0,
                'acceleration': [0,0,0],
                'attitude': [0,0,0],
                'angular_velocity': [0,0,0],
                'warnings': [0,0,0,0]}

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
         DinoMain._dinoSerial  = DinoSerial('/dev/serial0')
         DinoMain._dinoSpectrometer = DinoSpectrometer()
         DinoMain._dinoServo   = DinoServo(SERVO_PIN)
         DinoMain._dinoServo.hardStopServo()


         #initialize the spectrometer
         DinoMain._dinoSpectrometer.initialize()
         
         # Initialize sensor data tuple
         DinoMain._data        = [None,] * I_SIZE

         # Experiment state
         DinoMain._currState   = DINO_STATE_INIT
         DinoMain._prevState   = DINO_STATE_INIT

         # Flag to decimate thermal algorithm
         DinoMain._thermalCount = 0

         # Flag to terminate the test
         DinoMain._endTest     = False


      return DinoMain.__instance


   def _readAllData(self):
      """
      Read/parse serial data and all sensors from Envirophat.
      Store a tuple of sensor readings with "False" 
      for any fields that could not be read.
      """
      flight_event = FLIGHT_DATA['flight_event']#self._dinoSerial.readData()
      flight_altitude = FLIGHT_DATA['altitude']
      flight_acceleration = FLIGHT_DATA['acceleration']
      tempEnv    = self._dinoEnv.readData()
      #print('flight_state =')
      #print(flight_state)

      self._data[I_FLIGHT_STATE]    = flight_event#tempSerial[NR_FLIGHT_STATE]
      self._data[I_ALTITUDE]        = flight_altitude #tempSerial[NR_ALTITUDE]
      self._data[I_ACCELERATION]    = flight_acceleration #tempSerial[NR_ACCELERATION]
      self._data[I_LIGHT_RED]       = tempEnv[ENV_HAT_LIGHT_RED]
      self._data[I_LIGHT_GREEN]     = tempEnv[ENV_HAT_LIGHT_GREEN]
      self._data[I_LIGHT_BLUE]      = tempEnv[ENV_HAT_LIGHT_BLUE]
      self._data[I_LIGHT_CLEAR]     = tempEnv[ENV_HAT_LIGHT_CLEAR]
      self._data[I_TEMPERATURE]     = tempEnv[ENV_HAT_TEMPERATURE]
      self._data[I_PRESSURE]        = tempEnv[ENV_HAT_PRESSURE]
      self._data[I_ACCEL_X]         = tempEnv[ENV_HAT_ACCEL_X]
      self._data[I_ACCEL_Y]         = tempEnv[ENV_HAT_ACCEL_Y]
      self._data[I_ACCEL_Z]         = tempEnv[ENV_HAT_ACCEL_Z]
    
   def parse_serial_packet(self, incoming_data):
    # Remove leading or trailing white space and separate the fields.
    incoming_data = incoming_data.strip()
    fields = incoming_data.split(',')

    # Ensure that the appropriate number of data fields are present.
    if len(fields) != NUMDATAFIELDS:
        return False
    else:
        index = 0
        for field in fields:
            if index == 0:
                FLIGHT_DATA['flight_event'] = field
            elif index == 1:
                FLIGHT_DATA['exptime'] = float(field)
            elif index == 2:
                FLIGHT_DATA['altitude'] = float(field)
            elif index == 3:
                FLIGHT_DATA['gps_altitude'] = float(field)
            elif index == 4:
                FLIGHT_DATA['velocity'][0] = float(field)
            elif index == 5:
                FLIGHT_DATA['velocity'][1] = float(field)
            elif index == 6:
                FLIGHT_DATA['velocity'][2] = float(field)
            elif index == 7:
                FLIGHT_DATA['acc_magnitude'] = float(field)
            elif index == 8:
                FLIGHT_DATA['acceleration'][0] = float(field)
            elif index == 9:
                FLIGHT_DATA['acceleration'][1] = float(field)
            elif index == 10:
                FLIGHT_DATA['acceleration'][2] = float(field)
            elif index == 11:
                FLIGHT_DATA['attitude'][0] = float(field)
            elif index == 12:
                FLIGHT_DATA['attitude'][1] = float(field)
            elif index == 13:
                FLIGHT_DATA['attitude'][2] = float(field)
            elif index == 14:
                FLIGHT_DATA['angular_velocity'][0] = float(field)
            elif index == 15:
                FLIGHT_DATA['angular_velocity'][1] = float(field)
            elif index == 16:
                FLIGHT_DATA['angular_velocity'][2] = float(field)
            elif index == 17:
                FLIGHT_DATA['warnings'][0] = int(field)
            elif index == 18:
                FLIGHT_DATA['warnings'][1] = int(field)
            elif index == 19:
                FLIGHT_DATA['warnings'][2] = int(field)
            elif index == 20:
                FLIGHT_DATA['warnings'][3] = int(field)
            index = index + 1
        return True
    
    
  
   def _determineState(self):
      """
      Determine the state of the experiment.
      """
      # Record previous state. 
      self._prevState = self._currState
      
      
      # Logic to determine the current experiment state
      strState = self._data[I_FLIGHT_STATE]
      try:
       nrState = NR_STATE_LETTERS.index(strState)
      except:
        DinoLog.logMsg("Errpr in Conversion to String")
        return self._prevState

      #print('strState = ',strState)
      
      
      if(nrState < NR_STATE_COAST_START):          #NR_STATE_MECO
         self._currState = DINO_STATE_INIT
         
      elif(nrState < NR_STATE_COAST_END):          #NR_STATE_DROGUE_CHUTES
         if(self._currState == DINO_STATE_INIT):
            self._currState = DINO_STATE_START_EXP
         else:
            self._currState = DINO_STATE_EXPERIMENT
            
      elif(nrState < NR_STATE_TOUCHDOWN):  
         self._currState = DINO_STATE_END_EXP    
         
      else:
         self._currState = DINO_STATE_FINISHED

      # Capture state transitions in the log
      if(self._prevState != self._currState):
         DinoLog.logMsg("Transitioned to state=" + str(self._currState))
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
      if(self._thermalCount > THERMAL_CONTROL_PERIOD):
         self._thermalCount = 0
      else:
         self._thermalCount = self._thermalCount + 1
         return False
      
      # Determine temperature

      if (self._data[I_TEMPERATURE] is not None):
         # Read temperature from EnviroPHat
         temperature = self._data[I_TEMPERATURE]
         #temperature = TURN_ON_HEATER - 10 #test
         print("EVPHAT:temperature = ", temperature)
      elif(self._data[I_ALTITUDE] is not None):

         # Convert altitude to meters
         altitudeInMeters = self._data[I_ALTITUDE] * FEET_TO_METER

         # Compute the temperature based on the altitude

         # Troposphere
         if(altitudeInMeters < MAX_ALTITUDE_TROPOSPHERE):
            temperature = TROPOSPHERE_OFFSET + TROPOSPHERE_GAIN * altitudeInMeters
            temperature = round(temperature,2)
            altitudeInMeters = round(altitudeInMeters,2)
            #print("Altitude = ", altitudeInMeters, "Temperature =", temperature)
         # Lower stratosphere
         elif(altitudeInMeters < MAX_ALTITUDE_LOWER_STRATOSPHERE):
            temperature = LOWER_STRATOSPHERE_OFFSET + LOWER_STRATOSPHERE_GAIN * altitudeInMeters
            temperature = round(temperature,2)
            altitudeInMeters = round(altitudeInMeters,2)
            #print("Altitude = ", altitudeInMeters, "Temperature =", temperature)
         # Upper stratosphere
         else:
            temperature = UPPER_STRATOSPHERE_OFFSET + UPPER_STRATOSPHERE_GAIN * altitudeInMeters
            temperature = round(temperature,2)
            altitudeInMeters = round(altitudeInMeters,2)
            #print("Altitude = ", altitudeInMeters, "Temperature =", temperature)
      else:
         # Read CPU temperature and use that as an approximation
        try:
         cpu = CPUTemperature()
         temperature = cpu.temperature + CPU_TEMP_OFFSET
         temperature = round(temperature,2)
         print("CPU Temperature =", temperature)
        except:
         DinoLog.logMsg("ERROR - Could Not Read CPU Temperature.")
         print("Could not read CPU temperature")


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

      return True

   def run(self):
    try:
      ser = serial.Serial(port=PORTNAME, baudrate=BAUDRATE, timeout=TIMEOUT)
    except:
      DinoLog.logMsg("ERROR - Failed To Open Serial Port.")
      print("Failed To Open Serial Port")
      #self._dinoSerial.openSerialPort()
    while(self._endTest == False):
         #print("Reading the USB serial port")
         #Read all sensor data and serial data

          # Run thermal algorithm
         try:
          self._runThermalControl()  #need to run thermal control even before communication with NRFF
         except:
          DinoLog.logMsg("ERROR - Failed Thermal Control.")
          print("Failed Thermal Control")

         try:
          currMet = DinoTime.getMET()
         except:
           DinoLog.logMsg("ERROR - Could Not Read MET")
           print("Could Not Read MET")

         try:
          data_in = ser.read(MAXBUFFER)
         except:
          DinoLog.logMsg("ERROR - Could Not Read Serial Port")
          print("Could Not Read Serial Port")

         if (len(data_in) == 0):
            #print("Waiting For Serial Data")
            #print(currMet)
            tempEnv    = self._dinoEnv.readData()
            self._data[I_TEMPERATURE]     = tempEnv[ENV_HAT_TEMPERATURE]
            continue

        # Check that packet was well formatted.
         try:
          if not self.parse_serial_packet(data_in.decode('utf-8')):
            continue
         except:
             DinoLog.logMsg("ERROR - Could not decode serial data.")
             continue
        
         print(data_in)
         self._readAllData()
         DinoLog.logData(self._data)
         # Determine experiment state
         self._determineState()

         # Run thermal algorithm
         #self._runThermalControl()

         if(self._currState == DINO_STATE_INIT):
            pass

         elif(self._currState == DINO_STATE_START_EXP):
            self._dinoServo.restartServo()
            self._dinoCamera.startRecording(duration=CAMERA_REC_DURATION)
            self._dinoServo.startServo(SERVO_AGITATION_INTERVAL)
            self._dinoSpectrometer.startCapturing(SPECTROMETER_CAPTURE_INTERVAL)

            
         elif(self._currState == DINO_STATE_EXPERIMENT):
            pass
            
         elif(self._currState == DINO_STATE_END_EXP):
            #stop the servo low level oscillation
            self._dinoServo.hardStopServo()
            #stop the threads
            self._dinoCamera.stopRecording()
            self._dinoServo.stopServo()
            self._dinoSpectrometer.stopCapturing()
                        
         else:
            self._endTest = True
            self._dinoServo.stopServo()

         
         # Sleep for 0.05sec. By the time it wakes up, 
         # there should be serial data readily available.
         sleep(0.1)
         

