# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 16:18:56 2015

@author: debian
"""
import os
import pandas as pd

path = '/home/debian/Documents/data/strasbourg'
file = os.path.join(path, 'table_des_mots_2.csv')

#table_des_mots_2 = pd.read_csv(file, sep = ';')
#table_des_mots_2.index = list(table_des_mots_2['Unnamed: 0'])
#table_des_mots_2.drop('Unnamed: 0', axis = 1, inplace = True)

def nettoyage(string):
    to_replace = [',', '.', ')', '(', '-', '"', "d'", '&', '+', '/', '«', '»', "l'", "'", '!']
    for s in to_replace:
        string = string.replace(s, '')
    to_replace = ['é', 'è']
    for s in to_replace:
        string = string.replace(s, 'e')
    if len(string) <= 2:
        return ''
        
    ### Plus specifique
    to_replace = ['lot', 'pour', 'des', 'les', 'sur', 'strasbourg', 'ville', 'cus', 'mise', 'stbg', 'dans']
    for s in to_replace:
        string = string.replace(s, '')
    if not string.isalpha():
        return ''
        
    return string

def singulier_de_liste(liste_de_strings):
    '''remplace les strings au pluriel par le singulier si le singulier est dans la liste'''
    liste_de_strings_copy = list(liste_de_strings)
    def _plur_1(x, liste_de_strings):
        if len(x) <= 4:
            return x
        elif x[-1] != 's':
            return x
        elif x[:-1] not in liste_de_strings:
            return x
        else:
            return x[:-1]
            
    def _plur_2(x, liste_de_strings):
        if len(x) <= 4:
            return x
        elif x[-3:] != 'aux':
            return x
        elif (x[:-3] + 'al') not in liste_de_strings:
            return x
        else:
            return x[:-3] + 'al'
            
    liste_de_strings = [_plur_1(x, liste_de_strings_copy) for x in liste_de_strings]
    return liste_de_strings
    

columns = total_tab.columns
columns = [nettoyage(x) for x in columns]
columns = singulier_de_liste(columns)
total_tab.columns = columns
total_tab.index = columns

for x in [0,1]:
    print "Un tour de nettoyage"
    total_tab = total_tab.T
    total_tab['temp_col'] = total_tab.index
    grp = total_tab.groupby('temp_col')
    total_tab = grp.sum()


total_tab.drop('', axis = 0, inplace = True)
total_tab.drop('', axis = 1, inplace = True)

a = total_tab.sum()
a.sort(ascending = False)

#a = a[2:]
a = a[a > 100]
total_tab = total_tab.loc[a.index, a.index]
total_tab.fillna(0)

b = a.apply(lambda x: float(math.sqrt(x)))
total_tab_norm = total_tab.apply(lambda x: x / b)
total_tab_norm = total_tab_norm.apply(lambda x: x / b, axis = 1)
distance_tab = total_tab_norm.applymap(lambda x: 1/x)

for i in distance_tab.index:
    distance_tab.loc[i, i] = inf
    
distance_tab = distance_tab.replace(inf, 4 * distance_tab[distance_tab != inf].max().max())

