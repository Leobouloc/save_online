# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 15:26:47 2014

@author: work
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
from tools.panda_tools import *
import itertools

from sklearn.ensemble import RandomForestClassifier

path = '/home/debian/Documents/data/strasbourg'
file = os.path.join(path, 'CUS_CUS_ACP_MPUB.XLS')
file2 = os.path.join(path, 'CUS_CUS_AMC_MPUB2.xls')
file3 = os.path.join(path, 'CUS_CUS_AMC_STAMP2.xls')

################################################
# Fonctions de nettoyage

def unify_type(table):
    '''unifie les champs type et type_proc dans new_type'''
    def _new_type(line):
        new_type = sort((line['type'], line['type_proc']))
        new_type = new_type[0] + ' - ' + new_type[1]
        return new_type    

    table['new_type'] = np.nan
    sel = table.type.notnull() & table.type_proc.notnull() & (table.type == table.type_proc)
    table.loc[sel, 'new_type'] = table.loc[sel, 'type']
    sel_2 = table.type.notnull() & table.type_proc.notnull() & (table.type != table.type_proc)
    table.loc[sel_2, 'new_type'] = table[sel_2].apply(_new_type, axis = 1)
    sel_3 = table.type.notnull() & table.type_proc.isnull()
    table.loc[sel_3, 'new_type'] = table.loc[sel_3, 'type']
    sel_4 = table.type.isnull() & table.type_proc.notnull()
    table.loc[sel_4, 'new_type'] = table.loc[sel_4, 'type_proc']
    return table

################################################

marches = pd.read_excel(file)
marches.dropna(how='all', inplace=True)
marches.columns = ['collectivite', 'annee', 'numero', 'objet_1', 'objet_2', 'type',
                   'attributaire', 'cp', 'debut', 'seuils']
marches = rem_whspc(marches)
marches['objet'] = marches.objet_1 + ' ' + marches.objet_2

marches_2 = pd.read_excel(file2)
marches_2.dropna(how='all', inplace=True)
marches_2.columns = ['collectivite', 'annee', 'numero', 'reconductible', 'annee_initiale', 'objet_1', 
                     'objet_2', 'mode_passation', 'num_lot', 'libelle', 'forme', 'type',
                   'attributaire', 'cp', 'siret', 'debut', 'montant_attribue', 'avenants', 'num_proc']
marches_2 = rem_whspc(marches_2)
marches_2['objet'] = marches_2.objet_1 + ' ' + marches_2.objet_2.fillna('')



attract = pd.read_excel(file3)
attract.dropna(how='any', inplace=True)
attract.columns = ['collectivite', 'num_proc', 'num_dossier', 'objet_procedure', 'mode_passation',
                   'type_proc', 'date_publication', 'date_limite_reception', 'date_ouverture',
                   'date_jugement', 'date_notification', 'nb_lots', 'nb_depots']
attract = rem_whspc(attract)
                  
### Attention : il y a des doublons pour num_proc dans attract et dans marches_2
### De plus, marches_2 manque de nombreux id_procedure

test = marches_2.merge(attract, how = 'outer', on = 'num_proc')

# On remplace les montants nuls par nan
test.loc[test.montant_attribue == 0, 'montant_attribue'] = np.nan
# On regroupe els infos sur le type de contrat
test = unify_type(test)


test['duree'] = test['date_limite_reception'] - test['date_publication']
test.loc[test.duree.notnull(), 'duree'] = test[test.duree.notnull()]['duree'].apply(float)
test['duree'] = test.duree.apply(lambda x: x / np.timedelta64(1, 's'))
test['ratio'] = test['avenants'].apply(float) / test['montant_attribue'].apply(float)
test['dep'] = np.nan
test.loc[test.cp.notnull(), 'dep'] = test.loc[test.cp.notnull(), 'cp'].apply(lambda x: x[:2])
toast = panda_merge(test, test['ratio'])

#toast.groupby('nb_lots')[0].apply(lambda x : ((x!=0) & (x.notnull())).sum())
#
#
#sel = test['nb_depots'].notnull()
#toast = test[sel]
#toast['duree'] = toast['date_limite_reception'] - toast['date_publication']
#toast['duree'] = toast.duree.apply(int)
#toast['date_ouverture_str'] = toast['date_ouverture'].apply(str)
#toast['date_ouverture_mois'] = toast['date_ouverture_str'].apply(lambda x: x[5:7])
#toast['date_ouverture_an'] = toast['date_ouverture_str'].apply(lambda x: x[:4])
#
#duree = duree.apply(int)
#
## Nb de ratio non nuls et non nan
#(test['ratio'].notnull() & test['ratio'] != 0).sum()
#
#
####################################
#### Question qu'on se pose
#
#toast = test[test['avenants'].notnull()]
#grp_and_count(toast, 'attributaire', lambda x: x['avenants'].sum() / x['montant_attribue'].sum())
#grp_and_count(toast, 'type', lambda x: x['avenants'].sum() / x['montant_attribue'].sum())
#grp_and_count(toast, 'type', lambda x: x['montant_attribue'].sum())
#
## Que sont les lots, il n'y a pas de lien entre le champ nb_lots et l'actuel nb de lots
## ratio avenants par entreprise (COLAS est : +33% sur 45)
#
####################################






#new_seuils = [10000, 50000, 0.1 * 10**6, 10**6, 5*10**6]
##new_seuils = ['+ 4 000', '+ de 20 000', '+ de 90 000', '+ de 200 000', '+ de 2M']
#type_names = ['Travaux', 'Services', 'Fournitures']
#
#
## TODO : on trouve également STBG
#cus = ['Bischheim', 'Blaesheim', 'Eckbolsheim', 'Eckwersheim', 'Entzheim',
#        'Eschau', 'Fegersheim', 'Geispolsheim', 'Hoenheim', 'Holtzheim',
#        'Illkirch-Graffenstaden', 'Lampertheim', 'La Wantzenau', 'Lipsheim',
#        'Lingolsheim', 'Mittelhausbergen', 'Mundolsheim', 'Niederhausbergen',
#        'Oberhausbergen', 'Oberschaeffolsheim', 'Ostwald', 'Plobsheim',
#        'Reichstett', 'Schiltigheim', 'Souffelweyersheim', 'Strasbourg',
#        'Vendenheim']
#        
#
#
#def to_serie(string):
#    return pd.Series([villes.loc[villes['nom_commune'] == ville.upper(), string].iloc[0] for ville in cus])
#
## Renvoie le code insee et postal pour lesvilles ci dessus
##cus_code_insee = [villes.insee_code[villes.nom_comm == ville.upper()].iloc[0] for ville in cus]
##cus_code_postal = [villes.postal_code[villes.nom_comm == ville.upper()].iloc[0] for ville in cus]
#
#
#def repere_ville(table, cus):
#    '''Trouve le nom de ville dans le libelle et le place dans le champ ville'''
#    def lambda_func(ligne, cus):
#        libelle_1 = ligne['objet_1']
#        libelle_2 = ligne['objet_2']
#        list_villes = []
#        for ville in cus:
#            if ville == 'Strasbourg':
#                if (ville.lower() in libelle_1.lower()) or ('stbg' in libelle_1.lower()):
#                    list_villes = list_villes + [ville]
#                if isinstance(libelle_2, str):
#                    if (ville.lower() in libelle_2.lower()) or ('stbg' in libelle_2.lower()):
#                        list_villes = list_villes + [ville]                
#            else:
#                if ville.lower() in libelle_1.lower():
#                    list_villes = list_villes + [ville]
#                if isinstance(libelle_2, str):
#                    if ville.lower() in libelle_2.lower():
#                        list_villes = list_villes + [ville]
#        if len(set(list_villes)) == 1:
#            return list_villes[0]
#        else:
#            return np.nan
#    return table.apply(lambda ligne: lambda_func(ligne, cus), axis = 1)
#
#
#for [table, champ] in  [[marches, 'objet_1']]:#, [[attract, 'libelle'])]: #, [marches, 'objet_2']]:
#    print 'reecriture'
#    for _list in [['\xd6', 'O'],['\xf6', 'o'],['\xd4', 'O'],['\xf4', 'o'],
#                  ['\xcf', 'I'],['\xcf', 'I'],['\xef', 'i'],['\xcb', 'E'],
#                    ['\xeb', 'e'],['\xc7', 'e'],['\xc8', 'E'],['\xe8', 'e'],
#                    ['\xc9', 'E'], ['\xe9', 'e'], ['\xce', 'I'], ['\xee', 'i'],
#                     ['\xc0', 'A'], ['\xe0', 'a'], ['\xca', 'E'], ['\xea', 'e'],
#                    ['\xc2', 'A'], ['\xe2', 'a'], ["'", ' '], ['\xae', ''], ['\xce', ''],
#                     ['\xdb', 'U'], ['\xfb', 'u'], ['\xfc', 'u'], ['\xdc', 'U'], 
#                    ['\x92', ' '], ['\xb0', ' ']]:
#        table[champ] = table[champ].apply(lambda x: x.replace(_list[0], _list[1]))             
#    table[champ] = table[champ].apply(lambda x: x.lower())
##    table[champ] = table[champ].apply(lambda x: x.replace('\xd6', 'O'))  # Ô
##    table[champ] = table[champ].apply(lambda x: x.replace('\xf6', 'o'))  # ô
##    table[champ] = table[champ].apply(lambda x: x.replace('\xd4', 'O'))  # Ö
##    table[champ] = table[champ].apply(lambda x: x.replace('\xf4', 'o'))  # ö
##    table[champ] = table[champ].apply(lambda x: x.replace('\xcf', 'I'))  # Ï
##    table[champ] = table[champ].apply(lambda x: x.replace('\xef', 'i'))  # ï
##    table[champ] = table[champ].apply(lambda x: x.replace('\xcb', 'E'))  # Ë
##    table[champ] = table[champ].apply(lambda x: x.replace('\xeb', 'e'))  # ë
##    table[champ] = table[champ].apply(lambda x: x.replace('\xc7', 'e'))  # Ç
##    table[champ] = table[champ].apply(lambda x: x.replace('\xeb', 'e'))  # ç
##    table[champ] = table[champ].apply(lambda x: x.replace('\xc8', 'E'))  # È
##    table[champ] = table[champ].apply(lambda x: x.replace('\xe8', 'e'))  # è
##    table[champ] = table[champ].apply(lambda x: x.replace('\xc9', 'E'))  # É
##    table[champ] = table[champ].apply(lambda x: x.replace('\xe9', 'e'))  # é
##    table[champ] = table[champ].apply(lambda x: x.replace('\xce', 'I'))  # Î
##    table[champ] = table[champ].apply(lambda x: x.replace('\xee', 'i'))  # î
##    table[champ] = table[champ].apply(lambda x: x.replace('\xc0', 'A'))  # À
##    table[champ] = table[champ].apply(lambda x: x.replace('\xe0', 'a'))  # à
##    table[champ] = table[champ].apply(lambda x: x.replace('\xca', 'E'))  # Ê
##    table[champ] = table[champ].apply(lambda x: x.replace('\xea', 'e'))  # ê
##    table[champ] = table[champ].apply(lambda x: x.replace('\xc2', 'A'))  # Â
##    table[champ] = table[champ].apply(lambda x: x.replace('\xe2', 'a'))  # â
##    table[champ] = table[champ].apply(lambda x: x.replace("'", ' '))  # '
##    table[champ] = table[champ].apply(lambda x: x.replace('\xae', ''))  # ®
##    table[champ] = table[champ].apply(lambda x: x.replace('\xce', ''))  # ??????
##    table[champ] = table[champ].apply(lambda x: x.replace('\xdb', 'U'))  # Û
##    table[champ] = table[champ].apply(lambda x: x.replace('\xfb', 'u'))  # û
##    table[champ] = table[champ].apply(lambda x: x.replace('\xfc', 'u'))  # û
##    table[champ] = table[champ].apply(lambda x: x.replace('\xdc', 'U'))  # û
##    table[champ] = table[champ].apply(lambda x: x.replace('\x92', ' '))  # '
##    table[champ] = table[champ].apply(lambda x: x.replace('\xb0', ' '))  # °
#
#
#
#def rewrite_seuil(seuil):
#    if unicode(seuil) == u'Marchés de 4 000 à 19 999,99 euros HT':
#        return new_seuils[0]
#    elif unicode(seuil) == u'Marchés de 20 000 à 89 999,99 euros HT':
#        return new_seuils[1]
#    elif unicode(seuil) == u'Marchés de 90 000 à 199 999,99 euros HT':
#        return new_seuils[2]
#    elif unicode(seuil) == u'Marchés de 200 000 à 5 000 000 euros HT':
#        return new_seuils[3]
#    elif unicode(seuil) == u'Marchés de 5 000 000 euros HT et plus':
#        return new_seuils[4]
#
#
#def rewrite_debut_mois(date):
#    if isinstance(date, str):
#        new_date = date[6:10] + date[3:5]
#        return datetime.datetime.strptime(new_date, "%Y%m")
#    else:
#        return np.nan
#
#
#def rewrite_debut_an(date):
#    if isinstance(date, str):
#        new_date = date[6:10]
#        return datetime.datetime.strptime(new_date, "%Y")
#    else:
#        return np.nan
#
#
#def rewrite_debut_jour(date):
#    if isinstance(date, str):
#        new_date = date[:4] + date[5:7] + date[8:]
#        return new_date
#    else:
#        return np.nan
#
#
#marches.loc[:, 'new_seuils'] = marches['seuils'].apply(rewrite_seuil)
#marches.loc[:, 'debut_mois'] = marches['debut'].apply(rewrite_debut_mois)
#marches.loc[:, 'debut_an'] = marches['debut'].apply(rewrite_debut_an)
#marches.loc[:, 'debut_jour'] = marches['debut'].apply(rewrite_debut_jour)
#
#
#'''Plot des marchés débutant mensuellement par catégorie de prix'''
##a = marches.groupby('type')['debut_mois'].value_counts()
##for x in type_names:
##    b = a[x].sort_index()
##    plt.plot(b.index, b, label = str(x))
##    plt.xlabel(u"Début d'éxecution du marché")
##    plt.ylabel(u'Nombre de contrats débutant dans le mois')
##    plt.title(u'Nombre de contrats débutant chaque mois passés dans la CUS et VDS')
##    plt.legend()
##plt.show()
#
##    b = b/b.mean() # On normalise pour repérere les saisonnalités
#
#'''Plot des marchés débutant annuellement par catégorie de prix'''
##a = marches.groupby('new_seuils')['debut_an'].apply(lambda x: value_counts(x).sort_index())
##for x in new_seuils[:4]:
##    b = a[x].sort_index()
##    plt.plot(b.index, b, label = str(int(x)))
##    plt.legend()
##plt.show()
#
#'''Pourcentage d'offres fermées avec un seul concurrent par type'''
##attract.groupby(['code','type']).apply(lambda x: sum(x['nb_depots']<2) / float(len(x))) * 100
#
#
#
#


##########################################################""
## Deviner le type manquant par la frequence d'apparition

def _make_cols(ligne):
    global all_mots
    if isinstance(ligne.objet, str) or isinstance(ligne.objet, unicode):
        mots = ligne.objet.lower().replace('.', ' ').split()
        all_mots += mots

def make_cols(table):
    table.apply(_make_cols, axis = 1)
    return list(set(all_mots))

def _mot(ligne):
    '''sert a créer la table du nombre d occurence de chaque mot pour chaque type'''
    global table_des_mots
    print ligne['num_proc']
    cat_mot = ligne['new_type']
    mots = ligne['objet'].split()
    for mot in mots:
        mot = mot.lower()
        if mot in list(table_des_mots.index):
            table_des_mots.loc[mot, cat_mot] += 1
        else:
            table_des_mots.loc[mot, :] = 0
            table_des_mots.loc[mot, :cat_mot] = 1


#'''Création d'un lexique pour classer les descriptions dans marché'''
#table_des_mots = pd.DataFrame(columns = [u'Services', u'Fournitures', u'Travaux', u'Services - Travaux',
#       u'Fournitures - Services', u'Fournitures - Travaux'])
#sel = test.objet.notnull() & test.new_type.notnull()
#test[sel].apply(lambda ligne: _mot(ligne), axis = 1)
#table_des_freq_mots = table_des_mots / table_des_mots.sum()

def caract_phrase(table_des_freq_mots, ligne):
    '''a partir de la table_des_freq_mots, détermine le type '''
    if not (isinstance(ligne['objet'], str) or isinstance(ligne['objet'], unicode)):
        objet = ''
    else:
        objet = ligne['objet']
    mots = objet.lower().split()
    types = [u'Services', u'Fournitures', u'Travaux', u'Services - Travaux', u'Fournitures - Services', u'Fournitures - Travaux']
    probs = dict()
    for typ in types:
        probs[typ] = 1
    count = 0
    for mot in mots:
        if mot in list(table_des_freq_mots.index):
            count += 1
            for typ in types: 
                probs[typ] *= table_des_freq_mots.loc[mot, typ]
    max_value = -1
    for typ, value in probs.iteritems():
        if value > max_value:
            max_typ = typ
            max_value = value
        ligne[typ] = value
    print 'nb_mots en commun : ' + str(count)
    ligne['count'] = count
    ligne['type_calcule'] = max_typ
    return ligne

#test = test.apply(lambda x: caract_phrase(table_des_freq_mots, x), axis = 1)


##########################################################""
## Deviner le type avec With random forests

def _for_random_forests(ligne):
    if isinstance(ligne.objet, str) or isinstance(ligne.objet, unicode):
        mots = ligne.objet.lower().split()
        mots = ['_' + x for x in mots]
        ligne[mots] = True
        return ligne
    else:
        return ligne


    
#testa = test
#all_mots = []
#make_cols(testa)
#all_mots = list(set(all_mots))
#all_mots = ['_' +  x for x in all_mots]
#
#
#features = pd.DataFrame(False, index = testa.index, columns = all_mots)
#testa = testa.merge(features, how = 'inner', left_index = True, right_index = True)
#testa = testa.apply(_for_random_forests, axis = 1)
#forest = make_forest(testa[testa.objet.notnull() & testa.new_type.notnull()], 'new_type', all_mots)
#prediction = use_forest(forest, testa[testa.objet.notnull()], all_mots)
#testa['prediction_new_type'] = np.nan
#testa.loc[testa.objet.notnull(), 'prediction_new_type'] = prediction


############################################################
#def pop_from_ville(table_ville):
#    '''FAUX8FAUX8FAUX'''
#    pop = table_ville.groupby('cp').apply(lambda x: x['population'].iloc[0])
#    return pop.sum()
#
##mauvais = marches.loc[(marches.type != ' ') & (marches.type != marches.type_calcule)]
#test = marches.merge(villes, how='left', left_on='cp', right_index=True)
#test['dep'] = test['cp'].apply(lambda x: x[0:2])
#
#test.loc[test['objet_2'].isnull(), 'objet_2'] = ''
#test['objet'] = test['objet_1'] + ' ' + test['objet_2']
##
#test['destination'] = repere_ville(test, cus)
#
#
#cus_pop = [villes.loc[villes['nom_commune'] == ville.upper(), 'population'].iloc[0] for ville in cus]
#cus_rev_fisc = [villes.loc[villes['nom_commune'] == ville.upper(), 'rev_fisc_de_ref_des_foy_fisc'].iloc[0] for ville in cus]
#cus_nb_foy_fisc = [villes.loc[villes['nom_commune'] == ville.upper(), 'nb_foy_fisc'].iloc[0] for ville in cus]
#cus_nb_marches = [test['destination'].value_counts()[ville] for ville in cus]
#cus_val_marches = [test.groupby('destination')['new_seuils'].sum()[ville] for ville in cus]
#
#
### Crée une nouvelle colonne indiquant si le siège de l'entreprise est dans la CUS
#test['is_in_cus'] = test['cp'].apply(lambda x: x in cus_code_postal)
#
### Selectionner les champs avec le mot "word"
#word = 'amiante' # Has to be lower case
#def ret_sel(word):
#    return marches['objet_1'].apply(lambda x: word in x.lower()) | marches['objet_2'].apply(lambda x: word in str(x).lower())
#
#
#
#
## Compter les mots les plus usites
#a = table_des_mots.sum(axis = 1)
#a.sort(ascending = False)
#inutiles = ['de', 'la', 'des', 'du', 'strasbourg', '-', 'l', 'le', 'en', 'et', 'd', 'a', 'les', 'au', 'dans', 'pour', ':', 'au', 'une', 'un', 'sur', 'dans', 'strasbourg.', 'urbaine', 'communaute']
#selector = [not(x in inutiles) for x in a.index]
#mots_frequents = list((a[selector][:50]).index)
#
#for mot in mots_frequents:
#    attract[mot] = 0
#
#for mot in mots_frequents:
#    attract[mot] = attract['libelle'].str.contains(mot)
#    
#mots_frequents_corr = pd.DataFrame(0, index = mots_frequents, columns = mots_frequents)    
#
#for mot_x in mots_frequents:
#    print mot_x
#    for mot_y in mots_frequents:
#        mots_frequents_corr.loc[mot_x, mot_y] = sum(attract[mot_x] & attract[mot_y])
#    
#def parcours(res):
#    if len(res) == len(mots_frequents):
#        return res
#    else:
#        a = list(mots_frequents)
#        for deja in res:
#            a.remove(deja)
#        return parcours (res + [mots_frequents_corr.loc[a, res[-1]].argmax()])
#        
#
##a = marches[selector].groupby(['attributaire', 'debut_jour']).apply(len).reset_index()
##b = a.pivot('attributaire', 'debut_jour', 0) 