try:
	from picamera import PiCamera # NoIR camera
	useStub = False
except:
	print("ERROR - PiCamera not loaded.")
	useStub = True


from DinoTime import *
from DinoLog  import *


class DinoCamera:

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
		return DinoCamera.__instance


	def isRecording(self):
		return self.__isRecording


	def getFilename(self):
		return self.__filepath	

	""" Returns True for success. """
	def startRecording(self):
		if(self.__isRecording == True):
			DinoLog.logMsg("ERROR - PiCamera already recording.")
			return False

		timestamp = DinoTime.getTimestampStr()
		self.__filepath = self.__folder + "/" + self.__filename + "_" + timestamp + ".h264"
		self.__recStartMet = DinoTime.getMET()
		self.__isRecording = True

		if(useStub == True):
			DinoLog.logMsg("STUB - Start PiCamera file=[" + self.__filepath + "]")
			return False
		
		camera.resolution = (800, 600)
		camera.framerate  = 15
		camera.start_recording(self.__filepath);
		DinoLog.logMsg("Start PiCamera file=[" + self.__filepath + "]")
		return True

	""" Returns recording time or -1 if failed. """		
	def stopRecording(self):
		if(self.__isRecording == False):
			DinoLog.logMsg("WARNING - PiCamera already stopped.")
			return -1

		recTime = DinoTime.getMET() - self.__recStartMet
		self.__recStartMet = 0
		self.__isRecording = False

		if(useStub == True):
			DinoLog.logMsg("STUB - Stop PiCamera file=[" + self.__filepath + "] " + \
				"duration=[" + str(recTime) + "sec]")
			return recTime

		camera.stop_recording()
		DinoLog.logMsg("Stop PiCamera file=[" + self.__filepath + "] " + \
			"duration=[" + str(recTime) + "sec]")
		return recTime


