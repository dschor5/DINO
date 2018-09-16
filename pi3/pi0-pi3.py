#!/usr/bin/env python
print("Hello World")

          
import time
import serial

ser = serial.Serial(
port='/dev/ttyS0',
baudrate = 115200,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1)
counter=0
while 1:
 ser.write('$')
 print("sent $ to pi3")
 time.sleep(1)
 counter += 1
