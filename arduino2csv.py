#!/usr/bin/env python3
#This code exports data from arduino to excel

import serial
#if having an import error, pip3 install pyserial using terminal.

ARDUINO = '/dev/cu.usbmodem1649921'
BAUD    = 57600
OUTFILE = 'arduino.csv'

arduino = serial.Serial(ARDUINO, BAUD)

print('Connected; writing to file ' + OUTFILE)

file = open(OUTFILE, 'w')

while True:

    c = arduino.read().decode('utf8')

    file.write(c)

arduino.close()
file.close()


