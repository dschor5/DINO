###############################################################################
# Setup General
# - Run the following commands to ensure the RasPi is up to date:
#    sudo apt-get update
#    sudo apt-get upgrade
#    sudo apt-get install python3-pip
#
# - Install gpio configuration
#    sudo apt install pigpio
# - Enable GPIO deamon 
#    sudo systemctl enable pigpiod
#
# References:
# - GPIO Docs:      https://gpiozero.readthedocs.io/en/stable/api_output.html
###############################################################################

# Python libraries
from time       import sleep
from gpiozero   import LED        # GPIO interface
from gpiozero   import PWMOutputDevice



###############################################################################
# Constants
###############################################################################

# GPIO Pin numbers
# From: Terry's email.
SERVO_PIN  = 18
HEATER_PIN = 23
FAN_PIN    = 24


###############################################################################
# Local variables
###############################################################################

# Define objects to control external hardware devices.
# Use the "LED" object because it has the on/off capability required.
servoControl  = PWMOutputDevice(SERVO_PIN, True, 0, 10)
heaterControl = LED(HEATER_PIN)
fanControl    = LED(FAN_PIN)


###############################################################################
# Configuration
###############################################################################


###############################################################################
# Main Program
###############################################################################


print("Turn Servo ON for 10 seconds")
servoControl.on()
servoControl.value = 1
sleep(10)
print("Turn Servo OFF")
servoControl.off()
servoControl.value = 0

print("Turn Heater ON for 10 seconds")
heaterControl.on()
sleep(10)
print("Turn Heater OFF")
heaterControl.off()

print("Turn Fan ON for 10 seconds")
fanControl.on()
sleep(10)
print("Turn Fan OFF")
fanControl.off()

