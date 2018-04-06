#Code by Matt Lubas, Eric Wirth, and Alfred Rwagaju on finding tidal volume for
#both expected values from Arduino and actual values from Kinovea.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy.signal import argrelextrema
import xlrd
import peakutils



def TidalVolume(file):
    """Name csv or xls file to take the data, find local maximums and minimums
    using numpy and argrelextrema. Reports a list of tidal volumes between
    local minimums and maximums. Plots this as well. """

    k_ratio = 0.2485/0.269 #conversion because k value was not re-calculated when
    #we ran the first sampling.

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
    
    global tv_expected
    global x 
    global t_expected
    x= [] #create list of x in order to use floats instead of strings.
    for item in d:
        
        if item[:5] == "Tidal":
            item = 0

        temp = float(item) *k_ratio
        x.append(float(temp))

    x_mean = sum(x)/ len(x)
    #print(x_mean)
    x_mode = max(set(x), key=x.count)
    #print (x_mode)

    #turns the list into a numpy array for finding max and mins
    x_array = np.array(x) 

    # for local maxima
    
    #argrelextrema(x_array, np.greater)

    
    # for local minima
    #argrelextrema(x_array, np.less)

    #Finds all the local mins and maxes
    tv_maxes = x_array[argrelextrema(x_array, np.greater )]
    tv_mins = x_array[argrelextrema(x_array, np.less)]

    #print(tv_maxes)
    #print(tv_mins)

    #Finds the tidal volume by the difference between the local maxes and mins.
    tv_expected = tv_maxes - tv_mins
    #print(tv_expected)

    #plt.plot(tv_expected)
    #plt.show()
    return x_array, tv_expected



#TidalVolume("R-1-1.4-1.csv")
#TidalVolume("R-1-1.4-1.xls")

###################################
###################################

file = "R-3-3-1"
TidalVolume(file+".csv")

###################################
###################################



Fs = 240.0  # sampling rate
Ts = 1.0/Fs # sampling interval

k_ratio = 0.2485/0.269 #conversion because k value was not re-calculated when
#we ran the first sampling.


df = pd.read_excel(file +".xls")
length =len(df.index)

first_row = 16

points = length- first_row
d = []

t = []

for i in range(first_row,points):
    temp=df.iloc[i, 0]
    d_adjusted = (float(temp))*10 #multiple by 10 to convert to millimeters
    d.append(float(d_adjusted))

for i in range(first_row,points):
    temp=df.iloc[i, 2]
    t_adjusted = (float(temp))/Fs #Adjusts to same framerate
    t.append(t_adjusted)

dual_data = []
for i in range(0, len(d)):
    dual_data.append([d[i],t[i]])

x_array = np.array(d)


# for local maxima
#print("Look Here !")
#argrelextrema(x_array, np.greater, order=3)


# for local minima
#argrelextrema(x_array, np.less)

#Finds all the local mins and maxes
tv_maxes = x_array[argrelextrema(x_array, np.greater_equal, order =7)]
tv_mins = x_array[argrelextrema(x_array, np.less_equal, order = 5)]

"""
plt.plot(t,d,'r-', t_expected,x,'b-')
plt.show()
"""
#finding the local maximums of the samples
print(tv_maxes)
#finds the local minimums of the samples
print(tv_mins)


#Finds the tidal volume by the difference between the local maxes and mins.
#In a way that only runs for the number of variables for the minimal one
#This part takes the difference of the two 
if len(tv_maxes) < len(tv_mins):
    tv = []
    for i in range(0, len(tv_maxes)):
        tv.append(tv_maxes[i]-tv_mins[i])
    
elif len(tv_maxes) > len(tv_mins):
    tv = []
    for i in range(0, len(tv_mins)):
        tv.append(tv_maxes[i]-tv_mins[i])
        
else:
    tv = tv_maxes - tv_mins

print(tv)

mean_tv = sum(tv)/len(tv)
print(mean_tv)

#removes all correspondence that does not fall within this range,
#above half of mean value
tv = [i for i in tv if i > mean_tv/2] 



#Plots
plt.plot(tv_expected,'r-', label ='Expected Tidal Volume- Teensy')
plt.plot(tv,'b-', label = 'Actual Tidal Volume- Video Data')

#Axis Labels, Title, and Legend
plt.xlabel('Time')
plt.ylabel('Tidal Volume')
plt.title('Tidal Volume: Expected vs Actual '+ file)
plt.legend()

plt.savefig('TidalVolume-'+file+'.png', bbox_inches='tight')
plt.show()






