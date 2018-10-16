from threading     import Thread
from threading     import RLock  # Note re-entrant lock
from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from picamera import PiCamera # NoIR camera
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - PiCamera not loaded.")


class DinoCamera(object):
   """ 
   Class DinoCamera - Interface with PiNoir Camera.

   The camera can be used to capture a single recording (for testing) or
   a stream of continuous short recordings for flight. 

   The stream of short recordings was designed to ensure files are saved
   periodically such that the data is not lost in case of an anomaly. 
   Each filename appends a timestamp such that the sequence of videos 
   can be reconstructed for post-processing. 
   """

   # DinoCamera Singleton instance 
   __instance = None

   # Constants
   MIN_DURATION = 5.0
   MAX_DURATION = 60.0


   def __new__(cls, folder=".", filename="dinoVideo"):
      """
      Create a singleton instance of the DinoCamera class. 
      Log an error if the PiCamera() object cannot be created due to missing libraries. 

      Parameters
      ----------
      folder : str
         Folder name where files are saved. 
      filename : str
         Filename prefix for all videos. 
         The timestamp and extension are appended to the name provided.
      """
      if(DinoCamera.__instance is None):
         DinoCamera.__instance  = object.__new__(cls)
         DinoCamera.__folder    = folder
         DinoCamera.__filename  = filename
         DinoCamera.__filepath  = ""
         DinoCamera.__count     = 0
         DinoCamera.__single    = True
         DinoCamera.__stop      = True
         DinoCamera.__thread    = None

         # Create lock object to protect shared resources
         # between the PiCamera() object and the 
         try:
            DinoCamera.__lock = RLock()         
         except:
            DinoCamera.__lock = None
            DinoLog.logMsg("ERROR - Could not create lock for PiCamera().")

         # Create PiCamera object.
         try:
            DinoCamera.__camera = PiCamera()
            DinoCamera.__camera.resolution = (800, 600)
            DinoCamera.__camera.framerate  = 15
         except:
            DinoCamera.__camera = None
            DinoLog.logMsg("ERROR - Could not create PiCamera() object.")
      return DinoCamera.__instance


   def isRecording(self):
      """
      Return True if thread is active and PiCamera is recording.
      """
      self.__lock.acquire()
      recording = (self.__stop == False)
      self.__lock.release()
      return recording


   def getNumRecordings(self):
      """
      Return the number of recordings made since the start of the program.
      """
      self.__lock.acquire()
      num = self.__count
      self.__lock.release()
      return num


   def getFilename(self):
      """ 
      Return the name of the current or most recent recording.
      """
      self.__lock.acquire()
      filename = self.__filepath
      self.__lock.release()
      return filename
         


   def startRecording(self, single=True, duration=60):
      """
      Start a PiCamera recording. 

      Parameters
      ----------
      single : bool
         If True, start a single recording. 
         If False, start a stream of continuous recordings
      duration : int
         Duration for each individual recording in seconds.
      
      Returns
      -------
      bool
         True if it successfully started the recording.
         False if it was already recording or failed to start a new recording.
      """
      # Ensure there is no recording in progress.
      if(self.isRecording() == True):
         DinoLog.logMsg("ERROR - PiCamera recording already in progress.")
         return False
      
      # Validate input parameters
      if((duration < self.MIN_DURATION) or (duration > self.MAX_DURATION)):
         DinoLog.logMsg("ERROR - Invalid PiCamera recording duration=[" + str(duration) + "].")
         return False

      # Record settings and start thread
      self.__duration  = int(duration)

      # Settings protected by re-entrant lock
      self.__lock.acquire()
      self.__single    = single
      self.__stop      = False
      self.__recording = True
      self.__lock.release()
   
      # Start thread.
      try:
         self.__thread = Thread(target=self.__run).start()
         status = True
      except:
         DinoLog.logMsg("ERROR - Could not start PiCamera thread.")
         status = False

      return status


   def stopRecording(self):
      """ 
      Stop camera recording and terminate thread. 

      Terminates the ongoing recording even if it has not finished
      the desired video duration. This will also stop terminate 
      continuous recording in order to end the thread.

      Return
      ------
      bool
         Returns True
      """
      self.__lock.acquire()
      self.__stop = True
      self.__recording = False
      self.__lock.release()
      if((self.__thread is not None) and (self.__thread.is_alive())):
         self.__thread.join()
         self.__thread = None
      return True


   def __run(self):
      """ 
      Thread for PiCamera. 

      The thread runs once for a single recording (for testing) or
      continuosly for a stream of recordings. If run continuosuly, 
      the application must call stopRecording() to terminate the thread.

      For each recording, the thread will:
      1. Assign a unique filename with a timestamp
      2. Start a recording
      3. Capture the MET at the start of the recording
      4. Wait in a loop until the recording completed
      """
      # Run main loop for the required number of recordings
      firstTime = True
      stop = False
      while(((firstTime == True) or (self.__single == False)) and (stop == False)):
         firstTime = False

         # Generate filename for new recording
         timestamp = DinoTime.getTimestampStr()
         self.__lock.acquire()
         self.__filepath = self.__folder + "/" + self.__filename + "_" + timestamp + ".h264"
         filepath = self.__filepath
         self.__count = self.__count + 1
         self.__lock.release()

         # Start new recording
         try:
            print(self.__camera.start_recording(filepath))
            DinoLog.logMsg("Start PiCamera file=[" + filepath + "]")
         except:
            DinoLog.logMsg("ERROR - Failed to start PiCamera file=[" + filepath + "]")

         # Wait until it reaches the end of the recording or
         # the application sends a request to stop the capture.
         recStartTime = DinoTime.getMET() 
         recTime = DinoTime.getMET() - recStartTime  
         while((recTime <= self.__duration) and (stop == False)):
            time.sleep(1)
            self.__lock.acquire()
            stop = self.__stop
            self.__lock.release()   
            recTime = DinoTime.getMET() - recStartTime

         # Stop the recording.
         try:
            self.__camera.stop_recording()
            DinoLog.logMsg("Stop PiCamera file=[" + filepath + "] duration=[" + str(recTime) + "sec]")
         except:
            DinoLog.logMsg("ERROR - Failed to stop PiCamera PiCamera file=[" + filepath + "] ")

      # Reset thread variables
      self.__lock.acquire()
      self.__stop = True
      self.__single = True
      self.__lock.release()


