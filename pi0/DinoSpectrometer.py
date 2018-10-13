from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   pass   
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - Spectrometer interface not loaded.")
   

class DinoSpectrometer(object):

   __instance = None

   """ Singleton instance. """
   def __new__(cls):
      if(DinoSpectrometer.__instance is None):
         DinoSpectrometer.__instance = object.__new__(cls)
      return DinoSpectrometer.__instance


