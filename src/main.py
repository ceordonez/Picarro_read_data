#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from read_data import read_picarro, read_excel
from plot_data import make_plot, span_plot
from config_file import *
from transform_data import transform_data

def main():

    DataP = read_picarro(path_picarro)

    DataC = read_excel(path_excel, excel_filename)

    dataP, dataC = transform_data(DataP, DataC)

    fig, axs, lines, tts = make_plot(dataP, dataC)

    span_plot(fig, axs, lines, tts, dataP)


if __name__ == '__main__':
    main()
