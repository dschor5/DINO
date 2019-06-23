
###############################################################################
# Constants
###############################################################################

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

#number of seconds after power is applied to the Dino and before ignition
POWER_TO_DINO_BEFORE_IGNITION = 300.00

#Mission events happening and their number of seconds after ignition

MAIN_ENGIN_IGNITION_EVENT = 0
LIFT_OFF_EVENT = 7.0
COST_START_EVENT = 177.0
COST_END_EVENT = 348.0

# Camera recording duration in seconds
CAMERA_REC_DURATION = 30.0

# Servo agitation interval in seconds
SERVO_AGITATION_INTERVAL = 4.0

# Spectrometer capture interval in seconds
SPECTROMETER_CAPTURE_INTERVAL = 10.0

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

# Column names for parsing data
I_FLIGHT_STATE    = 0   # Integer
I_ALTITUDE        = 1   # Float
I_ACCELERATION    = 2   # Float
I_LIGHT_RED       = 3   # Integer
I_LIGHT_GREEN     = 4   # Integer
I_LIGHT_BLUE      = 5   # Integer
I_LIGHT_CLEAR     = 6   # Integer
I_TEMPERATURE     = 7   # Float
I_PRESSURE        = 8   # Float
I_ACCEL_X         = 9   # Float
I_ACCEL_Y         = 10  # Float
I_ACCEL_Z         = 11  # Float
I_SIZE            = 12


