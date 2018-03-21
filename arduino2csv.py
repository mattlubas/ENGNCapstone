#!/usr/bin/env python3
#This code exports data from arduino to excel
from serial import Serial

ARDUINO = '/dev/cu.usbmodem414'
BAUD    = 57600
OUTFILE = 'arduino.csv'

arduino = Serial(ARDUINO, BAUD)

print('Connected; writing to file ' + OUTFILE)

file = open(OUTFILE, 'w')

while True:

    c = arduino.read().decode('utf8')

    file.write(c)

arduino.close()
file.close()


