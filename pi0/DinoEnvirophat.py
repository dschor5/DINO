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


   ENV_KEYS = {
      "LIGHT_RED"      : 0,
      "LIGHT_GREEN"    : 1,
      "LIGHT_BLUE"     : 2,
      "LIGHT_CLEAR"    : 3,
      "TEMPERATURE"    : 4,
      "PRESSURE"       : 5,
      "ACCELERATION_X" : 6,
      "ACCELERATION_Y" : 7,
      "ACCELERATION_Z" : 8,
      "MAG_X"          : 9,
      "MAG_Y"          : 10,
      "MAG_Z           : 11
   }


   def __new__(cls):
      """
      Create a singleton instance of the DinoEnvirophat class. 
      """
      if(DinoEnvirophat.__instance is None):
         DinoEnvirophat.__instance = object.__new__(cls)
         DinoEnvirophat.__data = dict.fromkeys(ENV_KEYS)

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

         Index | Abbreviation | Description
         ------------------------------------------------------
          0    | LR           | Light red channel
          1    | LG           | Light green channel
          2    | LB           | Light blue channel
          3    | LC           | Light clear channel
          4    | T            | Temperature (C)
          5    | P            | Pressure (Pa)
          6    | AX           | Acceleration along x-axis
          7    | AY           | Acceleration along y-axis
          8    | AZ           | Acceleration along z-axis
          9    | MX           | Magnetometer reading along x-axis
         10    | MX           | Magnetometer reading along x-axis
         11    | MX           | Magnetometer reading along x-axis

      Returns
      -------
      touple
         (LR, LG, LB, LC, T, P, AX, AY, AZ, MX, MY, MZ) 
      """
      data = ()
      data = data + self.getLightSensorReadings()
      data = data + self.getTemperature()
      data = data + self.getPressure()
      data = data + self.getAcceleration()
      data = data + self.getMagReading()
      return data
   
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
         temp = light.raw()
      except:
         DinoLog.logMsg("ERROR - Envirophat fail to read light sensor.")
         temp = (None, None, None, None)
      self.__data["LIGHT_RED"]   = temp[0]
      self.__data["LIGHT_GREEN"] = temp[1]
      self.__data["LIGHT_BLUE"]  = temp[2]
      self.__data["LIGHT_CLEAR"] = temp[3]
      return self.__data
            

   def getTemperature(self):
      """ 
      Read temperature in degree celsius. 
      
      Returns
      -------
      float
         Temperature in degree Celsius.
      """
      try:
         value = (weather.temperature(),)
      except:
         DinoLog.logMsg("ERROR - Envirophat fail to read temperature.")
         value = (None,)
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
         value = (weather.pressure(unit='Pa'),)
      except:
         DinoLog.logMsg("ERROR - Envirophat fail to read pressure.")
         value = (None,)
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
         DinoLog.logMsg("ERROR - Envirophat fail to read acceleration.")
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
         DinoLog.logMsg("ERROR - Envirophat fail to read magnetometer.")
         value = (None, None, None)
      return value


