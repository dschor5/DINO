from threading     import Thread
from threading     import RLock  # Note re-entrant lock
from threading     import Event 
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


   def __new__(cls, filename="dinoVideo"):
      """
      Create a singleton instance of the DinoCamera class. 
      Log an error if the PiCamera() object cannot be created due to missing libraries. 

      Parameters
      ----------
      filename : str
         Filename prefix for all videos. 
         The timestamp and extension are appended to the name provided.
      """
      if(DinoCamera.__instance is None):
         DinoCamera.__instance  = object.__new__(cls)
         DinoCamera.__filename  = filename
         DinoCamera.__isRecording = False
         DinoCamera.__count     = 0
         DinoCamera.__single    = True
         DinoCamera.__thread    = None
         DinoCamera.__lockCount = None
         DinoCamera.__lockRec   = None
         DinoCamera.__stop      = None

         # Create lock object to protect shared resources
         # between the PiCamera() object and the 
         try:
            DinoCamera.__lockCount = RLock()         
            DinoCamera.__lockRec   = RLock()
         except:
            DinoLog.logMsg("ERROR - Could not create lock for PiCamera().")

         # Create event to notify recording thread when to stop
         try:
            DinoCamera.__stop = Event()
            DinoCamera.__stop.set()
         except:
            DinoLog.logMsg("ERROR - Could not create event for PiCamera().")

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
      self.__lockRec.acquire()
      isRecording = self.__isRecording
      self.__lockRec.release()
      return isRecording


   def getNumRecordings(self):
      """
      Return the number of recordings made since the start of the program.
      """
      self.__lockCount.acquire()
      num = self.__count
      self.__lockCount.release()
      return num


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
      self.__stop.set()
      self.__single    = single
   
      # Start thread.
      try:
         self.__stop.clear()
         self.__thread = Thread(target=self.__run, args=(self.__stop, self.__lockCount, self.__lockRec,)).start()
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
         Returns True if it is still recording (error) or False otherwise.
      """
      self.__stop.set()
      try:
         self.__thread.join()
         self.__thread = None
      except:
         return False
      return self.isRecording()


   def __run(self, stopEvent, lockCount, lockRec):
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
      lockRec.acquire()
      self.__isRecording = True
      lockRec.release()

      # Run main loop for the required number of recordings
      firstTime = True
      faultFound = False
      while(((firstTime == True) or (self.__single == False)) and (stopEvent.isSet() == False) and (faultFound == False)):
         firstTime = False

         # Generate filename for new recording
         timestamp = DinoTime.getTimestampStr()
         filepath = self.__filename + "_" + timestamp + ".h264"         

         # Updated shared variables
         lockCount.acquire()
         self.__count = self.__count + 1
         lockCount.release()
         
         # Start new recording
         try:
            self.__camera.start_recording(filepath)
            DinoLog.logMsg("Start PiCamera file=[" + filepath + "]")
         except:
            DinoLog.logMsg("ERROR - Failed to start PiCamera file=[" + filepath + "]")
            faultFound = True

         # Wait until it reaches the end of the recording or
         # the application sends a request to stop the capture.
         recStartTime = DinoTime.getMET() 
         time.sleep(0.1)
         recTime = DinoTime.getMET() - recStartTime
         while((recTime <= self.__duration) and (stopEvent.isSet() == False and (faultFound == False))):
            time.sleep(0.1)
            recTime = DinoTime.getMET() - recStartTime

         # Stop the recording.
         try:
            self.__camera.stop_recording()
            DinoLog.logMsg("Stop PiCamera file=[" + filepath + "] duration=[" + str(recTime) + "sec]")
         except:
            DinoLog.logMsg("ERROR - Failed to stop PiCamera PiCamera file=[" + filepath + "] ")
            faultFound = True

      # Reset thread variables
      lockRec.acquire()
      self.__isRecording = False
      lockRec.release()
      stopEvent.set()

