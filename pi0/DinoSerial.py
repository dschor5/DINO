from threading     import Thread # Thread to record continuously
from threading     import RLock  # Note re-entrant lock
from threading     import Event  # Events for communicating within threads

from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from serial     import *        # Serial communication
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - Serial interface not loaded.")


# Field names within the New Shepard packet received at 10Hz.
# From: NR-BLUE-W0001 (RevA) Feather Frame Payload User's Guide (002).pdf
NR_FLIGHT_STATE    = 0     # Current flight state as a single ASCII char. 
NR_EXP_TIME        = 1     # Current experiment time in seconds as decimal 
                           # number with 2 digits following the decimal point.
NR_ALTITUDE        = 2     # Current vehicle altitude above ground level in feet as a 
                           # decimal number with 6 digits following the decimal point.
NR_VELOCITY_X      = 3     # Current vehicle velocity in feet per second along the three          
NR_VELOCITY_Y      = 4     # axis of the capsule as a decimal number with 6 digits following
NR_VELOCITY_Z      = 5     # the decimal point.
NR_ACCELERATION    = 6     # Magnitude of the current vehicle acceleration in feet per  
                           # second squared as a decimal number with 6 digits 
                           # following the decimal point.
NR_RESERVED_1      = 7     # Reserved for future use. Expect "0.000000".
NR_RESERVED_2      = 8 
NR_ATTITUDE_X      = 9     # The current vehicle attitude in radians about the three axis 
NR_ATTITUDE_Y      = 10    # as a decimal number with 6 digits following the decimal point.
NR_ATTITUDE_Z      = 11  
NR_ANG_VEL_X       = 12    # Current vehicle angular velocity in radians per second
NR_ANG_VEL_Y       = 13    # about the three axis as a decimal number with 6 digits following
NR_ANG_VEL_Z       = 14    # the decimal point.   
# Warnings triggered for different phases of the flight. 
# Single digit value set to 1 when the warning is TRUE and 0 when FALSE.
NR_WARNING_LIFTOFF = 15    # Triggered on main engine ignition
NR_WARNING_RCS     = 16    # Triggered during microgravity phase of flight to notify
NR_WARNING_ESCAPE  = 17    # Triggered during the escape motor ignition process
NR_WARNING_CHUTE   = 18    # Triggered shortly before drogue chute deployments
NR_WARNING_LANDING = 19    # Triggered by altitude shortly before the capsule touches down
NR_WARNING_FAULT   = 20    # Triggered in anticipation of an abnormally hard landing
NR_SIZE            = 21  

# Possible flight states sent by New Shepard vehicle to the payload.
# From: NR-BLUE-W0001 (RevA) Feather Frame Payload User's Guide (002).pdf
NR_STATE_NONE        = 0   # @  No flight state has been reached yet 
                           #    (typically the time prior to liftoff).
NR_STATE_LIFTOFF     = 1   # A  This state is triggered once sensed acceleration 
                           #    first changes due to engine ignition.
NR_STATE_MECO        = 2   # B  This state is triggered after the rocket's main engine 
                           #    cuts out, and the flight enters its coast stage.
NR_STATE_SEPARATION  = 3   # C  This state occurs after the rocket and capsule 
                           #    separate, shortly before the microgravity 
                           #    portion of the flight begins.
NR_STATE_COAST_START = 4  # D  This state indicates the beginning of the cleanest 
                           #    microgravity operations onboard the capsule, 
                           #    most experiments should begin logging data at this time.
NR_STATE_APOGEE      = 5   # E  This state occurs when the vehicle has reached its 
                           #    maximum altitude and begins to descend.
NR_STATE_COAST_END   = 6   # F  This state indicates the end of microgravity operations 
                           #    onboard the capsule, as we begin to experience 
                           #    atmospheric accelerations. Many experiments will 
                           #    cease logging data at this time.
NR_STATE_UNDER_CHUTE = 7   # G  This state indicates that drogue parachutes have 
                           #    deployed and the capsule is in its final descent.
NR_STATE_LANDING     = 8   # H  This state occurs after capsule touchdown.
NR_STATE_SAFING      = 9   # I  After touchdown, this state indicates that the 
                           #    capsule is venting and safing all energetic systems.
NR_STATE_FINISHED    = 10  # J  This state is only ever reached in simulation and 
                           #    indicates the end of the logged flight data.
NR_STATE_MISSION_END = 13  # M  Mission End: ‘M’ = This event is triggered once the CC has finished performing 
                           #    its post-flight safing procedure. This is the last flight event that NanoLabs can
                           #    use to close out their experiments prior to being powered down. It is recommended 
                           #    to close out your experiment prior to reaching this flight event, as there may be 
                           #    less than a second before power is lost.   
NR_STATE_LETTERS = "@ABCDEFGHIJKLM"  


class DinoSerial(object):

   __instance = None
   



   """
   PORT_NAME = '/dev/ttyAMA0'
   BAUD_RATE = 115200
   PARITY    = serial.PARITY_NONE
   STOP_BITS = serial.STOPBITS_ONE
   BYTE_SIZE = serial.EIGHTBITS
   TIMEOUT   = 0.1 # 10 Hz packets 
   """
   
   # Maximum number of bytes/characters before a sync byte. 
   # If this is observed, then we have a communication problem. 
   MAX_MSG_LENGTH = 200
   

   """ Singleton instance. """
   def __new__(cls, portName):
      if(DinoSerial.__instance is None):
         DinoSerial.__instance = object.__new__(cls)
         DinoSerial.__serialPort = None
         DinoSerial.__data = [None] * NR_SIZE

         # Create lock object to protect shared resources.
         try:
            DinoSerial.__copyLock = RLock()
         except:
            DinoLog.logMsg("ERROR - Could not create lock to serial copy data.")

         # Create event to notify reading thread when to stop.
         # While this could have been done with a lock, the event 
         # has built in functions for checking if a flag is set.
         try:
            DinoSerial.__stop = Event()
            DinoSerial.__stop.set()
         except:
            DinoLog.logMsg("ERROR - Could not create event for serial thread.")            
            
      return DinoSerial.__instance

   def startReading(self, habFlight=False):
      """
      Start reading serial data. 
      
      The flag is used for the HAB configuration only as it needs to 
      send a character over the serial port before it begins the 
      transmissions. In flight, this flag should be set to false. 
      
      Parameters
      ----------
      habFlight : bool
         False for HAB flights only. 
      """
      
      if(habFlight == True):
         pass
      
   def __openSerialPort(self):
      """
      Open the serial port. 
      
      Return
      ------
      bool
         True on success. False otherwise.
      """
      # Serial port settings. 
      # From: NR-BLUE-W0001 (RevA) Feather Frame Payload User's Guide (002).pdf
      try:
         self.__serialPort = serial.Serial(
            port        = self.PORT_NAME,
            baudrate    = self.BAUD_RATE,
            parity      = self.PARITY,
            stopbits    = self.STOP_BITS,
            bytesize    = self.BYTE_SIZE,
            timeout     = self.TIMEOUT
            )
      except:
         self.__serialPort = None
         DinoLog.logMsg("ERROR - Could not open serial port.")
      
   def readData(self):
      self.__data[NR_FLIGHT_STATE]    = "@"
      self.__data[NR_EXP_TIME]        = DinoTime.getMET()
      self.__data[NR_ALTITUDE]        = 0.0
      self.__data[NR_VELOCITY_X]      = 0.0      
      self.__data[NR_VELOCITY_Y]      = 0.0     
      self.__data[NR_VELOCITY_Z]      = 0.0      
      self.__data[NR_ACCELERATION]    = 0.0      
      self.__data[NR_RESERVED_1]      = 0.0      
      self.__data[NR_RESERVED_2]      = 0.0     
      self.__data[NR_ATTITUDE_X]      = 0.0     
      self.__data[NR_ATTITUDE_Y]      = 0.0      
      self.__data[NR_ATTITUDE_Z]      = 0.0      
      self.__data[NR_ANG_VEL_X]       = 0.0      
      self.__data[NR_ANG_VEL_Y]       = 0.0      
      self.__data[NR_ANG_VEL_Z]       = 0.0      
      self.__data[NR_WARNING_LIFTOFF] = 0     
      self.__data[NR_WARNING_RCS]     = 0     
      self.__data[NR_WARNING_ESCAPE]  = 0     
      self.__data[NR_WARNING_CHUTE]   = 0     
      self.__data[NR_WARNING_LANDING] = 0     
      self.__data[NR_WARNING_FAULT]   = 0     
      return self.__data

      
   def __closeSerialPort(self):
      pass
      
   def __resetSerialPort(self):
      """
      Flush serial port input buffer. 
      """
      self.__serialPort.reset_input_buffer()
      

   def __findSyncByte(self):
      """
      Find the sync byte (a character A-J or @ that represents 
      the state of the vehicle/hab and return it. Special cases:
      - If this character is not found after MAX_MSG_LENGTH bytes, 
        then reset the serial port and start again. 
      - If there is no data available by the TIMEOUT period, 
        then return None.
      
      Returns
      -------
      str 
         Sync character of None if it failed to read a value.
      """
      countChars = 0
      syncByte = serialPort.read()
      while((syncByte is not None) and (syncByte not in HAB_STATES)):
         countChars = countChars + 1
         if(countChars > MAX_MSG_LENGTH):
            countChars = 0
            self.__resetSerialPort()
         syncByte   = serialPort.read()
      return syncByte
      
      
   def __readSerialThread():
      pass
      
