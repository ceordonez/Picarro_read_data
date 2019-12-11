#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import pdb
import logging
import os
from config_file import dilution

def read_picarro(path, first=True):
    for filename in os.listdir(path):
        if filename[-3:] == 'dat':
            filename = os.path.join(path, filename)
            data = pd.read_csv(filename, sep='\s+',
                               usecols = ['DATE', 'TIME', 'HR_12CH4_dry',
                                          'HP_12CH4_dry', 'HR_Delta_iCH4_Raw',
                                          'HP_Delta_iCH4_Raw', '12CO2_dry',
                                          'Delta_Raw_iCO2'])
            data.columns = ['DATE', 'TIME', 'HPCH4_d', 'HPdCH4',
                            'HRCH4_d', 'HRdCH4', 'CO2_d', 'dCO2']
            if first:
                alldata = data
                first = False
            else:
                alldata = alldata.append(data, sort=False, ignore_index=True)
    return alldata.reset_index(drop=True)

def read_excel(path, filename):
    filename = os.path.join(path, filename)

    if dilution:
        data = pd.read_excel(filename, sheet_name='Dilutions',
                            skiprows= [0, 1, 2],
                            usecols = [1, 16, 18, 20, 22],
                            names = ['Datetime', 'CH4_ppm', 'dCH4',
                                    'CO2_ppm', 'dCO2'],
                            parse_dates = [0], infer_datetime_format=True)
    else:
        data = pd.read_excel(filename, sheet_name='CH4-CO2 Bottle Method',
                            skiprows= [0, 1, 2, 4],
                            usecols = [1, 14, 16, 18, 20],
                            names = ['Datetime', 'CH4_ppm', 'dCH4',
                                    'CO2_ppm', 'dCO2'],
                            parse_dates = [0], infer_datetime_format=True)

    return data
