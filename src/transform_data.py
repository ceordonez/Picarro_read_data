#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl

def transform_data(data1, data2):
    data1['Datetime'] = pd.to_datetime(data1['DATE'].astype(str) + ' ' + data1['TIME'].astype(str))
    data1 = data1.sort_values(by='Datetime')
    data2 = data2.sort_values(by='Datetime')
    data1['Julday'] = mpl.dates.date2num(data1.Datetime)
    data2['Julday'] = mpl.dates.date2num(data2.Datetime)
    return data1, data2
