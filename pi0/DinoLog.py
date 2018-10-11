import time
import os
import sys

from DinoTime import DinoTime

class DinoLog:

	""" Initialization. Starts a new log file. """
	def __init__(self, folder, filename):
		DinoTime() # Initialize time functions
		timestamp = DinoTime.getTimestampStr()
		self.__filepath = folder + "/" + filename + timestamp + ".txt"
		if(not os.path.exists(os.path.dirname(self.__filepath))):
			os.mkdir(os.path.dirname(self.__filepath))
		self.__fp = None
		self.log("Log file \"" + self.__filepath + "\" initialized.")
		

	""" Log a message. """
	def log(self, msg):
		# Log entries include both the current time and the MET.
		timeStr = DinoTime.getTimestampStr()
		metStr  = "{0:.2f}".format(DinoTime.getMET())

		# Format for log messages
		logEntry = timeStr + " - " + metStr + " - " + msg + "\n"

		# Log the message. Keep the file open. 
		if(self.__fp is None):
			self.__fp = open(self.__filepath, 'a')
		self.__fp.write(logEntry)
		self.__fp.flush()		


	def closeLog(self):
		self.__fp.close()
		self.__fp = None
