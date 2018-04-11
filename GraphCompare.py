#Code by Matt Lubas, Eric Wirth, and Alfred Rwagaju on finding tidal volume for
#both expected values from Arduino and actual values from Kinovea.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

PA = 452.25 / 1000
#mm^2 is piston area of pneumatic actuator. Divides by 1000 to convert mm^3 to
#milliliters (mL)

def TidalVolume(file):
    """Name csv or xls file to take the data, find local maximums and minimums
    using numpy and argrelextrema. Reports a list of tidal volumes between
    local minimums and maximums. Plots this as well. """

    #k_ratio = 0.2485/0.269  #conversion because k value was not re-calculated when
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

    #Globals used here because of sloppy half functions/ half not code.
    global tv_expected
    global x 
    global t_expected
    
    x= [] #create list of x in order to use floats instead of strings.
    for item in d:


        #if error around Tidal Volume comes up when commented out- use this
        #statement, or vice versa.
        if item[:5] == "Tidal":
            item = 0

        temp = float(item) #*k_ratio
        x.append(float(temp))

    #Code that is not used here , but may need to be to correspond the two
    # graphs
    x_mean = sum(x)/ len(x)
    #print(x_mean)
    x_mode = max(set(x), key=x.count)


    #Turns Tidal Volume from a distance measure to a Volume
    
    
    #turns the list into a numpy array for finding max and mins
    x_array = np.array(x)

    x_Volume = x_array * PA


    #Finds all the local mins and maxes
    tv_maxes = x_Volume[argrelextrema(x_Volume, np.greater )]
    tv_mins = x_Volume[argrelextrema(x_Volume, np.less)]


    if len(tv_maxes) < len(tv_mins):
        tv_expected = []
        for i in range(0, len(tv_maxes)):
            tv_expected.append(tv_maxes[i]-tv_mins[i])
    
    elif len(tv_maxes) > len(tv_mins):
        tv_expected = []
        for i in range(0, len(tv_mins)):
            tv_expected.append(tv_maxes[i]-tv_mins[i])

    else:
        tv_expected = tv_maxes - tv_mins
        
    #print(tv_maxes)
    #print(tv_mins)

    #Finds the tidal volume by the difference between the local maxes and mins.
    tv_expected = tv_maxes - tv_mins
    print(tv_expected)


    #plt.plot(tv_expected)
    #plt.show()
    return x_array, tv_expected


def Plotting(tv_expected, tv_actual, mean_tv, file):
    """Creates and saves a beautiful plot of tidal volume based on expected and
    actual tidal volume"""
    
    #Plots
    plt.plot(tv_expected,'r-', label ='Expected Tidal Volume- Teensy')
    plt.plot(tv,'b-', label = 'Actual Tidal Volume from Video Data. Median = %.02f mL' % (mean_tv))

    #Axis Labels, Title, and Legend
    plt.xlabel('Number of Breaths')
    plt.ylabel('Tidal Volume (mL)')
    plt.title('Tidal Volume: Expected vs Actual '+ file)
    plt.ylim((1, 2)) #may take out for bigger graphs
    plt.legend()

    plt.savefig(OutputFolder+'TidalVolume-'+file+'.png', bbox_inches='tight')
    plt.show()

#TidalVolume("R-1-1.4-1.csv")
#TidalVolume("R-1-1.4-1.xls")

###################################
###################################

workbook_old = "TidalVolumeRuns/"
workbook = "Validation2/"
file = "B-1.8-2.2-1"

TidalVolume(workbook+file+".csv")
#TidalVolume(workbook_old+file+".csv")

OutputFolder ="Validation2/TidalVolumeGraphs/"

###################################
###################################



Fs = 240.0  # sampling rate
Ts = 1.0/Fs # sampling interval

k_ratio = 0.269/.2485 #conversion because k value was not re-calculated when
#we ran the first sampling.

#df = pd.read_excel(workbook+file +".xls")
df = pd.read_excel(workbook_old+file +".xls")

length =len(df.index)

#position where Kinovea values start
first_row = 16

points = length- first_row
#two lists for time and distance.... may remove, but could be useful for
# a side by side comparison of actual values.
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

#turning the normal list into a numpy array

x_array = np.array(d)

x_Volume = PA * x_array

x_Volume = k_ratio**2 *x_Volume

#Finds all the local mins and maxes
tv_maxes = x_Volume[argrelextrema(x_Volume, np.greater_equal, order =7)]
tv_mins = x_Volume[argrelextrema(x_Volume, np.less_equal, order = 7)]


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


median_tv = np.median(tv)
print(median_tv)

#removes all correspondence that does not fall within this range,
#above half of mean value
if median_tv < 0.1:
    tv = [i for i in tv if i > median_tv/2]
    median_tv = np.median(tv)
    
tv = [i for i in tv if i > median_tv/2]


median_tv = np.median(tv)
print(median_tv)





Plotting(tv_expected,tv,median_tv, file)
#Plotting(tv_expected,tv_expected,tv_expected,file)

#Plotting(tv,tv,median_tv, file)





