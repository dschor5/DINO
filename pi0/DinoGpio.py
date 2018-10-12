try:
	useStub = False
	
except:
	print("ERROR - GPIO not loaded.")
	useStub = True


from DinoTime import *
from DinoLog  import *


class DinoSpectrometer:

	__instance = None

	""" Singleton instance. """
	def __new__(cls):
		if(DinoGpio.__instance is None):
			DinoGpio.__instance = object.__new__(cls)
		return DinoGpio.__instance


