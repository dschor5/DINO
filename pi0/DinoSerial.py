from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   pass
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - Serial interface not loaded.")


class DinoSerial(object):

   __instance = None

   """ Singleton instance. """
   def __new__(cls):
      if(DinoSerial.__instance is None):
         DinoSerial.__instance = object.__new__(cls)
         DinoSerial.__
      return DinoSerial.__instance

   @staticmethod
   def __readSerialThread():
      pass