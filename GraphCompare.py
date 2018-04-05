#Code by Matt Lubas, Eric Wirth, and Alfred Rwagaju on finding tidal volume for
#both expected values from Arduino and actual values from Kinovea.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import xlrd


def TidalVolume(file):
    """Name csv or xls file to take the data, find local maximums and minimums
    using numpy and argrelextrema. Reports a list of tidal volumes between
    local minimums and maximums. Plots this as well. """

    if file[-4:] == ".csv":
        headers = ['d', 't']
        df = pd.read_csv(file, names = headers)
    
    elif file[-4:] == ".xls":
        df = pd.read_excel(file)
    else:
        print("Error in file input... please put a .csv or .xls file.")
        

    t_start = (df['t'][0])

    df['t'] = (df['t'] - t_start) /1000000
    d = df['d']
    print(df['t'])
    
    global x 
    global t_expected
    x= [] #create list of x in order to use floats instead of strings.
    for item in d:
        
        if item[:5] == "Tidal":
            item = 0
       
        x.append(float(item))
                              

    #turns the list into a numpy array for finding max and mins
    x_array = np.array(x) 

    # for local maxima
    argrelextrema(x_array, np.greater)

    # for local minima
    argrelextrema(x_array, np.less)

    #Finds all the local mins and maxes
    tv_maxes = x_array[argrelextrema(x_array, np.greater)]
    tv_mins = x_array[argrelextrema(x_array, np.less)]

    #Finds the tidal volume by the difference between the local maxes and mins.
    tv = tv_maxes - tv_mins
    print(tv)

    t_expected = df['t']

    plt.plot(tv)
    plt.show()
    return x_array, t_expected

#TidalVolume("R-1-1.4-1.csv")
#TidalVolume("R-1-1.4-1.xls")


TidalVolume("R-3-3-1.csv")

Fs = 240.0  # sampling rate
Ts = 1.0/Fs # sampling interval

df = pd.read_excel("R-3-3-1.xls")
print(df)

length =len(df.index)

first_row = 16

points = length- first_row
d = []
t = []

for i in range(first_row,points):
    temp=df.iloc[i, 0]
    d.append(float(temp))

for i in range(first_row,points):
    temp=df.iloc[i, 2]
    t_adjusted = (float(temp))/Fs #Adjusts to same framerate
    t.append(t_adjusted)


x_array = np.array(d) 

# for local maxima
argrelextrema(x_array, np.greater)

# for local minima
argrelextrema(x_array, np.less)

#Finds all the local mins and maxes
tv_maxes = x_array[argrelextrema(x_array, np.greater)]
tv_mins = x_array[argrelextrema(x_array, np.less)]

plt.plot(t,d,'r-', t_expected,x,'b-')
plt.show()

print(tv_maxes)
print(tv_mins)

#Finds the tidal volume by the difference between the local maxes and mins.
tv = tv_maxes - tv_mins
print(tv)



