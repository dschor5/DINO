###############################################################################
# Setup General
# - Run the following commands to ensure the RasPi is up to date:
#    sudo apt-get update
#    sudo apt-get upgrade
#    sudo apt-get install python3-pip
#
# Serial Port
#       pip install pyserial
#
# Setup EnviroHat Installation:
#      curl https://get.pimoroni.com/envirophat | bash
#
# Setup PiCamera Installation:
#      sudo apt-get install python-picamera python3-picamera
#     
# References:
# - GPIO Docs:      https://gpiozero.readthedocs.io/en/stable/api_output.html
# - PiCamera Docs:  https://picamera.readthedocs.io/en/release-1.13/recipes1.html
# - EnviroHat Docs: https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-enviro-phat
# - Serial Docs:    https://pythonhosted.org/pyserial/pyserial.html#installation
###############################################################################

# Python libraries
from time       import *        # Time library
from gpiozero   import *        # GPIO interface
from serial     import *        # Serial communication

# Envirophat 
from envirophat import light    # light sensor
from envirophat import leds     # control leds on the board
from envirophat import weather  # temperature and pressure sensors
from envirophat import motion   # accelerometer sensor

# Pi Camera
from picamera   import PiCamera # NoIR camera


###############################################################################
# Constants
###############################################################################

# Possible flight states sent by New Shepard vehicle to the payload.
# From: NR-BLUE-W0001 (RevA) Feather Frame Payload User's Guide (002).pdf
FLIGHT_STATES = {
   'NONE'         : '@',   # No flight state has been reached yet 
                           #    (typically the time prior to liftoff).
   'LIFTOFF'      : 'A',   # This state is triggered once sensed acceleration 
                           #    first changes due to engine ignition.
   'MECO'         : 'B',   # This state is triggered after the rocket's main engine 
                           #    cuts out, and the flight enters its coast stage.
   'SEPARATION'   : 'C',   # This state occurs after the rocket and capsule 
                           #    separate, shortly before the microgravity 
                           #    portion of the flight begins.
   'COAST_START'  : 'D',   # This state indicates the beginning of the cleanest 
                           #    microgravity operations onboard the capsule, 
                           #    most experiments should begin logging data at this time.
   'APOGEE'       : 'E',   # This state occurs when the vehicle has reached its 
                           #    maximum altitude and begins to descend.
   'COAST_END'    : 'F',   # This state indicates the end of microgravity operations 
                           #    onboard the capsule, as we begin to experience 
                           #    atmospheric accelerations. Many experiments will 
                           #    cease logging data at this time.
   'UNDER_CHUTES' : 'G',   # This state indicates that drogue parachutes have 
                           #    deployed and the capsule is in its final descent.
   'LANDING'      : 'H',   # This state occurs after capsule touchdown.
   'SAFING'       : 'I',   # After touchdown, this state indicates that the 
                           #    capsule is venting and safing all energetic systems.
   'FINISHED'     : 'J'    # This state is only ever reached in simulation and 
                           #    indicates the end of the logged flight data.
   }

# Field names within the New Shepard packet received at 10Hz.
# From: NR-BLUE-W0001 (RevA) Feather Frame Payload User's Guide (002).pdf
NL_KEYS = [
   'FLIGHT_STATE',         # 1)  Current flight state as a single ASCII char.
                           #     States defined in FLIGHT_STATES enum above.
   'EXP_TIME',             # 2)  Current experiment time in seconds as decimal number 
                           #     with 2 digits following the decimal point.
   'ALTITUDE',             # 3)  Current vehicle altitude above ground level in feet as a 
                           #     decimal number with 6 digits following the decimal point.
   'VELOCITY_X',           # 4)  Current vehicle velocity in feet per second along the vertical 
                           #     axis of the capsule as a decimal number with 6 digits following
                           #     the decimal point.
   'VELOCITY_Y',           # 5)  Same as VELOCITY_X but for the y-axis.
   'VELOCITY_Z',           # 6)  Same as VELOCITY_X but for the z-axis.
   'ACCELERATION',         # 7)  Magnitude of the current vehicle acceleration in feet per 
                           #     second squared as a decimal number with 6 digits 
                           #     following the decimal point.
   'RESERVED_1',           # 8)  Reserved for future use. Expect "0.000000".
   'RESERVED_2',           # 9)  Reserved for future use. Expect "0.000000".
   'ATTITUDE_X',           # 10) The current vehicle attitude in radians about the x-axis 
                           #     as a decimal number with 6 digits following the decimal point.
   'ATTITUDE_Y',           # 11) Same as ATTITUDE_X but for the y-axis.
   'ATTITUDE_Z',           # 12) Same as ATTITUDE_X but for the z-axis.
   'ANG_VEL_X',            # 13) Current vehicle angular velocity in radians per second
                           #     about the x-axis as a decimal number with 6 digits following 
                           #     the decimal point.
   'ANG_VEL_Y',            # 14) Same as ANV_VEL_X but for y-axis.
   'ANG_VEL_Z',            # 15) Same as ANV_VEL_X but for z-axis.                        
   'LIFTOFF_WARNING',      # 16) Warning triggered on main engine ignition, value is a single 
                           #     digit with 1 when the warning is true and 0 when is false.
   'RCS_WARNING',          # 17) Warning triggered during microgravity phase of flight to notify
                           #     that attitude adjustment in progress. 
                           #     Same format as LIFTOFF_WARNING.
   'ESCAPE_WARNING',       # 18) Warning triggered during the escape motor ignition process. 
                           #     Same format as LIFTOFF_WARNING.
   'CHUTE_WARNING',        # 19) Warning triggered shortly before drogue chute deployments. 
                           #     Same format as LIFTOFF_WARNING.  
   'LANDING_WARNING',      # 20) Warning triggered by altitude shortly before the capsule touches down.
                           #     Same format as LIFTOFF_WARNING.  
   'FAULT_WARNING',        # 21) Warning triggered in anticipation of an abnormally hard landing.
                           #     Same format as LIFTOFF_WARNING.  

# Telemetry keys recorded by the software in addition to the info from the vehicle.
# From: "HAB & DINOLAB Software Command Requirements.xlsx"
TLM_KEYS = [
   'Timestamp',            # Calculated by the software independent of serial packet received.
   'EnvLight',             # From Envirophat light sensor.
   'EnvRed',               # From Envirophat light sensor.
   'EnvGreen',             # From Envirophat light sensor.
   'EnvBlue',              # From Envirophat light sensor.
   'EnvTemperature',       # From Envirophat weather sensor.
   'EnvPressure',          # From Envirophat weather sensor.
   'EnvAccelerationX',     # From Envirophat motion sensor.
   'EnvAccelerationY',     # From Envirophat motion sensor.
   'EnvAccelerationZ'      # From Envirophat motion sensor.
   ]

# Temperature thresholds in degree Celsius to match sensors
# From: "HAB & DINOLAB Software Command Requirements.xlsx"
TURN_ON_HEATER  = 16.9 # Celsius. Equivalent to 62.5F.
TURN_OFF_HEATER = 21.1 # Celsius. Equivalent to 70.0F.
TURN_ON_COOLER  = 25.8 # Celsius. Equivalent to 78.5F.
TURN_OFF_COOLER = 18.3 # Celsius. Equivalent to 65.0F.

# GPIO Pin numbers
# From: Terry's email.
SERVO_PIN  = 18
HEATER_PIN = 16
FAN_PIN    = 12

# Stop servo agitation when acceleration measured > 0.1g.
# From: "HAB & DINOLAB Software Command Requirements.xlsx"
# TODO - See note when the threshold is used.
SERVO_END_AGITATION_THRESHOLD = 0.1

# Servo duty cycle
SERVO_DUTY_CYCLE = 5 # Sec.
SERVO_DURATION   = 3 # Iterations. ~180 degrees.

###############################################################################
# Local variables
###############################################################################
# Reference point for calculating MET
startTime = time.time() 
met       = 0

# Telemetry buffer. 
tlmBufferSensor = dict.fromkeys(TLM_KEYS)

# Serial telemetry buffer.
tlmBufferSerial = dict.fromkeys(NL_KEYS)

# Define objects to control external hardware devices.
# Use the "LED" object because it has the on/off capability required.
servoControl  = LED(SERVO_PIN)
heaterControl = LED(HEATER_PIN)
fanControl    = LED(FAN_PIN)

# Servo state variables
servoMoving    = False
servoMoveCount = 0
servoLastMove  = 0


###############################################################################
# Configuration
###############################################################################

# Turn off envirophat rgb led to prevent any light contamination.
leds.off()

# Configure the camera settings
camera.resolution = (800, 600)
camera.framerate  = 15

# Serial port settings. 
# From: NR-BLUE-W0001 (RevA) Feather Frame Payload User's Guide (002).pdf
serialPort = serial.Serial(
   port        = '/dev/ttyAMA0',
   baudrate    =  115200,
   parity      = serial.PARITY_NONE,
   stopbits    = serial.STOPBITS_ONE,
   bytesize    = serial.EIGHTBITS,
   timeout     = 0.1 # 10 Hz packets 
   )

outputFp = open('dataCapture', 'w')

###############################################################################
# Log Function
###############################################################################
def log(msg):
   currTime = time.time() - startTime
   logFp = open('log.txt', 'a')
   line = str(currTime) + " " + msg
   logFp.write(line)
   logFp.close()

###############################################################################
# Main Program
###############################################################################

# Start recording 
log("Camera=START")
camera.start_recording('/home/pi/video.h264')

# Flush serial port input buffer before main loop
serialPort.reset_input_buffer()
serialPort.write("$")

while(1):
   ###
   # Update internal mission elapsed time.
   ###
   met = time.time() - startTime

   ###
   # Read serial packet
   ###
   # Sync to the beginning of a new packet
   syncByte = serialPort.read()
   while(syncByte not in HAB_STATES):
      syncByte = serialPort.read()
   bytes = serialPort.read(200)
   tlmPoints = (str(bytes)).split(',')
   # Parse serial packet
   try:
      tlmBufferSerial['FLIGHT_STATE']    = str(syncByte)
      tlmBufferSerial['EXP_TIME']        = float(tlmPoints[0])
      tlmBufferSerial['ALTITUDE']        = float(tlmPoints[1])
      tlmBufferSerial['VELOCITY_X']      = float(tlmPoints[2])
      tlmBufferSerial['VELOCITY_Y']      = float(tlmPoints[3])
      tlmBufferSerial['VELOCITY_Z']      = float(tlmPoints[4])
      tlmBufferSerial['ACCELERATION']    = float(tlmPoints[5])        
      tlmBufferSerial['RESERVED_1']      = float(tlmPoints[6])        
      tlmBufferSerial['RESERVED_2']      = float(tlmPoints[7])        
      tlmBufferSerial['ATTITUDE_X']      = float(tlmPoints[8])        
      tlmBufferSerial['ATTITUDE_Y']      = float(tlmPoints[9])        
      tlmBufferSerial['ATTITUDE_Z']      = float(tlmPoints[10])        
      tlmBufferSerial['ANG_VEL_X']       = float(tlmPoints[11])       
      tlmBufferSerial['ANG_VEL_Y']       = float(tlmPoints[12])       
      tlmBufferSerial['ANG_VEL_Z']       = float(tlmPoints[13])       
      tlmBufferSerial['LIFTOFF_WARNING'] = int(tlmPoints[14])       
      tlmBufferSerial['RCS_WARNING']     = int(tlmPoints[15])       
      tlmBufferSerial['ESCAPE_WARNING']  = int(tlmPoints[16])       
      tlmBufferSerial['CHUTE_WARNING']   = int(tlmPoints[17])       
      tlmBufferSerial['LANDING_WARNING'] = int(tlmPoints[18])       
      tlmBufferSerial['FAULT_WARNING']   = int(tlmPoints[19])  
   except IndexError:
      log("Error reading serial data.")
      pass # Keep whatever was recorded from the partial packet.
   
   ###
   # Control Servo
   ###
   # From: "HAB & DINOLAB Software Command Requirements.xlsx"
   # - Start agitation on capsule separation (~160 sec)
   #   Initiate SERVO agitation (180 deg) 5 sec apart. 
   # - End agitation when sensed acceleration > 0.1g (~342 sec)
   
   # TODO - This does not make sense. Shouldn't this be when the 
   #        sensed acceleration is less than 0.1g meaning that 
   #        we are approaching microgravity?
   if(tlmBufferSerial['ACCELERATION'] > SERVO_END_AGITATION_THRESHOLD):
      log("Servo=OFF")
      servoControl.off()
      
   # After separation, toggle servo on/off.
   elif(tlmBufferSerial['FLIGHT_STATE'] > FLIGHT_STATES['SEPARATION']):
      
      # If it's been 5 sec since the last move, then initiate it again.
      if(servoMoving == False and (servoLastMove+SERVO_DUTY_CYCLE) <= met):
         servoMoving    = True
         servoMoveCount = 0
         servoLastMove  = met
         log("Servo=ON")
         servoControl.n()
      
      # If it's been 3 iterations, then stop the servo.
      if(servoMoving == True):
         if(servoMoveCount > SERVO_DURATION):
            log("Servo=OFF")
            servoControl.off()
         servoMoveCount = servoMoveCount + 1
            
   
   ###
   # Read other sensors
   ###
   
   # Read light sensor intensity and RGB (not sure if that is needed)
   #tlmBufferSensor['EnvLight'] = light.light()
   #r, g, b = light.rgb()
   #tlmBufferSensor['EnvRed']   = r 
   #tlmBufferSensor['EnvGreen'] = g
   #tlmBufferSensor['EnvBlue']  = b

   # Read temperature and pressure
   #tlmBufferSensor['EnvTemperature'] = weather.temperature()
   #tlmBufferSensor['EnvPressure']    = weather.pressure(unit='hPa')

   # Read acceleration 
   #x, y, z = motion.accelerometer()
   #tlmBufferSensor['EnvAccelerationX'] = x
   #tlmBufferSensor['EnvAccelerationY'] = y
   #tlmBufferSensor['EnvAccelerationZ'] = z

   ###
   # Control heater/cooler
   ###
   #if(tlmBufferSensor['EnvTemperature'] < TURN_ON_HEATER):
   #   log("Heater=ON")
   #   heaterControl.on()
      
   #elif(tlmBufferSensor['EnvTemperature'] > TURN_OFF_HEATER):
   #   log("Heater=OFF")
   #   heaterControl.off()
   
   #if(tlmBufferSensor['EnvTemperature'] < TURN_ON_COOLER):
   #   log("Cooler=ON")
   #   fanControl.on()
      
   #elif(tlmBufferSensor['EnvTemperature'] > TURN_OFF_COOLER):
   #   log("Cooler=OFF")
   #   fanControl.off()
      
      
   ###
   # Record data to CSV file
   ###
   # TODO - Add state of all software controlled pins. 
   outputFp.write(str(met))
   outputFp.write(str(tlmBufferSerial))
   outputFp.write(str(tlmBufferSensor))
   outputFp.write("\n")


###
# End of main loop.
###   
   
# Stop recording
log("Camera=STOP")
camera.stop_recording()

# Stop recording data
outputFp.close()





