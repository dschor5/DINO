import time


class DinoTime(object):
   """
   Class DinoTime - Tracks date/time and mission elapsed time (MET)

   This class offers two static methods used for timekeeping:
      1) Date/Time
         Accessible through DinoTime.getTimestampStr(). This format
         is used for archives and log files to ensure each file has
         a unique timetamp and does not override its predecessors. 

      2) Mission Elapsed Time (MET) in seconds
         This variable starts counting from 0 when the software
         initializes and can be used to measure the time elapsed 
         between events.  

   This class was designed using static methods such that these methods
   can be called from any part of the application. 
   """


   # DinoTime Singleton instance 
   __instance = None

   # Reference timestamp for calculating MET.
   __startTime = 0


   def __new__(cls):
      """
      Create a singleton instance of the DinoTime class.
      """
      if(DinoTime.__instance is None):
         DinoTime.__instance = object.__new__(cls)
         
         # Initialize MET. 
         DinoTime.__startTime = time.time()
      return DinoTime.__instance


   @staticmethod
   def getMET():
      """
      Static method to calculate and return MET.
      
      Returns
      -------
      float
         Mission elapsed time (MET) in seconds.
      """
      return time.time() - DinoTime.__startTime


   @staticmethod 
   def getTimestampStr():
      """
      Static method to return a string timestamp.
      The timestamp format is fixed width:
         YYYYMMDD-HHMMSS

      Returns
      -------
      str
         String containing timestamp.
      """
      return time.strftime("%Y%m%d-%H%M%S")


