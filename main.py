#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.read_data import read_picarro, read_excel
from src.plot_data import make_plot, span_plot
from src.transform_data import transform_data

from config_file import *

def main():

    DataP = read_picarro(path_picarro)

    DataC = read_excel(path_excel, excel_filename)

    dataP, dataC = transform_data(DataP, DataC)

    fig, axs, lines, tts = make_plot(dataP, dataC)

    span_plot(fig, axs, lines, tts, dataP)


if __name__ == '__main__':
    main()
