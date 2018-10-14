from DinoConstants import *
from DinoTime      import *
from DinoLog       import *

try:
   from picamera import PiCamera # NoIR camera
except:
   print(COLORS['TEST_FAIL'] + "ERROR" + COLORS['NORMAL'] + " - GPIO not loaded.")


class DinoCamera(object):

   __instance = None

   """ Singleton instance. """
   def __new__(cls, folder, filename):
      if(DinoCamera.__instance is None):
         DinoCamera.__instance = object.__new__(cls)
         DinoCamera.__folder = folder
         DinoCamera.__filename = filename
         DinoCamera.__filepath = ""
         DinoCamera.__isRecording = False
         DinoCamera.__recStartMet = 0
         try:
            DinoCamera.__camera = PiCamera()
         except:
            DinoLog.logMsg("ERROR - Could not create PiCamera() object.")
      return DinoCamera.__instance


   def isRecording(self):
      return self.__isRecording


   def getFilename(self):
      return self.__filepath   

   """ Returns True for success. """
   def startRecording(self):
      status = True
   
      if(self.__isRecording == True):
         DinoLog.logMsg("ERROR - PiCamera already recording.")
         status = False
      else:

         timestamp = DinoTime.getTimestampStr()
         self.__filepath = self.__folder + "/" + self.__filename + "_" + timestamp + ".h264"
         self.__recStartMet = DinoTime.getMET()
         self.__isRecording = True

         try:
            self.__camera.resolution = (800, 600)
            self.__camera.framerate  = 15
            self.__camera.start_recording(self.__filepath);
            DinoLog.logMsg("Start PiCamera file=[" + self.__filepath + "]")
         except:
            DinoLog.logMsg("ERROR - Failed to start PiCamera file=[" + self.__filepath + "]")
            status = False
         
      return status

   """ Returns recording time or -1 if failed. """      
   def stopRecording(self):
      recTime = 0
      
      if(self.__isRecording == False):
         DinoLog.logMsg("WARNING - PiCamera already stopped.")
         recTime = -1
      else:
         recTime = DinoTime.getMET() - self.__recStartMet
         self.__recStartMet = 0
         self.__isRecording = False

         try:
            self.__camera.stop_recording()
            DinoLog.logMsg("Stop PiCamera file=[" + self.__filepath + "] " + \
               "duration=[" + str(recTime) + "sec]")
         except:
            DinoLog.logMsg("ERROR - Failed to stop PiCamera PiCamera file=[" + self.__filepath + "] ")
         
      return recTime


