###############################################################################
# Setup General
# - Run the following commands to ensure the RasPi is up to date:
#    sudo apt-get update
#    sudo apt-get upgrade
#    sudo apt-get install python3-pip
#
# Setup EnviroHat Installation:
#      curl https://get.pimoroni.com/envirophat | bash
#
# References:
# - EnviroHat Docs: https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-phat
###############################################################################

# Time 
import time

# Envirophat 
from envirophat import light    # light sensor
from envirophat import leds     # control leds on the board
from envirophat import weather  # temperature and pressure sensors
from envirophat import motion   # accelerometer sensor


###############################################################################
# Constants
###############################################################################


###############################################################################
# Local variables initialized to zero
###############################################################################
lightReading = 0
r            = 0
g            = 0
b            = 0
temperature  = 0
pressure     = 0
x            = 0
y            = 0
z            = 0

###############################################################################
# Configuration
###############################################################################

print("Light, R, G, B, Temperature, Pressure, X, Y, Z")

for i in range(30):

   # Read light sensor intensity and RGB (not sure if that is needed)
   lightReading   = light.light()
   #r, g, b = light.rgb()

   # Read temperature and pressure
   temperature = weather.temperature()
   pressure    = weather.pressure(unit='hPa')

   # Read acceleration 
   x, y, z = motion.accelerometer()

   # Print readings
   print(lightReading, r, g, b, temperature, pressure, x, y, z)
   
   # Sleep for 1 second
   sleep(1)  


###
# End of main loop.
###   






