import time
import os
import sys

from DinoTime import *

#TODO - Update to support re-entrancy. 

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


class DinoLog(object):
   """
   Class DinoLog - Logs data + errors at runtime.

   Provides interface for logging messages at runtime. 
   The class abstracts some functionality to add timestamps 
   and unique identifiers to facilitate parsing the log.
   """

   # DinoLog Singleton instance 
   __instance = None
   

   def __new__(cls, archiveName):
      """
      Create a singleton instance and initialize the DinoLog. 

      Create a new folder of the archive with the name and a date/time timestamp.
      Log an initial entry indicating the file was created. 

      If debug is enabled, subsequent calls to logMsg() with debug=True will
      be recorded in the log. Otherwise, those messages will not be saved.

      Parameters
      ----------
      archiveName : str
         Name for log archive.
      debugEnable : bool
         Enable logging of debug messages.  
      """
      if(DinoLog.__instance is None):
         DinoLog.__instance = object.__new__(cls)

         # Generate filename for archive and create a new folder to store the data.
         timestamp = DinoTime.getTimestampStr()
         DinoLog.__folder = "Logs/" + archiveName + "_" + timestamp
         DinoLog.__filepath = DinoLog.__folder + "/" + archiveName + "_" + timestamp + ".txt"
         if(not os.path.exists(os.path.dirname(DinoLog.__filepath))):
            os.mkdir(os.path.dirname(DinoLog.__filepath))

         # Log initial entry to the file.
         DinoLog.__fp = None
         DinoLog.__instance.__log(EVENT_ID + "0" + CSV_SEP + \
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
         EVENT_ID + str(DinoLog.__msgId) + CSV_SEP + \
         msg.replace(CSV_SEP, SAFE_SEP))   

   @staticmethod
   def logData(data):
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
      DinoLog.__dataId = DinoLog.__dataId + 1
      
      # Format data for the log
      dataList = []
      for i in data:
         if(isinstance(i, float) == True):
            dataList.append('{0:.4f}'.format(i))
         else:
            dataList.append(str(i))
      
      DinoLog.__log(DinoLog.__instance, \
         DATA_ID + str(DinoLog.__dataId) + CSV_SEP + CSV_SEP.join(dataList))


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
      metStr  = format(DinoTime.getMET(), MET_STR_FORMAT)

      # Format for log messages
      logEntry = timeStr + CSV_SEP + metStr + CSV_SEP + msg + "\n"

      # Log the message. Keep the file open. 
      if(self.__fp is None):
         self.__fp = open(self.__filepath, 'a')
      self.__fp.write(logEntry)
      self.__fp.flush()      
      #print(logEntry)


   def __del__(self):
      """
      Destructor to ensure the log file is closed.
      """
      self.logMsg("Log file \"" + DinoLog.__filepath + "\" closed.")
      self.closeLog()


   def closeLog(self):
      """
      Close the log file if it is still opened.
      """
      if(self.__fp is not None):
         self.__fp.close()
         self.__fp = None



