###########################################################################################
#
#
#                               DinoLab Tester
#
###########################################################################################

from guizero import App, Text
from guizero import PushButton
import os
import csv
import glob
#import matplotlib.pyplot as plt


app = App(title="DinoLab Tester")



def test_servo():
  print("Testing the Servo Motor")
  os.system("sudo python3 test.py DinoServo")

def test_camera():
  print("Testing the Camera")
  os.system("sudo python3 test.py Camera")


def test_spectrometer():
  print("Testing the Spectrometer")
  os.system("sudo python3 test.py DinoSpectrometer")
  spectrum_files = glob.glob ("*.csv")
  last_spectrum_file = max(spectrum_files,key = os.path.getctime)
  print (last_spectrum_file)
  os.system("sudo python DinoSpectrograph.py " + last_spectrum_file)

def test_heater():
  print("Testing the Heater")
  os.system("sudo python3 test.py DinoThermalControl")


def test_serial():
  print("Testing the Serial Port")
  os.system("sudo python3 test.py DinoSerial")

def test_simulation():
  print("Testing the Serial Port")
  os.system("sudo python3 test.py DinoSim")
  
 
button1 = PushButton(app, command=test_spectrometer, text="Spectrometer")
button2 = PushButton(app, command=test_camera, text="Camera      ")
button3 = PushButton(app, command=test_servo, text="Servo       ")
button4 = PushButton(app, command=test_heater, text="Thermal Control")
button5 = PushButton(app, command=test_serial, text="Serial         ")
button6 = PushButton(app, command=test_simulation, text="Run Simulation")


button1.width = 12
button2.width = 12
button3.width = 12
button4.width = 12
button5.width = 12
button6.width = 12

button1.padding(5,5)
button2.padding(5,5)
button3.padding(5,5)
button4.padding(5,5)
button5.padding(5,5)
button6.padding(5,5)

app.display()