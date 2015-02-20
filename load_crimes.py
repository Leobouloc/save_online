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

deps = {
 u'Ain' : '01',
 u'Aisne' : '02',
 u'Allier' : '03',
 u'Alpes-Maritimes' : '06',
 u'Alpes-de-Haute-Provence' : '04',
 u'Ardennes' : '08',
 u'Ard\xe8che' : '07',
 u'Ari\xe8ge' : '09',
 u'Aube' : '11',
 u'Aude' : '11',
 u'Aveyron' : '12',
 u'Bas-Rhin' : '67',
 u'Bouches-du-Rh\xf4ne' : '13',
 u'CJ' : 'CJ',
 u'Calvados' : '14',
 u'Cantal' : '15',
 u'Charente' : '16',
 u'Charente-Maritime' : '17',
 u'Cher' : '18',
 u'Corr\xe8ze' : '19',
 u'Corse du Sud' : '2A',
 u'Creuse' : '23',
 u'C\xf4te-d\u2019Or' : '21',
 u"C\xf4tes-d'Armor" : '22',
 u'Deux-S\xe8vres' : '79',
 u'Dordogne' : '24',
 u'Doubs' : '25',
 u'Dr\xf4me' : '26',
 u'Essonne' : '91',
 u'Eure' : '27',
 u'Eure-et-Loir' : '28',
 u'Finist\xe8re' : '29',
 u'Gard' : '30',
 u'Gers' : '32',
 u'Gironde' : '33',
 u'Guadeloupe' : '971',
 u'Guyane' : '973',
 u'Haut-Rhin' : '68',
 u'Haute Corse' : '2B',
 u'Haute-Garonne' : '31',
 u'Haute-Loire' : '43',
 u'Haute-Marne' : '52',
 u'Haute-Savoie' : '74',
 u'Haute-Sa\xf4ne' : '70',
 u'Haute-Vienne' : '87',
 u'Hautes-Alpes' : '05',
 u'Hautes-Pyr\xe9n\xe9es' : '65',
 u'Hauts-de-Seine' : '92',
 u'H\xe9rault' : '34',
 u'Ille-et-Vilaine' : '35',
 u'Indre' : '36',
 u'Indre-et-Loire' : '37',
 u'Is\xe8re' : '38',
 u'Jura' : '39',
 u'Landes' : '40',
 u'Loir-et-Cher' : '41',
 u'Loire' : '42',
 u'Loire-Atlantique' : '44',
 u'Loiret' : '45',
 u'Lot' : '46',
 u'Lot-et-Garonne' : '47',
 u'Loz\xe8re' : '48',
 u'Maine-et-Loire' : '49',
 u'Manche' : '50',
 u'Marne' : '51',
 u'Martinique' : '972',
 u'Mayenne' : '53',
 u'Mayotte' : '976',
 u'Meurthe-et-Moselle' : '54',
 u'Meuse' : '55',
 u'Morbihan' : '56',
 u'Moselle' : '57',
 u'Ni\xe8vre' : '58',
 u'Nord' : '59',
 u'Nouvelle Cal\xe9donie' : 'NC',
 u'Oise' : '60',
 u'Orne' : '61',
 u'Paris' : '75',
 u'Pas-de-Calais' : '62',
 u'Polyn\xe9sie Fran\xe7aise' : 'PF',
 u'Puy-de-D\xf4me' : '63',
 u'Pyr\xe9n\xe9es-Atlantiques' : '64',
 u'Pyr\xe9n\xe9es-Orientales' : '66',
 u'Rh\xf4ne' : '69',
 u'R\xe9union' : '974',
 u'Saint Pierre et Miquelon' : 'SPM',
 u'Sarthe' : '72',
 u'Savoie' : '73',
 u'Sa\xf4ne-et-Loire' : '71',
 u'Seine-Maritime' : '76',
 u'Seine-St-Denis' : '93',
 u'Seine-et-Marne' : '77',
 u'Somme' : '80',
 u'Tarn' : '81',
 u'Tarn-et-Garonne' : '82',
 u'Territoire-de-Belfort' : '90',
 u'Val-de-Marne' : '94',
 u'Val-d\u2019Oise' : '',
 u'Var' : '83',
 u'Vaucluse' : '84',
 u'Vend\xe9e' : '85',
 u'Vienne' : '86',
 u'Vosges' : '88',
 u'Wallis et Futuna' : '95',
 u'Yonne' : '89',
 u'Yvelines' : '78',
 u'9G' : '9G',
 u'9H' : '9H',
 u'AC' : 'AC',
 u'AE' : 'AE',
 u'AT' : 'AT'
}


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
    columns = [u'dat', u'infract', u'designation', u'departement', 'code_dep', u'source', u'nombre']
    big_tab['code_dep'] = big_tab.departement.apply(lambda x: deps[x])
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
