#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
mpl.use('tkAgg')

def make_plot(x, y, dataC):
    fig, ax = plt.subplots(1, figsize=(10,8))
    line, = ax.plot(x, y)
    sc = ax.scatter(mpl.dates.date2num(dataC.Datetime), dataC.CH4_ppm, picker=4, color='grey')
    ax.set_ylim([0,300])
    tt = ax.text(0.8,0.8,'', transform = ax.transAxes)
    plt.subplots_adjust(bottom=0.2)
    datemin = mpl.dates.num2date(x[0])
    datemax = mpl.dates.num2date(x[-1])
    ax.set_xlim(datemin, datemax)
    return fig, ax, line, tt
