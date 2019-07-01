###############################################################################
#
#                              DinoCalibrate
#
# Programmer            Version         Date
# Fred Bourbour          1.0           12/29/18
##############################################################################

# runs with python2
import csv
from matplotlib import style
from matplotlib import pyplot as plt
import numpy as np
import array
import sys
import os.path

if(sys.argv[1] == ""):
 if (os.path.isfile('DinoCalibrate.csv') == false):
  print('No Spectrum file was found')
  exit
 else:
  fileName = 'Dino.csv'
else:
 fileName = sys.argv[1]
 
if(sys.argv[2] == ""):
 print("No reference wavelength was provided")
 exit

print(fileName) 

style.use('ggplot')
y = np.loadtxt(fileName,
                  unpack = True,
                  delimiter = ' ')

ysize = len(y) 
y_max = 0
x_max = 0
i = 0
x = [0] * ysize
for i in range (ysize): 
 x[i] = i

for i in range (ysize):
 if(y[i] > y_max):
    y_max = y[i]
    x_max = i

offset = int(sys.argv[2]) - x_max

print(offset)
file = open("offset.txt", "w")
file.write(str(offset))
file.close()
