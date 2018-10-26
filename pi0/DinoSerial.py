from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from serial     import *        # Serial communication
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - Serial interface not loaded.")


class DinoSerial(object):

   __instance = None
   

   # Field names within the New Shepard packet received at 10Hz.
   # From: NR-BLUE-W0001 (RevA) Feather Frame Payload User's Guide (002).pdf

   # Current flight state as a single ASCII char. 
   # States defined in FLIGHT_STATES enum above.
   I_FLIGHT_STATE = 0  
   
   # Current experiment time in seconds as decimal 
   # number with 2 digits following the decimal point.
   I_EXP_TIME = 1

   # Current vehicle altitude above ground level in feet as a 
   # decimal number with 6 digits following the decimal point.
   I_ALTITUDE = 2         

   # Current vehicle velocity in feet per second along the three 
   # axis of the capsule as a decimal number with 6 digits following
   # the decimal point.
   I_VELOCITY_X = 3           
   I_VELOCITY_Y = 4
   I_VELOCITY_Z = 5

   # Magnitude of the current vehicle acceleration in feet per 
   # second squared as a decimal number with 6 digits 
   # following the decimal point.
   I_ACCELERATION = 6

   # Reserved for future use. Expect "0.000000".
   I_RESERVED_1 = 7
   I_RESERVED_2 = 8

   # The current vehicle attitude in radians about the three axis 
   # as a decimal number with 6 digits following the decimal point.
   I_ATTITUDE_X = 9
   I_ATTITUDE_Y = 10
   I_ATTITUDE_Z = 11
   
   # Current vehicle angular velocity in radians per second
   # about the three axis as a decimal number with 6 digits following 
   # the decimal point.
   I_ANG_VEL_X = 12
   I_ANG_VEL_Y = 13
   I_ANG_VEL_Z = 14

   # Warnings triggered for different phases of the flight. 
   # Suingle digit value set to 1 when the warning is TRUE and 0 when FALSE.
   I_WARNING_LIFTOFF = 15  # Triggered on main engine ignition
   I_WARNING_RCS     = 16  # Triggered during microgravity phase of flight to notify
   I_WARNING_ESCAPE  = 17  # Triggered during the escape motor ignition process
   I_WARNING_CHUTE   = 18  # Triggered shortly before drogue chute deployments
   I_WARNING_LANDING = 19  # Triggered by altitude shortly before the capsule touches down
   I_WARNING_FAULT   = 20  # Triggered in anticipation of an abnormally hard landing


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
            

      return temp

      
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
      
