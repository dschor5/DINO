from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from gpiozero   import LED        # GPIO interface
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - GPIO for heater/cooler not loaded.")


class DinoThermalControl(object):

   # DinoThermalControl Singleton instance 
   __instance = None

   STATE_HEATER = 0
   STATE_COOLER = 1

   """ Singleton instance. """
   def __new__(cls, heaterPin, coolerPin):
      if(DinoThermalControl.__instance is None):
         DinoThermalControl.__instance = object.__new__(cls)
         DinoThermalControl.__state = [False, False]

         # Initialize heater control through GPIO pin. 
         try:
            DinoThermalControl.__heater = LED(heaterPin)
         except:
            DinoLog.logMsg("ERROR - Could not initialize GPIO for heater.")
            DinoThermalControl.__heater = None

         # Initialize cooler control through GPIO pin.
         try:
            DinoThermalControl.__cooler = LED(coolerPin)
         except:
            DinoLog.logMsg("ERROR - Could not initialize GPIO for cooler.")
            DinoThermalControl.__cooler = None
      return DinoThermalControl.__instance

   
   def run(self, temperature=25):
      """
      Run thermal control algorithm to control the heater/cooler.

      Parameter
      ---------
      temperature : float
         Current temperature in degree C.
         Default set such that heater and cooler are off.
      """
      if(temperature < TURN_ON_HEATER):
         self.__setHeaterState(True)
         self.__setCoolerState(False)
         
      elif(temperature > TURN_OFF_HEATER):
         self.__setHeaterState(False)
      
      if(temperature < TURN_ON_COOLER):
         self.__setCoolerState(True)
         self.__setHeaterState(False)
         
      elif(temperature > TURN_OFF_COOLER):
         self.__setCoolerState(False)
      
      try:
         self.__state[self.STATE_HEATER] = self.__heater.is_lit()
         self.__state[self.STATE_COOLER] = self.__cooler.is_list()
      except:
         self.__state[self.STATE_HEATER] = False
         self.__state[self.STATE_COOLER] = False

      return self.__state

   
   def __setHeaterState(self, turnOn):
      """
      Set heater state to ON or OFF.

      Parameter
      ---------
      turnOn : bool
         True to turn the heater on.

      Return
      ------
      bool
         True on success. False if error accessing GPIO.
      """
      try:
         self.__heater.on()
         status = self.__heater.is_list()
      except:
         DinoLog.logMsg("ERROR - Heater set(" + str(turnOn) + ") failed.")
         status = False
      return status
     

   def __setCoolerState(self, turnOn):
      """
      Set cooler state to ON or OFF.

      Parameter
      ---------
      turnOn : bool
         True to turn the cooler on.

      Return
      ------
      bool
         True on success. False if error accessing GPIO.
      """
      try:
         self.__cooler.on()
         status = self.__cooler.is_list()
      except:
         
         DinoLog.logMsg("ERROR - Cooler set(" + str(turnOn) + ") failed.")
         status = False
      return status
      

   
