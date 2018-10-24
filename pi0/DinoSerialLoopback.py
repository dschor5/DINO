from DinoConstants import *
from DinoTime      import *

try:
   from serial     import *        # Serial communication
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - Serial interface not loaded.")


class DinoSerialLoopback(object):
   """
   Class DinoSerialLoopback
   
   Setup a serial port loopback for testing only. 
   This class cannot log to DinoLog as it is not intended 
   to be used in flights. 
   
   The loopback has configurable states:
    - Sends properly formatted data.
   - 
   """

   # Predefined data sent for unit tests. 
   modeNormal = ( \
         (, 0.1), \
         (, 0.1), \
         
      )
   
   
         0 = Normal
         1 = Timeout between characters. If numMessages > 1, then 
             it will happen on a random charaacter in the last
             message being sent. 
         2 = Timeout between messages. Requires numMessages > 1, 
             such that there is a gap before the last message sent.
         3 = Invalid/unexpected byte found in the string.
             A value other than a digit, decimal point, or comma 
             is sent.
         4 = 



   __instance = None
   
   PORT_NAME = '/dev/ttyAMA0'
   BAUD_RATE = 115200
   PARITY    = serial.PARITY_NONE
   STOP_BITS = serial.STOPBITS_ONE
   BYTE_SIZE = serial.EIGHTBITS
   TIMEOUT   = 0.1 # 10 Hz packets 
   
   # Maximum number of bytes/characters before a sync byte. 
   # If this is observed, then we have a communication problem. 
   MAX_MSG_LENGTH = 200
   

   """ Singleton instance. """
   def __new__(cls, portName):
      if(DinoSerialLoopback.__instance is None):
         DinoSerialLoopback.__instance = object.__new__(cls)
         DinoSerialLoopback.__serialPort = None
                       
      return DinoSerialLoopback.__instance

   def startLoopbackTest(self, testMode, numMessages, habFlight=False):
      """
      Start reading serial data. 
      
      The flag is used for the HAB configuration only as it needs to 
      receive a character over the serial port before it begins the 
      transmissions. In flight, this flag should be set to false. 
      
      Parameters
      ----------
      testMode : int
         Test mode for sending data. Options are:
         0 = Normal
         1 = Timeout between characters. If numMessages > 1, then 
             it will happen on a random charaacter in the last
             message being sent. 
         2 = Timeout between messages. Requires numMessages > 1, 
             such that there is a gap before the last message sent.
         3 = Invalid/unexpected byte found in the string.
             A value other than a digit, decimal point, or comma 
             is sent.
         4 = 
         
      numMessages : int
         Number of messages to send. 
      habFlight : bool
         False for HAB flights only. 
      """
      if(habFlight == True):
         #TODO Receive byte to initiate comms
         pass
      
      # Start thread for reading serial data.
      
      
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
      
      
   def __closeSerialPort(self):
      pass
      

   def __readSerialThread():
      """
      Thread to read the serial data. 
      """