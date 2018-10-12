try:
	from envirophat import light    # light sensor
	from envirophat import leds     # control leds on the board
	from envirophat import weather  # temperature and pressure sensors
	from envirophat import motion   # accelerometer sensor
	useStub = False
	leds.off()
except:
	print("ERROR - EnviropHat not loaded.")
	useStub = True


from DinoTime import *
from DinoLog  import *


class DinoEnvirophat:

	__instance = None

	""" Singleton instance. """
	def __new__(cls):
		if(DinoEnvirophat.__instance is None):
			DinoEnvirophat.__instance = object.__new__(cls)
		return DinoEnvirophat.__instance

	""" Returns tuple with four values for R, G, B, and CLEAR values. """
	def getLightSensorReadings(self):
		if(useStub == True):
			DinoLog.logMsg("STUB - Envirophat read light sensor.")
			return (None, None, None, None)
		return light.raw()
            
	""" Read temperature in degree C. """
	def getTemperature(self):
		if(useStub == True):
			DinoLog.logMsg("STUB - Envirophat read temperature.")
			return None
		return weather.temperature()
   
	""" Return pressure in Pa."""
	def getPressure(self):
		if(useStub == True):
			DinoLog.logMsg("STUB - Envirophat read pressure.")
			return None
		return weather.pressure(unit='Pa')      

	""" Returns tuple for acceleration x, y, and z. """
	def getAcceleration(self):
		if(useStub == True):
			DinoLog.logMsg("STUB - Envirophat read acceleration.")
			return (None, None, None)
		return motion.accelerometer()
   
	""" Returns tuple for mag_x, mag_y, and mag_z readings."""
	def getMagReading(self):
		if(useStub == True):
			DinoLog.logMsg("STUB - Envirophat read magnetometer.")
			return (None, None, None)
		return motion.magnetometer()   


