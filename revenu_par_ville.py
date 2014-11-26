# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 14:47:57 2014

@author: work
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from random_forest import entropy

path = 'C:\\Users\\work\\Documents\\ETALAB_data'

column_names = ['departement', 'code_commune', 'nom', 'revenu_par_tranche',
                'nb_de_foyers', 'revenu_fiscal_de_ref_des_foyers', 'impot_total', 'nb_de_foyers_imposables', 
                'revenu_fiscal_de_ref_des_foyers_imposables', 'salaires_nb_foyers_concernes',
                'salaires_montant', 'retraites_nb_foyers_concernes', 'retraites_montant' ]

column_names_to_keep = ['code_dept', 'code_comm', 'nom_commune', 'cat_rev_fisc', 'nb_foy_fisc',
                        'rev_fisc_de_ref_des_foy_fisc', 'impot_net_total', 'nb_foy_fisc_imposables',
                        'rev_fisc_de_ref_des_foy_fisc_imposables', 'tr_et_sal_nb_foy_concernes',
                        'tr_et_sal_montant', 'retr_et_pens_nb_foy_concernes', 'retr_et_pens_montant']

annees = ['2002', '2007', '2012']

def load_info_villes(path):
    try:
        villes
    except:
        file = os.path.join(path, 'info_villes.csv' )  
        villes = pd.read_csv(file, sep = ';')
        
        villes.columns = [u'insee_code', u'postal_code', u'nom_comm', u'nom_dept',
                          u'nom_region', u'statut', u'z_moyen', u'superficie', 
                          u'population', u'geo_point_2d', u'geo_shape',
                          u'id_geofla', u'code_comm', u'code_cant', u'code_arr', 
                          u'code_dept', u'code_reg']
        villes['code_comm'] = villes['code_comm'].apply(lambda x: int(x))
        villes['population'] *= 1000
    return villes


def load_impots(path):
    try:
        impots
    except:
        file = os.path.join(path, 'impots_par_commune_2012.csv' )  
        impots = pd.read_csv(file, sep = ';')
        impots.columns = column_names_to_keep
        impots['code_comm'] = impots['code_comm'].apply(lambda x: int(x))
    return impots

def weighted_avg_and_std(values, weights):
    """
    Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)  # Fast and numerically precise
    return math.sqrt(variance)


def entropie_sociale(impots):
    print 'Actuellement dans entropie sociale'
#    from random_forest import entropy
    impots['rev_moy'] = impots.rev_fisc_de_ref_des_foy_fisc / impots.nb_foy_fisc
    selector = impots['cat_rev_fisc'] != 'Total'
    entropie_tab = impots[selector].groupby(['code_comm', 'code_dept']).apply(lambda x: weighted_avg_and_std(x['rev_moy'], x['nb_foy_fisc'])).reset_index()
    entropie_tab.columns = ['code_comm', 'code_dept', 'entropie']
    impots = impots.merge(entropie_tab, how = 'outer', on = ['code_comm', 'code_dept'])
    entropie_tab.loc[entropie_tab['entropie'].isnull(), 'entropie_sociale'] = 0
    return impots

    
def load_impots_aggrege(path):
    try:
        impots_aggrege
    except:
        # TODO: Indicateur d'inegalites
        impots = load_impots(path)
        impots = entropie_sociale(impots)
        impots_aggrege = impots[impots['cat_rev_fisc'] == 'Total']
        impots_aggrege = impots_aggrege.drop('cat_rev_fisc', axis = 1)
    return impots_aggrege


def load_elections(path, annees = annees, force = False):
    '''Force = True will reload regardless of preexisting file'''
    file_write = os.path.join(path, 'elections_csv.csv')
    try:
        assert not force
        
        elections = pd.read_csv(file_write, sep = ';')
    except:
        elections = pd.DataFrame(columns = ['code_dept', 'nom_comm', 'code_comm'])
        for annee in annees:
            for tour in [1,2]:
                prefix = annee + '_' + str(tour) + '_'
                print prefix
                file_name = 'elections_pres_' + annee + '.xls'
                file = os.path.join(path, file_name)
                table = pd.read_excel(file, tour - 1)
                range_length = (len(table.columns) - 15) // 6
                pres_sel = [u'Code du département', u'Libellé de la commune','Code de la commune', 'Inscrits', 'Abstentions', 'Blancs et nuls', 'Voix'] + ['Voix.' + str(n) for n in range(1, range_length)]
                pres_col = ['code_dept', 'nom_comm', 'code_comm', prefix + 'inscrits', prefix + 'abst', prefix + 'invalides'] + [prefix + (table['Nom'].iloc[0]).lower()] + [prefix + (table['Nom.' + str(n)].iloc[0]).lower() for n in range(1, range_length)]
                table = table[pres_sel]
                table.columns = pres_col
                elections = elections.merge(table, how = 'left', on = ['code_dept', 'nom_comm', 'code_comm'])
        elections.code_dept = elections.code_dept.apply(str)
        elections.to_csv(file_write, sep = ';', index = False)
    return elections


def make_dict():
    ####################
    _2002_1_extr_gauche = ['2002_1_gluckstein', '2002_1_hue', '2002_1_laguiller', '2002_1_besancenot']     
    _2002_1_gauche = ['2002_1_taubira', '2002_1_mamere', '2002_1_jospin']
    _2002_1_centre = ['2002_1_lepage', '2002_1_bayrou', '2002_1_chevenement']
    _2002_1_droite = ['2002_1_chirac', '2002_1_saint-josse', '2002_1_boutin', '2002_1_madelin'] 
    _2002_1_extr_droite = ['2002_1_megret', '2002_1_le pen']
    
    _2002_1_verts = '2002_1_mamere'
    _2002_1_soc = '2002_1_jospin'
    _2002_1_rpr = '2002_1_chirac'
    
    _2002_1_gauche_large = _2002_1_extr_gauche + _2002_1_gauche
    _2002_1_droite_large = _2002_1_centre + _2002_1_droite + _2002_1_extr_droite
    ####################

    ####################
    _2007_1_extr_gauche = ['2007_1_besancenot', '2007_1_buffet', u'2007_1_bové', '2007_1_laguiller']     
    _2007_1_gauche = ['2007_1_schivardi', '2007_1_voynet', '2007_1_royal', ]
    _2007_1_centre = ['2007_1_bayrou']
    _2007_1_droite = [u'2007_1_de villiers', '2007_1_nihous', '2007_1_sarkozy'] 
    _2007_1_extr_droite = ['2007_1_le pen']
    
    _2007_1_verts = '2007_1_voynet'
    _2007_1_soc = '2007_1_royal'
    _2007_1_rpr = '2007_1_sarkozy'
    
    _2007_1_gauche_large = _2007_1_extr_gauche + _2007_1_gauche
    _2007_1_droite_large = _2007_1_centre + _2007_1_droite + _2007_1_extr_droite
    ####################
    
    ####################
    _2012_1_extr_gauche = [u'2012_1_mélenchon', '2012_1_poutou', '2012_1_arthaud']     
    _2012_1_gauche = ['2012_1_joly', '2012_1_cheminade', '2012_1_hollande']
    _2012_1_centre = ['2012_1_bayrou']
    _2012_1_droite = ['2012_1_sarkozy']
    _2012_1_extr_droite = ['2012_1_le pen', '2012_1_dupont-aignan']
    
    _2012_1_verts = '2012_1_joly'
    _2012_1_soc = '2012_1_hollande'
    _2012_1_rpr = '2012_1_sarkozy'
    
    _2012_1_gauche_large = _2012_1_extr_gauche + _2012_1_gauche
    _2012_1_droite_large = _2012_1_centre + _2012_1_droite + _2012_1_extr_droite
    ####################
    
    dict  = {'_2002_1_gauche_large' : _2002_1_gauche_large, '_2002_1_droite_large' : _2002_1_droite_large,
             '_2007_1_gauche_large':_2007_1_gauche_large, '_2007_1_droite_large': _2007_1_droite_large,
             '_2012_1_gauche_large': _2012_1_gauche_large, '_2012_1_droite_large':_2012_1_droite_large}
    
    return dict

def variabilite(table, dict, annees = annees):
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


def load_and_merge(path):
    try:
        villes_merge
    except:
        villes = load_info_villes(path)
        elections = load_elections(path)
        impots_aggrege = load_impots_aggrege(path)
        
        #impots_aggrege.to_csv(os.path.join(path, 'impots_par_commune_agrege.csv'), sep = ';', index = False)
        #impots.to_csv(os.path.join(path, 'impots_par_commune.csv'), sep = ';', index = False)
        
        #impots_aggrege['code_commune'] =impots_aggrege['code_commune'].apply(lambda x: x.zfill(3)) 
        #impots_aggrege['code_dept'] = impots_aggrege['code_dept'].apply(lambda x: x.zfill(2))
        
        # Test cont
        villes_merge = pd.merge(impots_aggrege, villes[['insee_code', 'code_comm', 'code_dept', 'postal_code','nom_comm','population', 'superficie']], on = ['code_comm', 'code_dept'], how = 'left')
        villes_merge = villes_merge.merge(elections, how = 'left', on = ['code_comm', 'code_dept'])

    return villes_merge

def metriques(table):
        table['densite'] = table['population']/table['superficie']
        table['nb_votants'] = table['2012_2_inscrits'] - table['2012_2_abst']
        table['richesse'] = table['rev_fisc_de_ref_des_foy_fisc'] / table['nb_foy_fisc']
        table['assistes'] = table['retr_et_pens_montant'] / table['rev_fisc_de_ref_des_foy_fisc']
        
        dict = make_dict()
        table['variabilite'] = variabilite(table, dict)
        table['hollande_2_2012_prop'] = table['2012_2_hollande'] / (table['2012_2_hollande'] + table['2012_2_sarkozy'])
        table['lepen_2012_prop'] = table['2012_1_le pen'] / (table['2012_1_inscrits'] - table['2012_1_abst'])
        return table


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
