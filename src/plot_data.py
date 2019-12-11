#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib as mpl
import pdb
import numpy as np

from matplotlib.widgets import SpanSelector, Button, RadioButtons, MultiCursor
from pandas.plotting import register_matplotlib_converters
from config_file import lim_plot_var
register_matplotlib_converters()
mpl.use('tkAgg')

def make_plot(dataP, dataC):
    varplot = ('HRCH4_d', 'HRdCH4', 'CO2_d', 'dCO2')  # ['HPCH4_d', 'HPdCH4']
    fig, axs = plt.subplots(4, 1, figsize=(12,15), sharex=True)
    x1 = dataP['Julday']
    x2 = dataC['Julday']
    tts = []
    lines = []
    for i in range(len(axs)):
        if len(dataC) > 0:
            if 'CH4_d' in varplot[i]:
                sc = axs[i].scatter(x2, dataC.CH4_ppm, picker=4, color='r')
            elif 'CO2_d' in varplot[i]:
                sc = axs[i].scatter(x2, dataC.CO2_ppm, picker=4, color='r')
            elif 'dCH4' in varplot[i]:
                sc = axs[i].scatter(x2, dataC.dCH4, picker=4, color='r')
            elif 'dCO2' in varplot[i]:
                sc = axs[i].scatter(x2, dataC.dCO2, picker=4, color='r')
        lines.append(axs[i].plot(x1, dataP[varplot[i]])[0])
        axs[i].set_ylim(lim_plot_var[i])
        s = 'Avg = %.3f\nStd = %.3f' %(dataP[varplot[i]].mean(),dataP[varplot[i]].std())
        tts.append(axs[i].text(-.25, 0.8, s, transform = axs[i].transAxes))
    plt.subplots_adjust(top = .85, left=0.2)
    axs[0].set_ylabel('CH4 (ppm)')
    axs[1].set_ylabel(u'dCH4 (\u2030)')
    axs[2].set_ylabel('CO2 (ppm)')
    axs[3].set_ylabel(u'dCO2 (\u2030)')
    datemin = mpl.dates.num2date(x1.iloc[0])
    datemax = mpl.dates.num2date(x1.iloc[-1])
    axs[-1].set_xlim(datemin, datemax)

    return fig, axs, lines, tts

def span_plot(fig, axs, lines, tts, dataP):

    xs = []
    ys = []
    for i in range(len(axs)):
        xs.append(lines[i].get_xdata())
        ys.append(lines[i].get_ydata())

    axcolor = 'lightgoldenrodyellow'
    rax = plt.axes([0.20, 0.87, 0.10, 0.05], facecolor=axcolor)
    radio = RadioButtons(rax, ('HR_CH4_d', 'HP_CH4_d'))
    rax2 = plt.axes([0.35, 0.87, 0.10, 0.05], facecolor=axcolor)
    radio2 = RadioButtons(rax2, ('HR_dCH4', 'HP_dCH4'))

    def CH4func(label):
        xb = lines[0].get_xdata()
        dataPs = dataP.set_index('Julday')
        hzdict = {'HP_CH4_d': dataPs.HPCH4_d.loc[xb].values,
                  'HR_CH4_d': dataPs.HRCH4_d.loc[xb].values}
        ydata = hzdict[label]
        lines[0].set_ydata(ydata)
        plt.draw()

    def dCH4func(label):
        xb = lines[1].get_xdata()
        dataPs = dataP.set_index('Julday')
        hzdict = {'HP_dCH4': dataPs.HPdCH4.loc[xb].values,
                  'HR_dCH4': dataPs.HRdCH4.loc[xb].values}
        ydata = hzdict[label]
        lines[1].set_ydata(ydata)
        plt.draw()

    radio.on_clicked(CH4func)
    radio2.on_clicked(dCH4func)

    def fun_select(x2, y2, indmax, indmin):
        indmax = min(len(x2) - 1, indmax)
        thisx = x2[indmin:indmax]
        thisy = y2[indmin:indmax]
        if len(thisy) == 0:
            s = 'Avg = %.3f\nStd = %.3f' %(-9999.999,-9999.999)
        else:
            s = 'Avg = %.3f\nStd = %.3f' %(thisy.mean(),thisy.std())
        return thisx, thisy, s

    history = {'ax0': [], 'ax1': [], 'ax2': [], 'ax3': []}
    key_ax = list(history.keys())

    def onselect(xmin, xmax):
        i = 0
        x2 = lines[i].get_xdata()
        y2 = lines[i].get_ydata()
        indmin, indmax = np.searchsorted(x2, (xmin, xmax))
        indmax = min(len(x2) - 1, indmax)
        for j in range(len(axs)):
            xx = lines[j].get_xdata()
            yy = lines[j].get_ydata()
            thisx, thisy, s = fun_select(xx, yy, indmax, indmin)
            if len(thisx) > 0:
                history[key_ax[j]].append([thisx, thisy, s])
                lines[j].set_data(thisx, thisy)
                miny = np.nanmin(thisy)
                maxy = np.nanmax(thisy)
                miny = np.nanmax([miny, lim_plot_var[j][0]])
                maxy = np.nanmin([maxy, lim_plot_var[j][1]])
                if miny > 0:
                    axs[j].set_ylim(.9*miny,1.1*maxy)
                else:
                    axs[j].set_ylim(1.1*miny,.9*maxy)
                tts[j].set_text(s)
        if len(thisx) > 0:
            axs[i].set_xlim(xmin, xmax)
            fig.canvas.draw()

    def regselect(xmin, xmax):
        i = 0
        x2 = lines[i].get_xdata()
        y2 = lines[i].get_ydata()
        indmin, indmax = np.searchsorted(x2, (xmin, xmax))
        for j in range(len(axs)):
            xx = lines[j].get_xdata()
            yy = lines[j].get_ydata()
            if len(xx) > 0:
                thisx, thisy, s = fun_select(xx, yy, indmax, indmin)
                tts[j].set_text(s)
        fig.canvas.draw()

    span1 = []
    span2 = []
    for i in range(len(axs)):
        span1.append(SpanSelector(axs[i], onselect, 'horizontal', useblit=True,
                                rectprops=dict(alpha=0.5, facecolor='red'),
                                minspan=15/86400., button=1))
        span2.append(SpanSelector(axs[i], regselect, 'horizontal', useblit=True,
                                rectprops=dict(alpha=0.5, facecolor='green'),
                                minspan=15/86400., button=2, span_stays = True))
    class Index(object):
        def back(self, event):
            if len(history[key_ax[0]]) > 1:
                for i in range(len(axs)):
                    del  history[key_ax[i]][-1]
                    xss = history[key_ax[i]][-1][0]
                    yss = history[key_ax[i]][-1][1]
                    ss = history[key_ax[i]][-1][2]
                    lines[i].set_data(xss, yss)
                    tts[i].set_text(ss)
                    miny = np.nanmin(yss)
                    maxy = np.nanmax(yss)
                    miny = np.nanmax([miny, lim_plot_var[i][0]])
                    maxy = np.nanmin([maxy, lim_plot_var[i][1]])
                    if miny > 0:
                        axs[i].set_ylim(.9*miny,1.1*maxy)
                    else:
                        axs[i].set_ylim(1.1*miny,.9*maxy)
                axs[-1].set_xlim(xss.min(), xss.max())
                plt.draw()
            else:
                for i in range(len(axs)):
                    axs[i].set_ylim(lim_plot_var[i])
                    lines[i].set_data(xs[i],ys[i])
                    s = 'Avg = %.3f\nStd = %.3f' %(np.nanmean(ys[i]), np.nanstd(ys[i]))
                    tts[i].set_text(s)
                axs[-1].set_xlim(xs[-1].min(), xs[-1].max())
                plt.draw()

        def reset(self, event):
            for i in range(len(axs)):
                axs[i].set_ylim(lim_plot_var[i])
                lines[i].set_data(xs[i], ys[i])
                s = 'Avg = %.3f\nStd = %.3f' %(np.nanmean(ys[i]), np.nanstd(ys[i]))
                history[key_ax[i]].append([xs[i], ys[i], s])
                tts[i].set_text(s)
            axs[-1].set_xlim(xs[-1].min(), xs[-1].max())
            plt.draw()

    callback = Index()
    axres = plt.axes([0.50, 0.87, 0.1, 0.05])
    axbac = plt.axes([0.60, 0.87, 0.1, 0.05])
    bnres = Button(axres, 'Reset Plot')
    bnbac = Button(axbac, 'Back')
    bnres.on_clicked(callback.reset)
    bnbac.on_clicked(callback.back)
    plt.show()
