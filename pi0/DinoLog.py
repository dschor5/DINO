import time
import os
import sys

from DinoTime import *

class DinoLog(object):

   __instance = None
   
   DATA_ID        = "D"
   EVENT_ID       = "E"
   CSV_SEP        = ","
   SAFE_SEP       = ";"
   MET_STR_FORMAT = "0>8.2f"

   """ Initialization. Enforces singleton design pattern. """
   def __new__(cls, folder):
      if(DinoLog.__instance is None):
         DinoLog.__instance = object.__new__(cls)
         timestamp = DinoTime.getTimestampStr()
         DinoLog.__filepath = folder + "_" + timestamp + "/" + folder + "_" + timestamp + ".txt"
         if(not os.path.exists(os.path.dirname(DinoLog.__filepath))):
            os.mkdir(os.path.dirname(DinoLog.__filepath))
         DinoLog.__fp = None
         DinoLog.__instance.__log(DinoLog.EVENT_ID + "0" + DinoLog.CSV_SEP + \
             "Log file \"" + DinoLog.__filepath + "\" initialized.")
         DinoLog.__msgId = 0
         DinoLog.__dataId = 0         
      return DinoLog.__instance
   
   """ Get log filename. """
   def getFilename(self):
      return self.__filepath

   @staticmethod
   def logMsg(msg):
      DinoLog.__msgId = DinoLog.__msgId + 1
      DinoLog.__log(DinoLog.__instance, \
         DinoLog.EVENT_ID + str(DinoLog.__msgId) + DinoLog.CSV_SEP + \
         msg.replace(DinoLog.CSV_SEP, DinoLog.SAFE_SEP))   

   def logData(self, data):
      self.__dataId = self.__dataId + 1
      self.__log(self.DATA_ID + str(self.__dataId) + self.CSV_SEP + str(data))


   """ Log a message. """
   def __log(self, msg):
      # Log entries include both the current time and the MET.
      timeStr = DinoTime.getTimestampStr()
      metStr  = format(DinoTime.getMET(), self.MET_STR_FORMAT)

      # Format for log messages
      logEntry = timeStr + self.CSV_SEP + metStr + self.CSV_SEP + msg + "\n"

      # Log the message. Keep the file open. 
      if(self.__fp is None):
         self.__fp = open(self.__filepath, 'a')
      self.__fp.write(logEntry)
      self.__fp.flush()      


   def closeLog(self):
      self.__fp.close()
      self.__fp = None



