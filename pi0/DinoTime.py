import time


class DinoTime(object):

   """ Instance variable for Singleton design pattern. """
   __instance = None

   """ Store start time to calculate MET. """
   __startTime = 0


   """ Initialization. Enforces singleton design pattern. """
   def __new__(cls):
      if(DinoTime.__instance is None):
         DinoTime.__instance = object.__new__(cls)
         DinoTime.__startTime = time.time()
      return DinoTime.__instance


   """ Get the mission elapsed time (MET). """
   @staticmethod
   def getMET():
      return time.time() - DinoTime.__startTime


   """ Get the current time for log files only. """
   @staticmethod 
   def getTimestampStr():
      return time.strftime("%Y%m%d-%H%M%S")


