
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
   ]

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

# Stop servo agitation when acceleration measured > 0.1g.
# From: "HAB & DINOLAB Software Command Requirements.xlsx"
# TODO - See note when the threshold is used.
SERVO_END_AGITATION_THRESHOLD = 0.1

# Servo duty cycle
SERVO_DUTY_CYCLE = 5 # Sec.
SERVO_DURATION   = 3 # Iterations. ~180 degrees.
