from threading     import Thread # Thread to record continuously
from threading     import RLock  # Note re-entrant lock
from threading     import Event  # Events for communicating within threads

from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from gpiozero   import PWMOutputDevice
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - Servo PWM library not loaded.")


class DinoServo(object):

   # DinoServo Singleton instance 
   __instance = None

   # Constants
   MIN_PERIOD = 1.0
   MAX_PERIOD = 10.0

   """ Singleton instance. """
   def __new__(cls, servoPin):
      if(DinoServo.__instance is None):
         DinoServo.__instance = object.__new__(cls)
         DinoServo.__isAgitating = False
         DinoServo.__single      = True
         DinoServo.__thread      = None
         DinoServo.__lock        = None
         DinoServo.__stop        = None

         # Create lock object to protect shared resources.
         try:
            DinoServo.__lock = RLock()
         except:
            DinoLog.logMsg("ERROR - Could not create lock for servo thread.")

         # Create event to notify servo thread when to stop.
         # While this could have been done with a lock, the event 
         # has built in functions for checking if a flag is set.
         try:
            DinoServo.__stop = Event()
            DinoServo.__stop.set()
         except:
            DinoLog.logMsg("ERROR - Could not create event for PiCamera().")

         # Create PiCamera object.
         # Change configuration parameters as needed for the 
         try:
            #TODO - Check parameters
            DinoServo.__servo = PWMOutputDevice(servoPin, True, 0, 10)
         except:
            DinoServo.__servo = None
            DinoLog.logMsg("ERROR - Could not create PWMOutputDevice() object.")
      return DinoServo.__instance


   def isAgitating(self):
      """
      Return True if thread is active and the servo is agitating.
      """
      self.__lock.acquire()
      isAgitating = self.__isAgitating
      self.__lock.release()
      return isAgitating


   def startServo(self, single=True, period=4.0):
      """
      Start servo agitation on the requested period. 

      Parameters
      ----------
      single : bool
         If True, run a signel agitation immediately. 
         If False, agitate every [period] seconds
      period : float
         Time in seconds between agitations.
      
      Returns
      -------
      bool
         True if it successfully started the agitations.
         False if it was already running the thread.
      """
      # Ensure there is no servo agitation thread in progress.
      if(self.isAgitating() == True):
         DinoLog.logMsg("ERROR - Servo agitation already in progress.")
         return False
      
      # Validate input parameters
      if((period < self.MIN_PERIOD) or (period > self.MAX_PERIOD)):
         DinoLog.logMsg("ERROR - Invalid servo agitation period=[" + str(period) + "].")
         return False

      # Record settings and start thread
      self.__period  = float(period)
      self.__stop.set()
      self.__single  = single
   
      # Start thread.
      try:
         self.__stop.clear()
         self.__thread = Thread(target=self.__run, args=(self.__stop, self.__lock, period,)).start()
         sleep(0.5)
         status = self.isAgitating()
      except:
         DinoLog.logMsg("ERROR - Could not start servo agitation thread.")
         status = False
      return status


   def stopServo(self):
      """ 
      Stop thread to agitate the servo. 

      Return
      ------
      bool
         True if the agitation thread was stopped.
      """
      self.__stop.set()
      try:
         self.__thread.join()
         self.__thread = None
      except:
         return False
      return self.isAgitating()


   def __run(self, stopEvent, lock, period):
      """ 
      Thread for Servo. 

      The thread runs once for a single agitation (for testing) or
      continuosly for a stream of agitations separated by a known period. 
      If run continuosuly, the application must call stopServo() to 
      terminate the thread.

      Exit the loop if an error is encountered when commanding the servo
      or when the stopEvent flag is set through the stopServo() function.

      Parameter
      ---------
      stopEvent : threading.Event
         Flag to stop this thread from the main application.
         Set by calling the function stopServo()
      lock : threading.RLock
         Re-entrant safe lock to edit self.__isAgitating variable.
         This is set when the thread starts and cleared when the thread ends.
         Used by the application to check whether the thread is started 
         to agitate the dinos on a regular schedule.
      period : float
         Time in seconds between agitations.
      """
      # Set protected flag to show thread has started
      lock.acquire()
      self.__isAgitating = True
      lock.release()

      # Run main loop for a single or continuous mode.
      firstTime = True
      faultFound = False
      while(((firstTime == True) or (self.__single == False)) and (stopEvent.isSet() == False) and (faultFound == False)):
         firstTime = False

         # Start new recording. If successful, increment the recording counter.
         try:
            #TODO add servo command
            DinoLog.logMsg("Servo moved!")
         except:
            DinoLog.logMsg("ERROR - Failed to move servo.")
            faultFound = True

         # Wait until it reaches the end of the recording or
         # the application sends a request to stop the capture.
         startTime = DinoTime.getMET() 
         currDuration = DinoTime.getMET() - startTime
         while((currDuration <= period) and (stopEvent.isSet() == False and (faultFound == False))):
            time.sleep(0.1)
            currDuration = DinoTime.getMET() - startTime

      # Clear protected flag to show thread has started
      lock.acquire()
      self.__isAgitating = False
      lock.release()
      stopEvent.set()

   
