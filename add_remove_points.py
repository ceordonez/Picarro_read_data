#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(16,4))
a_input = np.sin(range(100))*np.random.normal(20,10,100)
b_input = [ 5, 15, 25, 30, 40, 50, 75, 85]

a = plt.plot(range(len(a_input)),a_input,color='red')[0]
b = plt.scatter(b_input,a_input[b_input],color='grey',s=50,picker=5)

def add_or_remove_point(event):
    global a
    xydata_a = np.stack(a.get_data(),axis=1)
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
    new_xydata_point_b = xydata_a[new_xdata_point_b,:]

    if event.button == 1:
        if new_xdata_point_b not in xdata_b:
            #insert new scatter point into b
            new_xydata_b = np.insert(xydata_b,0,new_xydata_point_b,axis=0)
            #sort b based on x-axis values
            new_xydata_b = new_xydata_b[np.argsort(new_xydata_b[:,0])]
            #update b
            b.set_offsets(new_xydata_b)
            plt.draw()
    elif event.button == 3:
        if new_xdata_point_b in xdata_b:
            #remove xdata point b
            new_xydata_b = np.delete(xydata_b,np.where(xdata_b==new_xdata_point_b),axis=0)
            print(new_xdata_point_b)
            #update b
            b.set_offsets(new_xydata_b)
        plt.draw()

fig.canvas.mpl_connect('button_press_event',add_or_remove_point)
plt.show()
