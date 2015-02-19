# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 14:47:57 2014

@author: leo_cdo_intern

##############################################################################
Conversion en une table CSV du fichier sur l'impot sur le revenu :
https://www.data.gouv.fr/fr/datasets/l-impot-sur-le-revenu-par-collectivite-territoriale/

Le fichier créé a le même nom que celui d'origine mais avec l'extension .csv
"""

from os.path import join
import pandas as pd

def load_ircom(path, file_name):
    '''Crée un csv à partir du fichier IRCOM'''
    
    column_names = ['departement', 'code_commune', 'nom', 'revenu_par_tranche',
                'nb_de_foyers', 'revenu_fiscal_de_ref_des_foyers', 'impot_total', 'nb_de_foyers_imposables', 
                'revenu_fiscal_de_ref_des_foyers_imposables', 'salaires_nb_foyers_concernes',
                'salaires_montant', 'retraites_nb_foyers_concernes', 'retraites_montant' ]
                
    print '\nAttention, le chargement prend quelques minutes'
    table = pd.DataFrame(columns = column_names)
    for i in range(111):
        try:
            print 'Chargement de la page', i
            test = pd.read_excel(join(path, file_name),
                                 i,
                                 skiprows = 23)
            test = test.iloc[:,1:]
            test.columns = column_names
            test['departement'] = test.departement.apply(lambda x: str(x).zfill(3))
            test['code_commune'] = test.departement.apply(lambda x: str(x).zfill(3))
            if len(test) == 0:
                print '   >>>  empty'
            table =  table.append(test, ignore_index = True)
        except:
            print '  >>  Erreur dans le chargement de la page', i
            pass
    table.to_csv(join(path, file_name.replace('.xls', '.csv')), index = False)
    return table
    print 'Chargement terminé'
    
    
    
if __name__ == '__main__':
    path = '/home/debian/Documents/data/villes' # Path du fichier .xls
    file_name = 'fichedescriptive_7270.xls' # Nom du fichier .xls
    table = load_ircom(path, file_name)
