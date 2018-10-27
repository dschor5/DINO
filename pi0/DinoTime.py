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

   # Minimum time difference to cause the time sync.
   SYNC_TIME_MIN_THRESHOLD = 1


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
   def setTime(newMet):
      """
      Static method that sets the time. Used to sync the 
      time to the main vehicle in the event of a reboot
      of the raspberry pi that cause the MET to be reset to 0.
      
      Only change the time if the difference between the 
      two clocks is greater than a certain threshold.
      
      Assume that the system can only jump the time forward.
      If a backwards time jump is requested, return False.
            
      Parameter
      ---------
      serialMET : float
         Time received through serial data.
         
      Return
      ------
      bool
         True if it changed the time, False otherwise.
      """
      currMet = DinoTime.getMET()
      status = False
      
      # Validate jump in forward direction and greater
      # than some minimum threshold.
      if((newMet - currMet) > DinoTime.SYNC_TIME_MIN_THRESHOLD):
         DinoTime.__startTime = time.time() - newMet
         status = True
      return status
      

   @staticmethod
   def getMET():
      """
      Static method to calculate and return MET.
      
      Returns
      -------
      float
         Mission elapsed time (MET) in seconds.
      """
      return float(time.time() - DinoTime.__startTime)


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


