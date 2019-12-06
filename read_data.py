#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import os


def read_picarro(path, first=True):
    for filename in os.listdir(path):
        if filename[-3:] == 'dat':
            print('Reading:', filename)
            filename = os.path.join(path, filename)
            data = pd.read_csv(filename, sep='\s+',
                            usecols=['DATE', 'TIME', 'HR_12CH4_dry',
                                    'HR_Delta_iCH4_Raw', '12CO2_dry',
                                    'Delta_Raw_iCO2'])
                            #parse_dates=[0, 1], infer_datetime_format=True)
            if first:
                alldata = data
                first = False
            else:
                alldata = alldata.append(data, sort=False, ignore_index=True)
#    alldata = alldata.sort_values(by='TIME')
    return alldata.reset_index(drop=True)

def read_excel(path, filename):
    filename = os.path.join(path, filename)
    data = pd.read_excel(filename, sheet_name='CH4-CO2 Bottle Method', skiprows=[0,1,2,4],
                         usecols = [1, 14, 18], names = ['Datetime', 'CH4_ppm', 'CO2_ppm'],
                         parse_dates = [0], infer_datetime_format=True)
#                         usecols=['Measuring Date\n + Time', ])
    return data
