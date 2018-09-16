#!/usr/bin/env python
#Fred Bourbour                  8/3/18
########################################################################################################
# This python script runs on the HAB pi3 computer. It is started on power up by adding the following line
# to the bottom of the /etc/rc.local file before the exit 0 line
# sudo python /home/pi/HAB/HABSim03.py 
#
###############################################Python Library Imports######################
import time
import serial
import string
import enum
from random import randint
from time import sleep
from sense_hat import SenseHat

sense = SenseHat()
sense.set_imu_config(True,True,True) # enable compass, gyro, and accelerometer 
print("senseHATis Running")
#######Turn a blue pixel on to indicate the program is running on powerup ##################
sense.clear()
pixel_x = 4
pixel_y = 4
red = 0
green = 0
blue = 255
sense.set_pixel(pixel_x, pixel_y, red, green, blue)

####################################New Shepard Flight Flight Status ##################################
 
IDLE = 0
LIFT_OFF=1
MECO=2
SEPARATION=3
COAST_START=4
APOGEE=5
COAST_END=6
UNDER_SHOOT=7
LANDING=8
SAFING=9
FINISHED=10

#####################Initialize variables and buffers ###################################################
CurrentStatus = IDLE
start_time = time.time()
transmit_buffer=list()
state_buffer=list()
transmit_buffer=['$','@','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?']
state_buffer=['@','A','B','C','D','E','F','G','H','I','J']
#pressure in atm unit. It is 1.00 at 0 altitude and each value corresponds to the air pressure for 500
# feet increase in altitude. 

pressure = [1.0,0.98,0.96,0.95,0.93,0.91,0.90,0.88,0.86,0.85,0.83,0.80,0.77,0.74,0.71,0.69,0.56,0.46,
                   0.37,0.30,0.24,0.19,0.15,0.11,0.09,0.07,0.06,0.05]

altitude = [0, 500,1000,1500,2000,2500,3000,3500,4000,4500,5000,6000,7000,8000,9000,10000,15000,20000,
            25000,30000,35000,40000,45000,50000,55000,60000,65000,70000]
            
counter=0
zeroGravityEntered=False
zeroGravityExited=False
liftOffAchieved = False
balloonHasLanded = False
#######################Initial Values ###################################################################
acceleration0 = sense.get_accelerometer_raw()
air_pressure0 = sense.get_pressure()

##############################Check LiftOff##############################################################
#Reads the accelerometer x,y, and z componenets. Checks to see if any of the three axis acceleration has
# exceeded 1g.
#########################################################################################################
def checkLiftOff():
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']
    #x = abs(x)
    #y = abs(y)
    #z = abs(z)
    # print(acceleration)
    if (x > 1 or y > 1 or z > 1):
     return True
    else:
     return False   

#############################getAltitude#################################################################
#senseHAT unit of air pressure is millibar. One bar = 1.01325 atm. The senseHAT value is converted to bar
# and then atm for comparison with the values in the table
##########################################################################################################

def getAltitude(air_pressure):
     air_pressure = air_pressure/1000 # convert to bar
     air_pressure = air_pressure/1.01325 #convert to atm
     if(air_pressure < 0.05):
      return 75000
     index = 0
     while index < 27:
      #print(air_pressure)
      if (air_pressure < pressure[index] and air_pressure > pressure[index + 1]):
       return altitude[index] 
      index += 1
    
##############################################################################
# HAB Mission Log 
###############################################################################
def hab_log(hab_message):
     now_time = time.time() - start_time
     log_file_ptr = open('hab_log.txt', 'a')
     line = str(now_time) + " " + hab_message
     log_file_ptr.write(line)
     log_file_ptr.close()
###############################################################################
# blink_leds
# Checks to make sure both pi computers are up running and communicating
###############################################################################
def blink_leds():
  red = 0
  green = 0
  blue = 0
  mission_time = time.time() - start_time
  #print(mission_time)
  pixel_x= 5
  blink_count = 10
  while blink_count:
     pixel_x= 5
     pixel_y= 5
     green = 255        #message received. Turn green pixel on
     sense.set_pixel(pixel_x, pixel_y, red, green, blue)
     sleep(.25)
     green = 0
     sense.set_pixel(pixel_x, pixel_y, red, green, blue)
     sleep(.25)
     blink_count -= 1
     if mission_time >= 10:  # wait 10 seconds  
      red = 255          #no message is received from DinoLAB. Red LED on
      sense.set_pixel(pixel_x, pixel_y, red, green, blue)
      sleep(.25)
      red = 0            #Red LED is OFF
      sense.set_pixel(pixel_x, pixel_y, red, green, blue)
      sleep(.25)
     else: # blink the blue LED
      pixel_x = 4
      pixel_y = 4
      blue = 255          # turn blue LED ON
      sense.set_pixel(pixel_x, pixel_y, red, green, blue)
      sleep(.25)
      blue = 0            # turn blue LED OFF
      sense.set_pixel(pixel_x, pixel_y, red, green, blue)
      sleep(.25)    
sleep(5)
sense.clear() 

#####################Wait For Message From DinoLab ###########################################################
hab_log("HAB Initialized\r\n");
print("HAB Initialized")
blink_leds()

#####################Main Program Loop #######################################################################
while 1:
 temp = sense.get_temperature()
 humidity = sense.get_humidity()
 air_pressure_now = sense.get_pressure()
 mag = sense.get_compass_raw()
 orientation = sense.get_orientation_degrees()
 gyro = sense.get_gyroscope_raw()
 
 humidity = round(humidity,1)
 temp = round(temp,1)
 air_pressure_now = round(air_pressure_now,1) # is in milibar
 ###################get orientation                                                 vfvffc and round it up  
 roll = orientation['roll']
 pitch = orientation['pitch']
 yaw = orientation['yaw']
 roll = round(roll,3)
 pitch = round(pitch,3)
 yaw = round(yaw,3)
 ###################get current time
 current_time = time.time() - start_time
 current_time = round(current_time,2)
 transmit_buffer[2] = current_time
 #if(liftOffAchieved): #testing
  #air_pressure_now = int(raw_input('pressure:'))
#################### Check if zero gravity is entered. If so, must activate the servo to agitate the Dinos 
 if(air_pressure_now < 60): 
  if zeroGravityEntered == False:
   zeroGravityEntered = True
   zeroGravityExited = False
   transmit_buffer[1] = state_buffer[COAST_START]
   print ("Entered Zero Gravity")
   hab_log("Entered Zero Gravity\r\n");
 
 #####################Check if zero gravity is exited. If so, must activate the servo to agitate the Dinos
 
 if (air_pressure_now > 100 and zeroGravityEntered): #balloon has popped.
  if zeroGravityExited == False:
   zeroGravityExited = True
   zeroGravityEntered = False
   transmit_buffer[1] = state_buffer[COAST_END]
   print ("Exited Zero Gravity")
   hab_log("Exited Zero Gravity\r\n");
 
 ######################Check to see if the balloon has landed ###########
  
 if (air_pressure_now >= air_pressure0 and zeroGravityExited): #balloon has landed
  if balloonHasLanded == False:
   balloonHasLanded = True
   transmit_buffer[1] = state_buffer[LANDING]
   print ("HAB Has Landed")
   hab_log("HAB Has Landed\r\n"); 
   
 ######################Check to see if baloon has taken off ############  
   

 if(checkLiftOff() and liftOffAchieved == False):
  liftOffAchieved = True;   
  transmit_buffer[1] = state_buffer[LIFT_OFF]
  print ("HAB TakeOff")
  hab_log("HAB TakeOff\r\n"); 
 #########################Fill Transmit BUffer################################
 altitude_ = getAltitude(air_pressure_now * 1.0)
 transmit_buffer[3] = altitude_
 transmit_buffer[4] = pitch
 transmit_buffer[5] = roll
 transmit_buffer[6] = yaw
 transmit_buffer[7] = temp
 transmit_buffer[8] = humidity
 #transmit_buffer[9] = mag
 #transmit_buffer[10] = orientation
 index=0
 #########################Transmi
 index=0
 #########################Transmit ###########################################
 print string.translate(str(transmit_buffer),None,"")

 #transmit_buffer=['$','@','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?','?']
 time.sleep(1)
 
