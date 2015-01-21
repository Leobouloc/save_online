# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 15:44:35 2015

@author: leo_cdo_intern

#####################################################################################################
Ce fichier contient : 
    - Un script de réduction de table, en supprimant les colonnes pouvant être déduites d'autres colonnes,
        qui génère par ailleurs des prédicteurs capables de reconstituer la base initiale
    - Un script qui permet de sauvegarder les prédicteurs ainsi créés (TODO)
    - Un script permettant de reconstruire la base initiale, ou seullement certaines variables (ou seulement... : TODO)
#####################################################################################################
"""

from DAMIR_CONFIG import nettoyage_fichier_R_1_path as path
from os.path import join
import pandas as pd
from itertools import combinations

#table = pd.read_csv(join(path, 'reduced_R201411.CSV'), sep = ';')



columns_to_analyse = [col for col in table.columns if not(col in ['Unnamed: 0', 'rem_mon', 'rec_mon', 'dep_mon', 'act_dnb', 'act_coe'])]

# TODO : Créer une nouvelle fonction pour les implications
# TODO : enlever tous les apply : all(smaller_table.groupby(list_of_columns)[variable_to_predict].nunique() == 1)
def check_all_implications(table, list_of_columns): 
    '''Checks if variable_to_predict is predicted by list_of_columns'''
    implicates = [x for x in list(table.columns) if (not x in list_of_columns)]
    for x in [0.00005, 0.0002, 0.001, 0.01, 0.1, 1]:
        print 'currently testing with ratio : ', x
        smaller_table = table[implicates + list_of_columns].iloc[:int(len(table) * x)]
        implicates = smaller_table.groupby(list_of_columns).apply(lambda x: x[implicates].apply(lambda y: y.nunique() == 1)).apply(all)
        implicates = list(implicates.index[implicates])        
        if len(implicates) == 0:
            return []
    return implicates
   

def get_all_predictions(table, list_of_columns, implications):
    return table[list_of_columns + implications].groupby(list_of_columns, as_index = False).apply(lambda x: x.iloc[0])


def recreate_original_table(new_table, list_of_predictors):
    '''Recreate full table with list'''
    for i in [len(list_of_predictors) - x - 1 for x in range(len(list_of_predictors))]:
        prediction = list_of_predictions[i]        
        print 'Adding :', [x for x in prediction['table'].columns if not(x in prediction['predictors'])], 'predicted by', prediction['predictors']
        new_table = new_table.merge(prediction['table'], on = prediction['predictors'], how = 'left')
    return new_table



print 'Reformating table for exploration ...'
new_table = table.copy()
nunique_by_col = new_table[columns_to_analyse].apply(lambda x: x.nunique())
nunique_by_col.sort(ascending = False)
columns = [x for x in new_table.columns if not(x in columns_to_analyse)] + list(nunique_by_col.index)
new_table = new_table[columns]


ind = list(new_table.index)
shuffle(ind)
new_table = new_table.loc[ind]
list_of_predictions = []

for nb_predictors in range(1,5):
    print '\nCurrently testing', nb_predictors, 'predictors'
    for list_of_columns in combinations([x for x in columns_to_analyse if x in new_table.columns], nb_predictors):
        if all([x in new_table.columns for x in list_of_columns]):
            print 'currently checking implications of', list_of_columns
            all_implications = check_all_implications(new_table, list(list_of_columns))
            if len(all_implications) != 0:
                print list_of_columns, '    >>> predicts', all_implications
                prediction = dict()
                prediction['predictors'] = list_of_columns
                prediction['table'] = get_all_predictions(table, list(list_of_columns), all_implications)
                list_of_predictions += [prediction]
                new_table.drop(all_implications, axis = 1, inplace = True)

        
#def check_implication(table, list_of_columns, variable_to_predict): 
#    '''Checks if variable_to_predict is predicted by list_of_columns'''
#    for x in [0.0002, 0.001, 0.01, 0.1, 1]:
##        print 'currently testing with ratio : ', x
#        smaller_table = table.iloc[:int(len(table) * x)]
#        implicates = all(smaller_table.groupby(list_of_columns)[variable_to_predict].nunique() == 1)
#        if not implicates:
#            return False
#    return True

#def get_prediction(table, list_of_columns, variable_to_predict):
#    return table[list_of_columns + [variable_to_predict]].groupby(list_of_columns, as_index = False).apply(lambda x: x.iloc[0])