#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl

def transform_data(data1, data2):
    data1['Datetime'] = pd.to_datetime(data1['DATE'].astype(str) + ' ' + data1['TIME'].astype(str))
    data1 = data1.sort_values(by='Datetime')
    data2 = data2.sort_values(by='Datetime')
    x = mpl.dates.date2num(data1.Datetime)
    y = data1.HR_12CH4_dry
    return data1, data2, x, y
