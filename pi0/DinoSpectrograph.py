###############################################################################
#
#                              DinoSpectrograph
#
# Programmer            Version         Date
# Fred Bourbour          1.0           12/27/18
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
 if (os.path.isfile('Dino.csv') == false):
  print('No Spectrum file was found')
  exit
 else:
  fileName = 'Dino.csv'
else:
 fileName = sys.argv[1]
 
print(fileName) 

style.use('ggplot')
y = np.loadtxt(fileName,
                  unpack = True,
                  delimiter = ' ')

ysize = len(y) 

i = 0
x = [0] * ysize
for i in range (ysize): 
 x[i] = i 


a = np.asarray(x)
b = np.asarray(y)

plt.plot(a,b)
plt.title('Spectrometer')
plt.ylabel('Amplitude')
plt.xlabel('Wavelength')
plt.show()
