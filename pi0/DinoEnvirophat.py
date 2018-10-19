from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from envirophat import light    # light sensor
   from envirophat import leds     # control leds on the board
   from envirophat import weather  # temperature and pressure sensors
   from envirophat import motion   # accelerometer sensor
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - Envirophat not loaded.")


class DinoEnvirophat(object):
   """ 
   Class DinoEnvirophat - Interface with EnviropHat.

   The envirophat communicates with the pi0 using I2C to read 
   a the following sensors:
      1) Light Sensor       (TCS3472)
      2) Temperature Sensor (BMP280)
      3) Pressure Sensor    (BMP280)
      4) Accelerometer      (LSM303D)
      5) Magnetometer       (LSM303D)

   The API for the Envirophat had many additional functions that perform 
   some post-processing of the data received. However, some of those work 
   on cached data from the last reading instead of updating the reading 
   and then performing the computation. Please review the details of the 
   API if updating any of the functions called. 
   """

   # DinoEnvirophat Singleton instance 
   __instance = None


   def __new__(cls):
      """
      Create a singleton instance of the DinoEnvirophat class. 
      """
      if(DinoEnvirophat.__instance is None):
         DinoEnvirophat.__instance = object.__new__(cls)

         # Turns LEDs on the board off so that they do not 
         # interfere with the experiment.
         leds.off()
      return DinoEnvirophat.__instance

   
   def getLightSensorReadings(self):
      """ 
      Read raw light sensor readings from red, green, blue, and clear
      channels and return them in a touple.
      
      Returns
      -------
      touple
         Light reading for (red, green, blue, and clear) channels.       
      """
      try:
         data = light.raw()
      except:
         DinoLog.logMsg("ERROR - Envirophat fail to read light sensor.")
         data = (None, None, None, None)
      return data
            

   def getTemperature(self):
      """ 
      Read temperature in degree celsius. 
      
      Returns
      -------
      float
         Temperature in degree Celsius.
      """
      try:
         value = weather.temperature()
      except:
         DinoLog.logMsg("ERROR - Envirophat read temperature.")
         value = None
      return value
   

   def getPressure(self):
      """ 
      Read pressure in Pa.
      
      Returns
      -------
      touple
         Pressure reading in Pa.
      """
      try:
         value = weather.pressure(unit='Pa')
      except:
         DinoLog.logMsg("ERROR - Envirophat read pressure.")
         value = None
      return value


   def getAcceleration(self):
      """ 
      Read acceleration in UNITS??? for (x,y,z) axis.
      
      Returns
      -------
      touple
         Acceleration touple (x,y,z) in UNITS???
      """
      try:
         value = motion.accelerometer()
      except:
         DinoLog.logMsg("ERROR - Envirophat read acceleration.")
         value = (None, None, None)
      return value
   

   def getMagReading(self):
      """ 
      Read magnetic field in UNITS??? for (x,y,z) axis.
      
      Returns
      -------
      touple
         Magnetic field touple (x,y,z) in UNITS???
      """
      try:
         value = motion.magnetometer()
      except:
         DinoLog.logMsg("ERROR - Envirophat read magnetometer.")
         value = (None, None, None)
      return value


