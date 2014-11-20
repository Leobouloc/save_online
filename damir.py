# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 14:29:43 2014

@author: work
"""
import pandas as pd
import os

path = 'C:\\Users\\work\\Documents\\ETALAB_data\\damir'


annees = [str(x) for x in range(2010, 2015)]
mois = [str(x) for x in range(1,13)]

period = [an + moi.zfill(2) for an in annees for moi in mois]


def table_reformat(table):
    table.rem_mon = table.rem_mon.str.replace('.', '')
    table.rem_mon = table.rem_mon.str.replace(',', '.')
    table.rem_mon = table.rem_mon.apply(float)
    return table 

ventes_med = []
for date in period:
    file_name = 'N' + date +'.csv'
    try:
        file = os.path.join(path, file_name)
        test = pd.read_csv(file, sep = ';')
        test = table_reformat(test)
        ventes_med += [test[test['exe_spe']==50].rem_mon.sum()]
        print date
    except:
        print 'missed : ' +  file_name