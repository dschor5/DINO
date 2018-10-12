try:
   useStub = False
   
except:
   print("ERROR - Spectrometer not loaded.")
   useStub = True


from DinoTime import *
from DinoLog  import *


class DinoSpectrometer:

   __instance = None

   """ Singleton instance. """
   def __new__(cls):
      if(DinoSpectrometer.__instance is None):
         DinoSpectrometer.__instance = object.__new__(cls)
      return DinoSpectrometer.__instance


