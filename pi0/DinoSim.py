from DinoMain import *

class DinoSim(DinoMain):
   def __new__(cls, dataSource=""):
      DinoSim.__dataSource = dataSource
      DinoSim.__fp = None
      DinoSim.__fp = open(DinoSim.__dataSource, "r")
      return DinoMain.__new__(cls, "sim")



   def _readAllData(self):
      """
      Read/parse serial data and all sensors from Envirophat.
      Store a touple of sensor readings with "False" 
      for any fields that could not be read.
      """
      line = self.__fp.readline()
      parts = line.split(CSV_SEP)

      self._data[I_FLIGHT_STATE]    = parts[NR_FLIGHT_STATE]
      self._data[I_ALTITUDE]        = float(parts[NR_ALTITUDE])
      self._data[I_ACCELERATION]    = float(parts[NR_ACCELERATION])
      self._data[I_LIGHT_RED]       = 0
      self._data[I_LIGHT_GREEN]     = 0
      self._data[I_LIGHT_BLUE]      = 0
      self._data[I_LIGHT_CLEAR]     = 0
      self._data[I_TEMPERATURE]     = 0.0
      self._data[I_PRESSURE]        = 0.0
      self._data[I_ACCEL_X]         = 0.0
      self._data[I_ACCEL_Y]         = 0.0
      self._data[I_ACCEL_Z]         = 0.0
