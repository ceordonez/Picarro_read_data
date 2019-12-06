#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import SpanSelector, Button
from read_data import read_picarro, read_excel
from plot_data import make_plot
from config_file import *
from transform_data import transform_data

def main():

    DataP = read_picarro(path_picarro)
    DataC = read_excel(path_excel, excel_filename)

    dataP, dataC, x, y = transform_data(DataP, DataC)

    fig, ax, line2, tt = make_plot(x, y, dataC)

    def onselect(xmin, xmax):
        x2 = line2.get_xdata()
        y2 = line2.get_ydata()
        indmin2, indmax2 = np.searchsorted(x2, (xmin, xmax))
        indmax2 = min(len(x2) - 1, indmax2)
        thisx = x2[indmin2:indmax2]
        thisy = y2[indmin2:indmax2]
        line2.set_data(thisx, thisy)
        ax.set_xlim(xmin, xmax)
        if len(thisy) == 0:
            ax.set_ylim(0, 300)
            s = 'Avg = %.3f\nStd = %.3f' %(-9999.999,-9999.999)
        else:
            s = 'Avg = %.3f\nStd = %.3f' %(thisy.mean(),thisy.std())
            ax.set_ylim(0.9*thisy.min(), 1.1*thisy.max())
        tt.set_text(s)
        fig.canvas.draw()

    span2 = SpanSelector(ax, onselect, 'horizontal', useblit=True,
                         rectprops=dict(alpha=0.5, facecolor='red'),
                         minspan=15/86400.)

    class Index(object):

        def reset(self, event):
            ax.set_xlim(x.min(), x.max())
            ax.set_ylim(0,300)
            line2.set_data(x,y)
            plt.draw()

    callback = Index()
    axres = plt.axes([0.81, 0.05, 0.1, 0.075])
    bnres = Button(axres, 'Reset Plot')
    bnres.on_clicked(callback.reset)
    plt.show()

if __name__ == '__main__':
    main()
