#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

def onselect1(x, y, line2, xmin, xmax, ax2, fig):
    indmin, indmax = np.searchsorted(x, (xmin, xmax))
    indmax = min(len(x) - 1, indmax)

    thisx = x[indmin:indmax]
    thisy = y[indmin:indmax]
    line2.set_data(thisx, thisy)
    ax2.set_xlim(thisx[0], thisx[-1])
    ax2.set_ylim(0.9*thisy.min(), 1.1*thisy.max())
    fig.canvas.draw()

def onselect2(line2, xmin, xmax, fig, tt, ax2):
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
