# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 14:47:57 2014

@author: work
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = '/home/debian/Documents/data/'

column_names = ['departement', 'code_commune', 'nom', 'revenu_par_tranche',
                'nb_de_foyers', 'revenu_fiscal_de_ref_des_foyers', 'impot_total', 'nb_de_foyers_imposables', 
                'revenu_fiscal_de_ref_des_foyers_imposables', 'salaires_nb_foyers_concernes',
                'salaires_montant', 'retraites_nb_foyers_concernes', 'retraites_montant' ]

column_names_to_keep = ['code_dept', 'code_comm', 'nom_commune', 'cat_rev_fisc', 'nb_foy_fisc',
                        'rev_fisc_de_ref_des_foy_fisc', 'impot_net_total', 'nb_foy_fisc_imposables',
                        'rev_fisc_de_ref_des_foy_fisc_imposables', 'tr_et_sal_nb_foy_concernes',
                        'tr_et_sal_montant', 'retr_et_pens_nb_foy_concernes', 'retr_et_pens_montant']


#table = pd.DataFrame(columns = column_names)
#
#for i in range(0,150):
#    print i
#    try:

#        print i
#        test = pd.read_excel(os.path.join(path, 'IRCOM_2012.xls'), i, skiprows = 23)
#        test = test.iloc[:,1:]
#        test.columns = column_names
#        table =  table.append(test, ignore_index = True)
#    except:
#        pass
    
def load_info_villes(path):
    file = os.path.join(path, 'villes', 'info_villes.csv' )  
    villes = pd.read_csv(file, sep = ';')
    
    villes.columns = [u'insee_code', u'postal_code', u'nom_comm', u'nom_dept',
                      u'nom_region', u'statut', u'z_moyen', u'superficie', 
                      u'population', u'geo_point_2d', u'geo_shape',
                      u'id_geofla', u'code_comm', u'code_cant', u'code_arr', 
                      u'code_dept', u'code_reg']
    return villes
 
 
def load_impots(path):
    file = os.path.join(path, 'villes', 'impots_par_commune_2012.csv' )
    tab = pd.read_csv(file, sep = ';')
    tab.columns = column_names_to_keep
    return tab
    

def load_population(path):
    file = os.path.join(path, 'villes', 'population_historique.csv')
    population = pd.read_csv(file, sep = ';')
    
    def _int(x):
        try:
            return np.int64(x)
        except:
            return x
    
    population['code_comm'] = population['DEPCOM'].apply(lambda x: x[2:]).apply(_int)
    population['code_dept'] = population['DEPCOM'].apply(lambda x: x[:2]).apply(str)
    population['accrois_pop'] = (population['PMUN11'] - population['PSDC90'])/population['PSDC90']
    return population


#pres_2012_1_sel = [u'Code du département', u'Libellé de la commune','Code de la commune', 'Inscrits', 'Abstentions', 'Blancs et nuls', 'Voix', 'Voix.1', 'Voix.2', 'Voix.3', 'Voix.7', 'Voix.9' ]
#pres_2012_1_col = ['dep', 'nom_comm', 'code_comm', 'inscrits', 'abst', 'blcs_nuls', 'joly', 'lepen', 'sarkozy', 'melenchon', 'bayrou', 'hollande']
#
#pres_2012_2_sel = [u'Code du département', u'Libellé de la commune','Code de la commune', 'Inscrits', 'Abstentions', 'Blancs et nuls', 'Voix', 'Voix.1']
#pres_2012_2_col = ['dep', 'nom_comm', 'code_comm', 'inscrits', 'abst', 'blcs_nuls', 'hollande', 'sarkozy']

def load_elections(path):
    annees = ['2007', '2012']
    elections = pd.DataFrame(columns = ['dep', 'nom_comm', 'code_comm'])
    for annee in annees:
        for tour in [1,2]:
            prefix = annee + '_' + str(tour) + '_'
            print prefix
            file_name = 'elections_pres_' + annee + '.xls'
            file = os.path.join(path, 'elections', file_name)
            table = pd.read_excel(file, tour-1) 
            

            
            range_length = (len(table.columns)-15) // 6
            pres_sel = [u'Code du département', u'Libellé de la commune','Code de la commune', 'Inscrits', 'Abstentions', 'Blancs et nuls', 'Voix'] + ['Voix.' + str(n) for n in range(1, range_length)]
            pres_col = ['dep', 'nom_comm', 'code_comm', prefix + 'inscrits', prefix + 'abst', prefix + 'invalides'] + [prefix + (table['Nom'].iloc[0]).lower()] + [prefix + (table['Nom.' + str(n)].iloc[0]).lower() for n in range(1, range_length)]
            pres_col = [col.replace(' ', '_') for col in pres_col]
            pres_col = [col.replace('\xc3\xa9', 'e') for col in pres_col]            
            table = table[pres_sel]
            table.columns = pres_col
            elections = elections.merge(table, how = 'outer', on = ['dep', 'nom_comm', 'code_comm'])
    elections.dep = elections.dep.apply(str)
    return elections
            
####################
_2002_1_extr_gauche = ['2002_1_gluckstein', '2002_1_hue', '2002_1_laguiller', '2002_1_besancenot']     
_2002_1_gauche = ['2002_1_taubira', '2002_1_mamere', '2002_1_jospin']
_2002_1_centre = ['2002_1_lepage', '2002_1_bayrou', '2002_1_chevenement']
_2002_1_droite = ['2002_1_chirac', '2002_1_saint-josse', '2002_1_boutin', '2002_1_madelin'] 
_2002_1_extr_droite = ['2002_1_megret', '2002_1_le_pen']

_2002_1_verts = '2002_1_mamere'
_2002_1_soc = '2002_1_jospin'
_2002_1_rpr = '2002_1_chirac'

_2002_1_gauche_large = _2002_1_extr_gauche + _2002_1_gauche
_2002_1_droite_large = _2002_1_centre + _2002_1_droite + _2002_1_extr_droite
####################

####################
_2007_1_extr_gauche = ['2007_1_besancenot', '2007_1_buffet', u'2007_1_bove', '2007_1_laguiller']     
_2007_1_gauche = ['2007_1_schivardi', '2007_1_voynet', '2007_1_royal', ]
_2007_1_centre = ['2007_1_bayrou']
_2007_1_droite = [u'2007_1_de_villiers', '2007_1_nihous', '2007_1_sarkozy'] 
_2007_1_extr_droite = ['2007_1_le_pen']

_2007_1_verts = '2007_1_voynet'
_2007_1_soc = '2007_1_royal'
_2007_1_rpr = '2007_1_sarkozy'

_2007_1_gauche_large = _2007_1_extr_gauche + _2007_1_gauche
_2007_1_droite_large = _2007_1_centre + _2007_1_droite + _2007_1_extr_droite
####################

####################
_2012_1_extr_gauche = [u'2012_1_melenchon', '2012_1_poutou', '2012_1_arthaud']     
_2012_1_gauche = ['2012_1_joly', '2012_1_cheminade', '2012_1_hollande']
_2012_1_centre = ['2012_1_bayrou']
_2012_1_droite = ['2012_1_sarkozy']
_2012_1_extr_droite = ['2012_1_le_pen', '2012_1_dupont-aignan']

_2012_1_verts = '2012_1_joly'
_2012_1_soc = '2012_1_hollande'
_2012_1_rpr = '2012_1_sarkozy'

_2012_1_gauche_large = _2012_1_extr_gauche + _2012_1_gauche
_2012_1_droite_large = _2012_1_centre + _2012_1_droite + _2012_1_extr_droite
####################

dict  = {'_2002_1_gauche_large' : _2002_1_gauche_large, '_2002_1_droite_large' : _2002_1_droite_large,
         '_2007_1_gauche_large':_2007_1_gauche_large, '_2007_1_droite_large': _2007_1_droite_large,
         '_2012_1_gauche_large': _2012_1_gauche_large, '_2012_1_droite_large':_2012_1_droite_large}

def elections_prop_maker(table, candidat):
    '''candidat peut prendre par exemple 2007_1_sarkozy'''
    inscrits = table[candidat[:7] + 'inscrits']
    abst = table[candidat[:7] + 'abst']
    return table[candidat] / (inscrits - abst)

def variabilite(table):
    for annee in annees:
        string_gauche = '_' + str(annee) + '_1_gauche_large'
        string_droite = '_' + str(annee) + '_1_droite_large'
        if annee == annees[0]:
            try:
                del var
            except:
                pass
            gauche = table[dict[string_gauche]].sum(axis = 1).apply(float)
            droite = table[dict[string_droite]].sum(axis = 1).apply(float)
            rapport = gauche/(droite + gauche)
        else:
            new_gauche = table[dict[string_gauche]].sum(axis = 1).apply(float)
            new_droite = table[dict[string_droite]].sum(axis = 1).apply(float)
            new_rapport = new_gauche/(new_gauche + new_droite)
            try:
                var += (new_rapport - rapport).apply(abs)
            except:
                var = (new_rapport - rapport).apply(abs)
            gauche = new_gauche
            droite = new_droite
            rapport = gauche/(droite + gauche)  
    return var





#def lambda_vote(x):
#    if x<43:
#        return 0
#    elif x<51:
#        return 1
#    elif x<59:
#        return 2
#    else:
#        return 3


#tab.replace('n.d.', np.nan, inplace = True)
#
#def rewrite_departement_lambda (x):
#    if x in ['2A0', '2B0', '971', '972', '973', '974', 'B31']:
#        return x
#    else:
#        x = int(x.split('.')[0])/10
#        return(str(x))
#        
#tab['departement'] = tab['departement'].apply(rewrite_departement_lambda)

def villes_merge(villes, tab, elections, population):
    tab_small = tab[tab['cat_rev_fisc'] == 'Total']
    tab_small.drop('cat_rev_fisc', axis = 1, inplace = True)
    
    #tab_small.to_csv(os.path.join(path, 'impots_par_commune_agrege.csv'), sep = ';', index = False)
    #tab.to_csv(os.path.join(path, 'impots_par_commune.csv'), sep = ';', index = False)
    
    #tab_small['code_commune'] =tab_small['code_commune'].apply(lambda x: x.zfill(3)) 
    #tab_small['dep'] = tab_small['dep'].apply(lambda x: x.zfill(2))
    
    tab_small['code_comm'] = tab_small['code_comm'].apply(lambda x: int(x))
    villes['code_comm'] = villes['code_comm'].apply(lambda x: int(x))
    
    
    
    # Test cont
    villes = pd.merge(tab_small, villes[['insee_code', 'code_comm', 'code_dept', 'postal_code','nom_comm','population', 'superficie']], on = ['code_comm', 'code_dept'], how = 'left')
    villes = villes.merge(elections, how = 'left', left_on = ['code_comm', 'code_dept'], right_on = ['code_comm', 'dep'])
    villes = villes.merge(population, on = ['code_comm', 'code_dept'], how = 'outer')   
    
    ### Metriques
    villes['population'] *= 1000
    villes['densite'] = villes['population']/villes['superficie']
    villes['nb_votants'] = villes['2012_2_inscrits'] - villes['2012_2_abst']
    villes['richesse'] = villes['rev_fisc_de_ref_des_foy_fisc'] / villes['nb_foy_fisc']
    villes['assistes'] = villes['retr_et_pens_montant'] / villes['rev_fisc_de_ref_des_foy_fisc']
    
    villes['variabilite'] = variabilite(villes)
    
    villes['hollande_2_2012_prop'] = villes['2012_2_hollande'] / (villes['2012_2_hollande'] + villes['2012_2_sarkozy'])

    villes['code_comm'] = villes.code_comm.apply(str).apply(lambda x: x.zfill(3))
    villes['code_dept'] = villes.code_dept.apply(str).apply(lambda x: x.zfill(2))
    return villes




def categorizer(table, sort_string = 'densite', cat_num = 10):

    a = table.copy()
    a.sort(sort_string, inplace = True)
    a = a['nb_votants']
    a = a.cumsum()
    max_val = a.max()
    quantiles = [float(max_val)/cat_num * float(x) for x in range(1, cat_num)]
    
    i = 0
    indexes = []
    for val in quantiles:
        loop = True
        val_index =[]
        while loop:
            loop = (a.iloc[i] < val) | (np.isnan(a.iloc[i]))
            val_index += [a.index[i]]
            i += 1
        indexes += [val_index]   
    
    new_col_name = sort_string + '_cat'
    table[new_col_name] = cat_num - 1
    for i in range(len(indexes)):
        table.loc[indexes[i], new_col_name] = i
    table.loc[table[sort_string].isnull(), new_col_name] = np.nan
    return table

def heat_map(table, x_str = 'richesse', y_str = 'densite', z_str = 'variabilite', precision = 10):    
    assert z_str in table.columns
    
    x_str_cat = x_str + '_cat'
    y_str_cat = y_str + '_cat'
    
    if not(x_str_cat in table.columns):
        print 'calculating categories for : ' + x_str
        table = categorizer(table, sort_string = x_str, cat_num = 10)
    if not(y_str_cat in table.columns):
        print 'calculating categories for : ' + y_str
        table = categorizer(table, sort_string = y_str, cat_num = 10)

    a = pd.pivot_table(villes, values = z_str, index = x_str_cat, columns = y_str_cat, 
                       aggfunc = np.mean)
    print a 


    print 'calculating ticks...'
    x_ticks = [min(villes.loc[villes[x_str].notnull(), x_str])]
    for cat in range(10):
        if not np.isnan(cat):
            print cat
            x_ticks += [max(villes.loc[villes[x_str_cat]==cat, x_str])]

    y_ticks = [min(villes.loc[villes[y_str].notnull(), y_str])]
    for cat in range(10):
        if cat in villes[y_str_cat]:
            y_ticks += [max(villes.loc[villes[y_str_cat]==cat, y_str])]
    print x_ticks
    
    fig, ax = plt.subplots()   
    ax.imshow(a, interpolation = 'none')    
    ax.set_xticks([x - 0.5 for x in range(11)])
    ax.set_yticks([x - 0.5 for x in range(11)])
    ax.set_xticklabels([minifunc(tic) for tic in x_ticks], rotation = 'vertical')
    ax.set_yticklabels([minifunc(tic) for tic in y_ticks])
#    ax.colorbar()
    plt.show()

def minifunc(x):
    assert x>=0
    if x == 0:
        return 0
    if (100 <= x)  and (x <1000):
        return round(x)
    elif x < 100:
        return minifunc(10 * x) / float(10)
    else :
        return minifunc(x / 10) * 10


try:
    villes
except:
    villes = load_info_villes(path)
try:
    tab
except:
    tab = load_impots(path)
try:
    elections
except:
    elections = load_elections(path)
try:
    population
except:
    population = load_population(path)
    
tout = villes_merge(villes, tab, elections, population)
    

#villes['quart_vote'] = villes['voix_sarkozy'].apply(lambda_vote)

##villes = villes[['nb_foy_fisc', 'rev_fisc_de_ref_des_foy_fisc',
#                                 'impot_net_total', 'nb_foy_fisc_imposables', 
#                                 'rev_fisc_de_ref_des_foy_fisc_imposables',
#                                 u'tr_et_sal_nb_foy_concernes', u'tr_et_sal_montant',
#                                 u'retr_et_pens_nb_foy_concernes',  u'retr_et_pens_montant',
#                                 u'postal_code', 'insee_code', 'nom_comm', u'population']] #, 'code_comm', 'code_dept']]
#

# Aggregation par code postal
#villes = villes.groupby('postal_code').sum()

#h['CODE_POSTAL'] = h['CODE_POSTAL'].apply(str)
#
#h = pd.merge(h, villes, left_on = 'CODE_POSTAL', right_index = True, how = 'left')




