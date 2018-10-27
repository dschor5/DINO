
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

# Camera recording duration in seconds
CAMERA_REC_DURATION = 60.0

# Servo agitation interval in seconds
SERVO_AGITATION_INTERVAL = 4.0

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
I_VELOCITY_X      = 2   # Float      
I_VELOCITY_Y      = 3   # Float
I_VELOCITY_Z      = 4   # Float
I_ACCELERATION    = 5   # Float
I_ATTITUDE_X      = 6   # Float
I_ATTITUDE_Y      = 7   # Float
I_ATTITUDE_Z      = 8   # Float
I_ANG_VEL_X       = 9   # Float
I_ANG_VEL_Y       = 10  # Float
I_ANG_VEL_Z       = 11  # Float
I_WARNING_LIFTOFF = 12  # Integer
I_WARNING_RCS     = 13  # Integer
I_WARNING_ESCAPE  = 14  # Integer
I_WARNING_CHUTE   = 15  # Integer
I_WARNING_LANDING = 16  # Integer
I_WARNING_FAULT   = 17  # Integer 
I_LIGHT_RED       = 18  # Integer
I_LIGHT_GREEN     = 19  # Integer
I_LIGHT_BLUE      = 20  # Integer
I_LIGHT_CLEAR     = 21  # Integer
I_TEMPERATURE     = 22  # Float
I_PRESSURE        = 23  # Float
I_ACCEL_X         = 24  # Float
I_ACCEL_Y         = 25  # Float
I_ACCEL_Z         = 26  # Float
I_MAG_X           = 27  # Float
I_MAG_Y           = 28  # Float
I_MAG_Z           = 29  # Float
I_SIZE            = 30


