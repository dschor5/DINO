try:
   from gpiozero   import LED        # GPIO interface
   from gpiozero   import PWMOutputDevice
except:
   print("ERROR - GPIO not loaded.")


from DinoTime import *
from DinoLog  import *


class DinoGpio:

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
      
   
