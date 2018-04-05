import matplotlib.pyplot as plt
import numpy as np
import xlrd
import xlwt
import decimal as decimal
decimal.getcontext().prec = 6
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

#SELECT THE FIRST ROW OF DATA!
firstRow = 19


#TYPE NAME OF FILE!
workbook = xlrd.open_workbook('R-1-1.4-1.xls')
worksheet = workbook.sheet_by_index(0)
x = worksheet.nrows

Fs = 240.0  # sampling rate
Ts = 1.0/Fs # sampling interval
t = []
for i in range(firstRow,x):
     temp = str(worksheet.cell(i,2))
     t.append(int(temp[6:-1]))
     
y = []
for i in range(firstRow,x):
    temp = decimal.Decimal(str(worksheet.cell(i,0))[7:]);
    y.append(temp) #position

#Normalize so that it can run the analysis
avg = decimal.Decimal(np.mean(y))
y[:] = (i - avg for i in y)

n = len(y) # length of the signal
k = np.arange(n)
T = n/Fs
frq = k/T # two sides frequency range
frq = frq[range(n//2)] # one side frequency range

Y = np.fft.fft(y) # fft computing and normalization
Y = Y[range(n//2)]
n = len(y)
freq = np.fft.fftfreq(n,Ts)
print(np.mean(freq))
#favg = np.mean(frq)
#print(favg)
plt.plot(t,y)
plt.xlabel('Time')
plt.ylabel('Position')
plt.show()
plt.plot(frq,abs(Y),'r') # plotting the spectrum
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.show()

newBook = xlwt.Workbook()
newSheet = newBook.add_sheet('Analyzed_Data')
row = newSheet.row(0)
row.write(0,'Time')
row.write(1,'Tidal Volume')
row.write(2,'Statistics')
for i in range(1,len(t)):
    row = newSheet.row(i)
    row.write(0,t[i])
    row.write(1,y[i])


newBook.save('Analyzed.xls')

