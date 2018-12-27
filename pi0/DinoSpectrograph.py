import csv
from matplotlib import style
from matplotlib import pyplot as plt
import numpy as np
import array
import plotly.plotly as p


style.use('ggplot')
y = np.loadtxt('Dino.csv',
                  unpack = True,
                  delimiter = ' ')

ysize = len(y) 

i = 0
x = [0] * ysize
for i in range (ysize): 
 x[i] = i 

plt.plot(x,y)

a = np.asarray(x)
b = np.asarray(y)

plt.plot(a,b)
plt.title('Spectrometer')
plt.ylabel('Amplitude')
plt.xlabel('Wavelength')
plt.show()
