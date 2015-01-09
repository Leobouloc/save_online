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

a = total_tab.sum()
a.sort(ascending = False)
    
### TOMORROW : RUN BELOW >>>>>


    
#table_des_mots.to_csv('table_des_mots_2_clean.csv', sep = ';')



#table_des_mots_2 = a.copy()
