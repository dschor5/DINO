import time
import os
import sys

from DinoTime import *

class DinoLog(object):
   """
   Class DinoLog - Logs data + errors at runtime.

   Provides interface for logging messages at runtime. 
   The class abstracts some functionality to add timestamps 
   and unique identifiers to facilitate parsing the log.
   """

   # DinoLog Singleton instance 
   __instance = None
   
   # Unique identifiers to differenciate data and messages
   # recorded to the log. 
   DATA_ID        = "D"
   EVENT_ID       = "E"

   # Character used to separate entries. 
   # Defaults to comma separated values (CSV) as ",".
   CSV_SEP        = ","
   # Character used to replace commas within messages. 
   SAFE_SEP       = ";"

   # Format for data/event counters in the log.
   MET_STR_FORMAT = "0>8.2f"


   def __new__(cls, archiveName):
      """
      Create and initialize DinoLog. 

      Create a new folder of the archive with the name and a date/time timestamp.
      Log an initial entry indicating the file was created. 

      Parameters
      ----------
      archiveName : str
         Name for log archive.  
      """
      if(DinoLog.__instance is None):
         DinoLog.__instance = object.__new__(cls)

         # Generate filename for archive and create a new folder to store the data.
         timestamp = DinoTime.getTimestampStr()
         DinoLog.__folder = archiveName + "_" + timestamp
         DinoLog.__filepath = self.__folder + "/" + archiveName + "_" + timestamp + ".txt"
         if(not os.path.exists(os.path.dirname(DinoLog.__filepath))):
            os.mkdir(os.path.dirname(DinoLog.__filepath))

         # Log initial entry to the file.
         DinoLog.__fp = None
         DinoLog.__instance.__log(DinoLog.EVENT_ID + "0" + DinoLog.CSV_SEP + \
             "Log file \"" + DinoLog.__filepath + "\" initialized.")

         # Initialize counters for logging.
         DinoLog.__msgId = 0
         DinoLog.__dataId = 0         
      return DinoLog.__instance
   
   
   @staticmethod
   def getFolder():
      """
      Returns teh folder for the current archive.
      
      Returns
      -------
      str
         Folder name for current archive
      """
      return DinoLog.__folder


   def getFilename(self):
      """
      Returns the filename for the current log.

      Returns
      -------
      str
         Filename of current log
      """
      return self.__filepath


   @staticmethod
   def logMsg(msg):
      """
      Log status/warning/error messages from application. 
      
      This is a static method such that it can be called from any of 
      the classes without needing to first get an instance of the class.

      The same log file is used to capture both messages and data. 
      Each of the two types has a unique counter to track how many 
      were written to a file. A letter (DATA_ID or EVENT_ID) 
      concatenated with the counter are added to each data entry. 
      This is only used to filter the files and ensure that they can 
      be easily arranged in chronological order.

      To facilitate parsing data, commands within the message are 
      converted to semicolons such that the CSV format is preserved.

      Parameter
      ---------
      data : str
         String to print to the file.       
      """
      DinoLog.__msgId = DinoLog.__msgId + 1
      DinoLog.__log(DinoLog.__instance, \
         DinoLog.EVENT_ID + str(DinoLog.__msgId) + DinoLog.CSV_SEP + \
         msg.replace(DinoLog.CSV_SEP, DinoLog.SAFE_SEP))   


   def logData(self, data):
      """
      Log data captured during the test. 
      
      The same log file is used to capture both messages and data. 
      Each of the two types has a unique counter to track how many 
      were written to a file. A letter (DATA_ID or EVENT_ID) 
      concatenated with the counter are added to each data entry. 
      This is only used to filter the files and ensure that they can 
      be easily arranged in chronological order.

      Parameter
      ---------
      data : list
         List to conver to a comma separated format for logging.
      """
      self.__dataId = self.__dataId + 1
      self.__log(self.DATA_ID + str(self.__dataId) + self.CSV_SEP + str(data))


   def __log(self, msg):
      """
      Log a message to the log. 

      The function will append a date/time and MET timestamps
      separated by CSV_SEP for easy parsing. 

      Open the file if needed. Then log the message and flush
      the data to the file in case the program is terminated abruptly. 
      The function keeps the file opened for subsequent writes.

      Parameter
      ---------
      msg : str
         Message to log to the file.
      """
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


   def __del__(self):
      """
      Destructor to ensure the log file is closed.
      """
      self.closeLog()


   def closeLog(self):
      """
      Close the log file if it is still opened.
      """
      if(self.__fp is not None):
         self.__fp.close()
         self.__fp = None



