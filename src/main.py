#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pdb
import os
import pandas as pd
from read_data import read_picarro, read_excel

mpl.use('tkAgg')

path_picarro = r'/home/cesar/Dropbox/Cesar/PhD/Data/Fieldwork/MultiLakeSurvey/Lakes/Bretaye/Data/Picarro'
path_excel = '/home/cesar/Dropbox/Cesar/PhD/Data/Fieldwork/MultiLakeSurvey/Lakes/Bretaye/Data/CH4-CO2'
dataP = read_picarro(path_picarro)
dataC = read_excel(path_excel, 'CH4-CO2-dC_Calculations_Bretaye_20190720_1.xlsx')
dataP['Datetime'] = pd.to_datetime(dataP['DATE'].astype(str) + ' ' + dataP['TIME'].astype(str))
dataP = dataP.sort_values(by='Datetime')
dataC = dataC.sort_values(by='Datetime')
x = mpl.dates.date2num(dataP.Datetime)
y = dataP.HR_12CH4_dry
fig, (ax1, ax2) = plt.subplots(2,1)
line1, = ax1.plot(x, y)
b = ax1.scatter(mpl.dates.date2num(dataC.Datetime), dataC.CH4_ppm, picker=4, color='grey')
ax1.set_ylim([0,300])
#points = np.array([])
line2, = ax2.plot(mpl.dates.date2num(dataP.Datetime), dataP.HR_12CH4_dry)
b = ax2.scatter(mpl.dates.date2num(dataC.Datetime), dataC.CH4_ppm, picker=4, color='grey')
ax2.set_ylim([0,300])
tt = ax2.text(0.8,0.8,'', transform = ax2.transAxes)
def add_or_remove_point(event):
    global a
    xydata_a = np.stack(a.get_data(), axis=1)
    xdata_a = a.get_xdata()
    ydata_a = a.get_ydata()
    global b
    xydata_b = b.get_offsets()
    xdata_b = b.get_offsets()[:,0]
    ydata_b = b.get_offsets()[:,1]

    #click x-value
    xdata_click = event.xdata
    #index of nearest x-value in a
    xdata_nearest_index_a = (np.abs(xdata_a-xdata_click)).argmin()
    #new scatter point x-value
    new_xdata_point_b = xdata_a[xdata_nearest_index_a]
    #new scatter point [x-value, y-value]
    new_xydata_point_b = xydata_a[xdata_nearest_index_a,:]

    if event.button == 1:
        if new_xdata_point_b not in xdata_b:
            i = 0
            #insert new scatter point into b
            new_xydata_b = np.insert(xydata_b, 0, new_xydata_point_b, axis=0)
            #sort b based on x-axis values
            new_xydata_b = new_xydata_b[np.argsort(new_xydata_b[:,0])]
            #update b
            b.set_offsets(new_xydata_b)

    elif event.button == 3:
        if new_xdata_point_b in xdata_b:
            #remove xdata point b
            new_xydata_b = np.delete(xydata_b,np.where(xdata_b==new_xdata_point_b),axis=0)
            #print(new_xdata_point_b)
            #update b
            b.set_offsets(new_xydata_b)
        plt.draw()

def onselect1(xmin, xmax):
    indmin, indmax = np.searchsorted(x, (xmin, xmax))
    indmax = min(len(x) - 1, indmax)

    thisx = x[indmin:indmax]
    thisy = y[indmin:indmax]
    line2.set_data(thisx, thisy)
    ax2.set_xlim(thisx[0], thisx[-1])
    ax2.set_ylim(0.9*thisy.min(), 1.1*thisy.max())
    fig.canvas.draw()

def onselect2(xmin, xmax):
    x2 = line2.get_xdata()
    y2 = line2.get_ydata()
    indmin2, indmax2 = np.searchsorted(x2, (xmin, xmax))
    indmax2 = min(len(x2) - 1, indmax2)
    thisx2 = x2[indmin2:indmax2]
    thisy2 = y2[indmin2:indmax2]
    s = 'Avg = %.3f\nStd = %.3f' %(thisy2.mean(),thisy2.std())
    #print s
    tt.set_text(s)
    line2.set_data(thisx2, thisy2)
    ax2.set_xlim(thisx2[0], thisx2[-1])
    ax2.set_ylim(0.9*thisy2.min(), 1.1*thisy2.max())
    fig.canvas.draw()

from matplotlib.widgets import SpanSelector
span1 = SpanSelector(ax1, onselect1, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'),
                    button=1)
span2 = SpanSelector(ax2, onselect2, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'),
                    button=1)

# Set useblit=True on most backends for enhanced performance.

plt.show()

#fig.canvas.mpl_connect('button_press_event', add_or_remove_point)
#plt.show()
