from threading     import Thread # Thread to record continuously
from threading     import Event  # Events for communicating within threads
import time
import os
import sys
import queue

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

# Size of message queue buffer
BUF_SIZE = 100


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

         DinoLog.__thread   = None
         DinoLog.__stop     = None
         DinoLog.__msgQueue = None


         # Generate filename for archive and create a new folder to store the data.
         timestamp = DinoTime.getTimestampStr()
         DinoLog.__folder = "Logs/" + archiveName + "_" + timestamp
         DinoLog.__filepath = DinoLog.__folder + "/" + archiveName + "_" + timestamp + ".txt"
         if(not os.path.exists(os.path.dirname(DinoLog.__filepath))):
            os.mkdir(os.path.dirname(DinoLog.__filepath))

         # Initialize message queue
         try:
            DinoLog.__msgQueue = queue.Queue(BUF_SIZE)
            DinoLog.__msgQueue.put(EVENT_ID + "0" + CSV_SEP + \
               "Log file \"" + DinoLog.__filepath + "\" initialized.")
         except:
            print("ERROR - Could not create msgQueue for Log.")
                  
         # Create event to notify log thread when to stop.
         # While this could have been done with a lock, the event 
         # has built in functions for checking if a flag is set.
         try:
            DinoLog.__stop = Event()
            DinoLog.__stop.set()
         except:
            print("ERROR - Could not create event for Log.")
            
         # Initialize counters for logging.
         DinoLog.__msgId = 0
         DinoLog.__dataId = 0    
         DinoLog.__startLog(DinoLog.__instance)     
      return DinoLog.__instance
   
   
   def __startLog(self):
      try:
         self.__stop.clear()
         self.__thread = Thread(target=self.__run, args=(self.__stop, self.__msgQueue, self.__filepath,))
         self.__thread.start()
      except Exception as e: 
         print(e)
         print("ERROR - Could not create thread for DinoLog.")
   
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
      DinoLog.__msgQueue.put(EVENT_ID + str(DinoLog.__msgId) + CSV_SEP + msg.replace(CSV_SEP, SAFE_SEP))   

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
      
      DinoLog.__msgQueue.put(DATA_ID + str(DinoLog.__dataId) + CSV_SEP + CSV_SEP.join(dataList))


   @staticmethod
   def stopLog():
      """ 
      Stop thread and close log file. 

      Return
      ------
      bool
         True if the log thread was stopped.
      """
      DinoLog.logMsg("Log file \"" + str(DinoLog.__filepath) + "\" closed.")
      DinoLog.__stop.set()
      try:
         DinoLog.__thread.join()
         DinoLog.__thread = None
      except:
         return False
      return True
      

   def __run(self, stopEvent, msgQueue, filepath):
      """ 
      Thread for Log. 

      Read all messages from the message queue and write them to the log. 
      If a stopEvent is set, then wait until it finishes clearing the queue
      before closing the file. 
      
      The implementation follows a Producer-Consumer design pattern.
      
      Parameter
      ---------
      stopEvent : threading.Event
         Flag to stop this thread from the main application.
         Set by calling the function stopLog()
      msgQueue : queue.Queue
         Log message queue. 
      filepath : str
         String containing the log file path
      """
      fp = None
      
      # Thread runs until it receives a stopEvent
      while((stopEvent.isSet() == False) or (not msgQueue.empty())):
      
         # Read all messages from the queue and write them to the file
         if(not msgQueue.empty()):
            msg = str(msgQueue.get())
            
            # Log entries include both the current time and the MET.
            timeStr = DinoTime.getTimestampStr()
            metStr  = format(DinoTime.getMET(), MET_STR_FORMAT)

            # Format for log messages
            logEntry = timeStr + CSV_SEP + metStr + CSV_SEP + msg + "\n"

            # Log the message. Keep the file open. 
            if(fp is None):
               fp = open(filepath, 'a')
            fp.write(logEntry)
            fp.flush()      
            time.sleep(0.02)
      
      # Close log
      fp.close()
      fp = None


   def __del__(self):
      """
      Destructor to ensure the log file is closed.
      """
      self.stopLog()



