
###############################################################################
# Constants
###############################################################################

# Colors for printing output using ANSI escape sequences. 
# From: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
COLORS = {
   'TEST_PASS'  : '\033[92m',   # Green
   'TEST_FAIL'  : '\033[91m',   # Red
   'VALUE'      : '\033[93m',   # Yellow
   'NORMAL'     : '\033[0m',    # White
   'HEADING'    : '\033[95m',   # Magenta
   'SUBHEADING' : '\u001b[36m', # Cyan
   'DECOR'      : '\033[94m',   # Purple
   'BOLD'       : '\033[1m'     # White/bold
   }


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
COOLER_PIN = 12


