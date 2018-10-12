try:
	useStub = False
	
except:
	print("ERROR - Serial interface not loaded.")
	useStub = True


from DinoTime import *
from DinoLog  import *


class DinoSerial:

	__instance = None

	""" Singleton instance. """
	def __new__(cls):
		if(DinoSerial.__instance is None):
			DinoSerial.__instance = object.__new__(cls)
		return DinoSerial.__instance


