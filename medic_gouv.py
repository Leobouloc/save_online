# -*- coding: utf-8 -*-
'''
Created on 26 juin 2014
c'''
import pandas as pd
from numpy.core.numeric import dtype
import numpy as np
import pdb

path_data = "C:\\Users\\work\\Documents\\ETALAB_data\\"
#Derniere mise à jour BDM
maj_bdm = 'maj_20140915122241\\'


dico_variables = dict( 
                      bdpm = ['CIS','Nom','Forme','Voies','Statut_AMM','Type_AMM','Etat','Date_AMM','Statut_BDM','Num_Europe','Titulaires','Surveillance'],
                      CIP_bdpm = ['CIS','CIP7','Label_presta', 'Statu_admin_presta','etat_commercialisation',
                                        'Date_declar_commerc','CIP13','aggrement_collectivites','Taux_rembours','Prix', 'indic_droit_rembours'],
                      GENER_bdpm = ['Id_Groupe','Nom_Groupe','CIS','Type','Num_Tri'],
                      COMPO_bdpm = ['CIS','Element_Pharma','Code_Substance','Nom_Substance','Dosage','Ref_Dosage','Nature_Composant','Substance_Fraction'],
                      HAS_SMR_bdpm = ['CIS','HAS','Evalu','Date','Valeur_SMR','Libelle_SMR'],
                      HAS_ASMR_bdpm = ['CIS','HAS','Evalu','Date','Valeur_ASMR','Libelle_ASMR'],
                      )
                    
def load_medic_gouv(maj_bdm, var_to_keep=None, CIP_not_null=False):
    ''' renvoie les tables fusionnées issues medicament.gouv.fr
        si var_to_keep est rempli, on ne revoit que la liste des variables
    '''
    # chargement des données
    path = path_data  + "medicaments_gouv\\" +  maj_bdm
    output = None
    for name, vars in dico_variables.iteritems():
        # teste si on doit ouvrir la table
        if var_to_keep is None: 
            intersect = vars
        if var_to_keep is not None:
            intersect = [var for var in vars if var in var_to_keep]
        if len(intersect) > 0:
            tab = pd.read_table(path + 'CIS_' + name +'.txt', header=None)
            if name in ['COMPO_bdpm', 'GENER_bdpm']:
                tab = tab.iloc[:,:-1]
            tab.columns = vars
            tab = tab[['CIS'] + intersect]
            # correction ad-hoc...
            if tab['CIS'].dtype == 'object':
                problemes = tab['CIS'].str.contains('REP', na=False)
                problemes = problemes | tab['CIS'].isin(['I6049513','inc     '])
                tab = tab.loc[~problemes,:]
                tab['CIS'].astype(int)
            
            if output is None: 
                output = tab
                print "la première table est " + name + " , son nombre de ligne est " + str(len(output))
            else:
                output = output.merge(tab, how='outer', on='CIS', suffixes=('',name[:-4]))
                if CIP_not_null:
                    if 'CIP7' in output.columns:
                        output = output[output['CIP7'].notnull()]
                print "après la fusion avec " + name + " la base mesure " + str(len(output))
    return output

if __name__ == '__main__':
    test = load_medic_gouv(maj_bdm, ['Etat','Date_AMM','CIP7','Label_presta','Date_declar_commerc','Taux_rembours','Prix','Id_Groupe','Type',
                                      'indic_droit_rembours', 'Statu_admin_presta','Element_Pharma','Code_Substance','Nom_Substance','Dosage',
                                      'Ref_Dosage','Nature_Composant','Substance_Fraction'])
#     test = load_medic_gouv(maj_bdm)

    nom = test['Label_presta']
    nom = nom[nom.notnull()]
    comprimes = nom.str.contains('comprim')
    liquides = nom.str.contains('ml') | nom.str.contains(' l')
#     gelules = test.str.contains(u'g\xe9lule')
    plaquettes = nom.str.contains('plaquette')
    sachets= nom.str.contains('sachet')
    flacons = nom.str.contains('flacon')
    solides = nom.str.contains(' g') | nom.str.contains('mg')
    liquides = nom.str.contains('ml')
    test = nom[~(solides | liquides| plaquettes | comprimes | sachets| flacons)] # On enlève tous les médicaments dont le contenant est référencé
    
    contenants = ['plaquette','flacon','tube', u'récipent', 'sachet', 'cartouche', 'boite', 'pochette', 'seringue']
    contenant_series = pd.Series(index=nom.index)
    for contenant in contenants: 
        try: 
#             concerne = nom.str.match(contenant)
            contient = nom.str.contains(contenant)
#             contient_strict = nom.str.contains(' ' + contenant)
#             debute = nom.str.match(contenant)
#             test = contient & (~debute)
#             retest = contient_stric & (~test)
            assert contenant_series[contient].isnull().all()
            contenant_series[contient] = contenant
            nom = nom.str.replace(contenant, 'contenant')
        except:
            deuxieme_contenant = contenant_series[contient][contenant_series[contient].notnull()]
            nom.loc[deuxieme_contenant.index]
            nom.loc[deuxieme_contenant.index].iloc[0]
            print nom.loc[deuxieme_contenant.index]
    
    pdb.set_trace()#debug tool // c to continue
    
#     test = nom[~(comprimes | liquides | plaquettes)]
#     test.iloc[0]
#     
#     test = [x[1][-3:] for x in nom.str.split('MG')]
#     
#     
#     'Label_presta'
# Pourquoi certains médicament n'ont pas de CIP ?