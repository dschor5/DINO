from DinoMain import *

class DinoSim(DinoMain):
   def __new__(cls, dataSource=""):
      DinoSim.__dataSource = dataSource
      DinoSim.__fp = None
      return DinoMain.__new__(cls, "sim")

   

   def _readAllData(self):
      """
      Read/parse serial data and all sensors from Envirophat.
      Store a touple of sensor readings with "False" 
      for any fields that could not be read.
      """

      return [1, 2, 3]
