from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from gpiozero   import LED        # GPIO interface
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - GPIO for heater/cooler not loaded.")


# Indeces into __state array to store whether the units are on/off.
STATE_HEATER = 0
STATE_COOLER = 1


class DinoThermalControl(object):

   # DinoThermalControl Singleton instance 
   __instance = None


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


   def __init__(self):
      """
      Initialize system with all devices turned off.
      """
      self.__state[STATE_HEATER] = self.setHeaterState(False)
      self.__state[STATE_COOLER] = self.setCoolerState(False)


   def __del__(self):
      """ 
      Destructor. Turn off all devices.
      """
      self.__state[STATE_HEATER] = self.setHeaterState(False)
      self.__state[STATE_COOLER] = self.setCoolerState(False)


   def getState(self):
      """
      Get the state of the heater and cooler.
      
      Returns
      -------
      list
         Heater state (on=True,off=False), Cooler state (on=True,off=False)
      """
      return self.__state


   
   def setHeaterState(self, turnOn):
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
      if((turnOn == True) and (self.__state[STATE_COOLER] == True)):
         DinoLog.logMsg("ERROR - Attempted to turn on heater when the cooler in already on.")
         turnOn = False

      try:
         if(turnOn == True):
            self.__heater.on()
         else:
            self.__heater.off()
         self.__state[STATE_HEATER] = self.__heater.is_lit
      except:
         DinoLog.logMsg("ERROR - Heater set(" + str(turnOn) + ") failed.")
         self.__state[STATE_HEATER] = False
      return self.__state[STATE_HEATER]
     


   def setCoolerState(self, turnOn):
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
      if((turnOn == True) and (self.__state[STATE_HEATER] == True)):
         DinoLog.logMsg("ERROR - Attempted to turn on cooler when the heater in already on.")
         turnOn = False

      try:
         if(turnOn == True):
            self.__cooler.on()
         else:
            self.__cooler.off()
         self.__state[STATE_COOLER] = self.__cooler.is_lit
      except:
         
         DinoLog.logMsg("ERROR - Cooler set(" + str(turnOn) + ") failed.")
         self.__state[STATE_COOLER] = False
      return self.__state[STATE_COOLER]
      

   
