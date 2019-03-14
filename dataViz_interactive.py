# -*- coding: utf-8 -*-
"""
DataViz script for importing CSV data from Bilge Pump Runtime Test Stand

CSV File has format of 4 columns, corresponding to:
    Flow Rate, Current, Voltage, Temperature
Sample rate is once a second. Following script reads in CSV columns into a
pandas data frame, labeling the columns as required.
Then, the columns of the data frame are smoothed using a window size
equal to one half hour with rolling mean calculation. 
Data frame index is converted to a list of integers and stored in a list for parsing.

"""
"""
                                Test 7: 
        42.23-hour runtime started Friday 22 February 2019 at 12:22 PM and concluded
        Sunday 24 February 2019 at 6:26AM ; test was scheduled to continue until 25 Feb. at noon
        but due to mains power loss over weekend, control box reset.


"""


#import python package for plotting data
import matplotlib.pyplot as plt
#import pandas package for data framing
import pandas as pd

# prompt for new csv file name and generated plot titles
fileName    = input('Enter file name of CSV: ')
testNumber  = input('Enter test number: ')
testDate    = input('Enter test date: ') 

#import csv file as a pandas data frame
df = pd.read_csv(fileName)

#name columns of data frame after sensor data it represents
df.columns = ['Flow','Current','Voltage','Temperature']
#name index of data frame as Time in seconds
df.index.name = 'Time (seconds)'
#print data frame for label verification
#print(df)
#add column to data frame for power = voltage * current
df['Power'] = pd.Series(df.Current * df.Voltage, index = df.index)

#number of samples to window in data frame for line smoothing, here set to a window of 1800 seconds/half an hour 
window_size = 1800
#move smoothed data from data frame into series
smoothCurrent     = df.Current.rolling(window_size,min_periods=1).mean()
smoothVoltage     = df.Voltage.rolling(window_size,min_periods=1).mean()
smoothTemperature = df.Temperature.rolling(window_size,min_periods=1).mean()
smoothPower       = df.Power.rolling(window_size,min_periods=1).mean()
#convert data frame index to list of integers (for scaling from seconds to hours)
time_index        = df.index.tolist()

# make time_index 1-indexed and convert from seconds to hours
for n in range( len(time_index) ):
    time_index[n] += 1
for n in range( len(time_index) ):
        time_index[n] = n / 3600

#set up figure 'data' to readable image size 
data = plt.figure(figsize=(10,10))

ax1 = data.add_subplot(411)
plt.setp(ax1.get_xticklabels(), visible=False)
plt.plot(time_index,smoothCurrent)
plt.title('Bilge Pump Runtime Results, Test # %s : %s '  %(testNumber,testDate) )
plt.ylabel('Current (A)')
plt.grid(True)

ax2 = data.add_subplot(412, sharex=ax1)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.plot(time_index,smoothVoltage)
plt.ylabel('Voltage (V)')
plt.grid(True)

ax3 = data.add_subplot(413, sharex=ax1)
plt.plot(time_index,smoothPower)
plt.ylabel('Power (W)')
plt.grid(True)

ax4 = data.add_subplot(414, sharex=ax1)
plt.plot(time_index,smoothTemperature)
plt.ylabel('Temp. ($\degree$F)')
plt.xlabel('Time (hours)')
plt.grid(True)

#Max value display
print('Max Current occurs at time', df['Current'].idxmax(), 'and is', df['Current'].max() ,'A')
print('Average Current is', df['Current'].mean(), 'A')
print('Max Voltage occurs at time', df['Voltage'].idxmax(), 'and is', df['Voltage'].max() ,'V')
print('Average Voltage is', df['Voltage'].mean(), 'V')
print('Max Power occurs at time', df['Power'].idxmax(), 'and is', df['Power'].max() ,'W')
print('Average Power is', df['Power'].mean(), 'W')
print('Max Temperature occurs at time', df['Temperature'].idxmax(), 'and is', df['Temperature'].max() ,'degrees F')
print('Average Temperature is', df['Temperature'].mean(), 'degrees F')