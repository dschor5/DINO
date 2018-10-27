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
      self._data[I_VELOCITY_X]      = float(parts[NR_VELOCITY_X])
      self._data[I_VELOCITY_Y]      = float(parts[NR_VELOCITY_Y])
      self._data[I_VELOCITY_Z]      = float(parts[NR_VELOCITY_Z])
      self._data[I_ACCELERATION]    = float(parts[NR_ACCELERATION])
      self._data[I_ATTITUDE_X]      = float(parts[NR_ATTITUDE_X])
      self._data[I_ATTITUDE_Y]      = float(parts[NR_ATTITUDE_Y])
      self._data[I_ATTITUDE_Z]      = float(parts[NR_ATTITUDE_Z])
      self._data[I_ANG_VEL_X]       = float(parts[NR_ANG_VEL_X])
      self._data[I_ANG_VEL_Y]       = float(parts[NR_ANG_VEL_Y])
      self._data[I_ANG_VEL_Z]       = float(parts[NR_ANG_VEL_Z])
      self._data[I_WARNING_LIFTOFF] = int(parts[NR_WARNING_LIFTOFF])
      self._data[I_WARNING_RCS]     = int(parts[NR_WARNING_RCS])
      self._data[I_WARNING_ESCAPE]  = int(parts[NR_WARNING_ESCAPE])
      self._data[I_WARNING_CHUTE]   = int(parts[NR_WARNING_CHUTE])
      self._data[I_WARNING_LANDING] = int(parts[NR_WARNING_LANDING])
      self._data[I_WARNING_FAULT]   = int(parts[NR_WARNING_FAULT])
      self._data[I_LIGHT_RED]       = 0
      self._data[I_LIGHT_GREEN]     = 0
      self._data[I_LIGHT_BLUE]      = 0
      self._data[I_LIGHT_CLEAR]     = 0
      self._data[I_TEMPERATURE]     = 0.0
      self._data[I_PRESSURE]        = 0.0
      self._data[I_ACCEL_X]         = 0.0
      self._data[I_ACCEL_Y]         = 0.0
      self._data[I_ACCEL_Z]         = 0.0
      self._data[I_MAG_X]           = 0.0
      self._data[I_MAG_Y]           = 0.0
      self._data[I_MAG_Z]           = 0.0
