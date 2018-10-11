###############################################################################
# Setup General
# - Run the following commands to ensure the RasPi is up to date:
#    sudo apt-get update
#    sudo apt-get upgrade
#    sudo apt-get install python3-pip
#
# Setup PiCamera Installation:
#      sudo apt-get install python-picamera python3-picamera
#     
# References:
# - PiCamera Docs:  https://picamera.readthedocs.io/en/release-1.13/recipes1.html
###############################################################################

# Time 
from time import sleep

# Pi Camera
from picamera   import PiCamera # NoIR camera


###############################################################################
# Constants
###############################################################################


###############################################################################
# Local variables
###############################################################################


###############################################################################
# Configuration
###############################################################################


###############################################################################
# Main Program
###############################################################################

# Start recording 
print("Start recording...")
camera = PiCamera()
camera.start_recording('/home/pi/video.h264')

for i in range(30):
   print(i)
   sleep(1)
   
# Stop recording
camera.stop_recording()





