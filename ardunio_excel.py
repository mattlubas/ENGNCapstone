#!/usr/bin/env python3
'''
This code exports data from arduino to excel and allows user input of tidal volume and frequency
Authors: Alfred Rwagaju, Professor Simon Levy, Matt Lubas, Eric Wirth
'''

ARDUINO = '/dev/cu.usbmodem1365201'
BAUD    = 57600

from threading import Thread
from time import time
from datetime import datetime
from serial import Serial

def writefile(file, arduino):

    while True:

        try:

            c = arduino.read().decode('utf8')

            file.write(c)

        except:

            return

def error():
    
    print('Please input two legitimate floating-point values')


def create_excel():
    """Creates an Excel file with name and correct serial port"""

    filename = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H-%M-%S') + '.csv'

    print('Writing to ' + filename)

    file = open(filename, 'w')
    
    thread = Thread(target=writefile, args = (file, arduino))
    thread.daemon = True
    thread.start()
    
    

if __name__ == '__main__':

    arduino = Serial(ARDUINO, BAUD)

    filename = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H-%M-%S') + '.csv'

    print('Writing to ' + filename)

    file = open(filename, 'w')
    
    thread = Thread(target=writefile, args = (file, arduino))
    thread.daemon = True
    thread.start()
    

    while True:

        response = input('Enter new tidal volume and frequency (q to quit) > ')

        if response[0].lower() == 'q':
            file.close()
            break

        values = response.split()

        okay = False

        if len(values) == 2:                # did we get two values:
            try:
                [float(x) for x in values]  # are they floating-point numbers?
                okay = True
            except:
                error()
        else:
            error()
            
        if okay:

            file.close()

            filename = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H-%M-%S') + '.csv'

            print('Writing to ' + filename)

            file = open(filename, 'w')
    
            thread = Thread(target=writefile, args = (file, arduino))
            thread.daemon = True
            thread.start()
            
            print('Sending: ' + response)
            arduino.write(response.encode('utf8'))
            


    arduino.close()
    
    


