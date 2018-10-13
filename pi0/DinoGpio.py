from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from gpiozero   import LED        # GPIO interface
   from gpiozero   import PWMOutputDevice
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - GPIO not loaded.")


class DinoGpio(object):

   __instance = None

   """ Singleton instance. """
   def __new__(cls, servoPin, heaterPin, coolerPin):
      if(DinoGpio.__instance is None):
         DinoGpio.__instance = object.__new__(cls)
      return DinoGpio.__instance


   def startServo(self, duration, speed):
      pass
   
   def heaterOn(self):
      pass
   
   def heaterOff(self):
      pass
      
   def coolearOn(self):
      pass
      
   def coolearOff(self):
      pass
      
   
