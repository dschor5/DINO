from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from envirophat import light    # light sensor
   from envirophat import leds     # control leds on the board
   from envirophat import weather  # temperature and pressure sensors
   from envirophat import motion   # accelerometer sensor
   leds.off()
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - Envirophat not loaded.")


class DinoEnvirophat(object):

   __instance = None

   """ Singleton instance. """
   def __new__(cls):
      if(DinoEnvirophat.__instance is None):
         DinoEnvirophat.__instance = object.__new__(cls)
      return DinoEnvirophat.__instance

   """ Returns tuple with four values for R, G, B, and CLEAR values. """
   def getLightSensorReadings(self):
      data = (None, None, None, None)
      try:
         data = light.raw()
      except:
         DinoLog.logMsg("ERROR - Envirophat fail to read light sensor.")
      return data
            
   """ Read temperature in degree C. """
   def getTemperature(self):
      try:
         value = weather.temperature()
      except:
         DinoLog.logMsg("ERROR - Envirophat read temperature.")
         value = None
      return value
   
   """ Return pressure in Pa."""
   def getPressure(self):
      try:
         value = weather.pressure(unit='Pa')
      except:
         DinoLog.logMsg("ERROR - Envirophat read pressure.")
         value = None
      return value

   """ Returns tuple for acceleration x, y, and z. """
   def getAcceleration(self):
      try:
         value = motion.accelerometer()
      except:
         DinoLog.logMsg("ERROR - Envirophat read acceleration.")
         value = (None, None, None)
      return value
   
   """ Returns tuple for mag_x, mag_y, and mag_z readings."""
   def getMagReading(self):
      try:
         value = motion.magnetometer()
      except:
         DinoLog.logMsg("ERROR - Envirophat read magnetometer.")
         value = (None, None, None)
      return value


