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


# Index of telemetry read from Envirophat
ENV_HAT_LIGHT_RED    = 0   # Envirophat light sensor red channel
ENV_HAT_LIGHT_GREEN  = 1   # Envirophat light sensor green channel
ENV_HAT_LIGHT_BLUE   = 2   # Envirophat light sensor blue channel
ENV_HAT_LIGHT_CLEAR  = 3   # Envirophat light sensor clear channel
ENV_HAT_TEMPERATURE  = 4   # Envirophat temperature sensor
ENV_HAT_PRESSURE     = 5   # Envirophat pressure sensor
ENV_HAT_ACCEL_X      = 6   # Envirophat acceleration along x-axis
ENV_HAT_ACCEL_Y      = 7   # Envirophat acceleration along y-axis
ENV_HAT_ACCEL_Z      = 8   # Envirophat acceleration along z-axis
ENV_HAT_SIZE         = 9



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
         DinoEnvirophat.__data = [None] * ENV_HAT_SIZE

         # Turns LEDs on the board off so that they do not 
         # interfere with the experiment.
         try:
            leds.off()
         except:
            DinoLog.logMsg("ERROR - Envirophat fail to turn off on-board led.")
      return DinoEnvirophat.__instance

   
   def readData(self):
      """
      Read all sensors in the envirophat and return them in a touple.

      Returns
      -------
      list
         List of raw telemetry readings from Envirophat organized
         using the indeces of the ENV_HAT_* global variable. 
      """
      temp = self.__getLightSensorReadings()
      self.__data[ENV_HAT_LIGHT_RED]   = temp[0]
      self.__data[ENV_HAT_LIGHT_GREEN] = temp[1]
      self.__data[ENV_HAT_LIGHT_BLUE]  = temp[2]
      self.__data[ENV_HAT_LIGHT_CLEAR] = temp[3]

      temp = self.__getTemperature()
      self.__data[ENV_HAT_TEMPERATURE] = temp[0]

      temp = self.__getPressure()
      self.__data[ENV_HAT_PRESSURE] = temp[0]

      temp = self.__getAcceleration()
      self.__data[ENV_HAT_ACCEL_X] = temp[0]
      self.__data[ENV_HAT_ACCEL_Y] = temp[1]
      self.__data[ENV_HAT_ACCEL_Z] = temp[2]

      return self.__data
   
   def __getLightSensorReadings(self):
      """ 
      Read raw light sensor readings from red, green, blue, and clear
      channels and return them in a touple.
      
      Returns
      -------
      touple
         Light reading for (red, green, blue, and clear) channels.       
      """
      try:
         temp = light.raw()
      except:
         DinoLog.logMsg("ERROR - Envirophat fail to read light sensor.")
         temp = (None, None, None, None)
      return temp
            

   def __getTemperature(self):
      """ 
      Read temperature in degree celsius. 
      
      Returns
      -------
      touple
         Temperature in degree Celsius.
      """
      try:
         value = (weather.temperature(),)
      except:
         DinoLog.logMsg("ERROR - Envirophat fail to read temperature.")
         value = (None,)
      return value   

   def __getPressure(self):
      """ 
      Read pressure in Pa.
      
      Returns
      -------
      touple
         Pressure reading in Pa.
      """
      try:
         value = (weather.pressure(unit='Pa'),)
      except:
         DinoLog.logMsg("ERROR - Envirophat fail to read pressure.")
         value = (None,)
      return value


   def __getAcceleration(self):
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
         DinoLog.logMsg("ERROR - Envirophat fail to read acceleration.")
         value = (None, None, None)
      return value


