# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 14:50:34 2015

@author: leo_cdo_intern

##############################################################################
Aggrégation des données criminologie :
https://www.data.gouv.fr/fr/datasets/les-crimes-et-delits-enregistres-par-la-gendarmerie-nationale/
https://www.data.gouv.fr/fr/datasets/crimes-et-delits-constates-par-la-police-nationale-en-2013/

Utilisation : modifiez le "path" ci dessous pour qu'ils correspondent à l'emplacement
de stockage des fichiers de la gendarmerie ci dessous. Modifiez les noms (file_name...)
si vous avez renommé ces fichiers.

Le nouveau fichier portera le nom indiqué dans la variable : new_file_name
"""

import pandas as pd
from os.path import join, dirname
import numpy as np


def load_crimes_fr(to_load, path, file_name_police, file_name_gendarmerie, new_file_name):
    '''Creates csv from the two tables, adds department ID'''
    big_tab = pd.DataFrame()
    for loading in to_load:
        
        print '\nChargement de la table', loading
        if loading == 'police':
            file_name = file_name_police
        elif loading == 'gendarmerie':
            file_name = file_name_gendarmerie
        else:
            print 'Ce load n est pas accepte. Il doit être police ou gendarmerie'
            
        table = pd.DataFrame()
        for i in range(12):
            try:
                print 'Chargement de la page', i
                test = pd.read_excel(join(path, file_name), i)
                test.columns = ['dat', 'infract', 'designation'] + list(test.columns[3:])
                toast = pd.melt(test, id_vars = list(test.columns[:3]), value_vars = list(test.columns[3:]))
                toast.columns = [u'dat', u'infract', u'designation', u'departement', u'nombre']
                toast[toast.nombre == '.'] = np.nan
                if len(test) == 0:
                    print '   >>>  empty'
                table =  table.append(toast, ignore_index = True)
            except:
                print '  >>  Erreur dans le chargement de la page', i
                pass
        table['source'] = loading
        big_tab = big_tab.append(table,ignore_index = True)
    big_tab = big_tab[big_tab.designation.notnull()]
    columns = [u'dat', u'infract', u'designation', u'departement', u'source', u'nombre'] 
    big_tab = big_tab[columns]
    big_tab.to_csv(join(path, new_file_name), index = False)
    print 'Le nouveau csv a été créé'
    return big_tab

if __name__ == '__main__':
    to_load = ['police', 'gendarmerie']
    path = '/home/debian/Documents/data/criminologie'
    file_name_police = '2013-fc-pn.xls'
    file_name_gendarmerie = '2013-fc-gn.xlsx'
    new_file_name = '2013-crimes-et-delits.csv'
    table = load_crimes_fr(to_load, path, file_name_police, file_name_gendarmerie, new_file_name)
