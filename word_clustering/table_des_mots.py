# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 15:53:00 2015

@author: debian
"""
from multiprocessing import Pool
import thread
import time
<<<<<<< HEAD
import pandas as pd
from panda_tools import *
import itertools

path = '/home/debian/Documents/data/strasbourg'
file2 = os.path.join(path, 'CUS_CUS_AMC_MPUB2.xls')
marches_2 = pd.read_excel(file2)
marches_2.dropna(how='all', inplace=True)
marches_2.columns = ['collectivite', 'annee', 'numero', 'reconductible', 'annee_initiale', 'objet_1', 
                     'objet_2', 'mode_passation', 'num_lot', 'libelle', 'forme', 'type',
                   'attributaire', 'cp', 'siret', 'debut', 'montant_attribue', 'avenants', 'num_proc']
marches_2 = rem_whspc(marches_2)
marches_2['objet'] = marches_2.objet_1 + ' ' + marches_2.objet_2.fillna('')
=======


#path = '/home/debian/Documents/data/strasbourg'
#file2 = os.path.join(path, 'CUS_CUS_AMC_MPUB2.xls')
#marches_2 = pd.read_excel(file2)
#marches_2.dropna(how='all', inplace=True)
#marches_2.columns = ['collectivite', 'annee', 'numero', 'reconductible', 'annee_initiale', 'objet_1', 
#                     'objet_2', 'mode_passation', 'num_lot', 'libelle', 'forme', 'type',
#                   'attributaire', 'cp', 'siret', 'debut', 'montant_attribue', 'avenants', 'num_proc']
#marches_2 = rem_whspc(marches_2)
#marches_2['objet'] = marches_2.objet_1 + ' ' + marches_2.objet_2.fillna('')
>>>>>>> b56d4e0d6cd4e41294ea5764d80bb868dd0192a4



##########################################################""
## Deviner le type manquant par la frequence d'apparition

def _make_cols(phrase, all_mots):
    if isinstance(phrase, str) or isinstance(phrase, unicode):
        mots = phrase.lower().replace('.', ' ').split()
        all_mots += mots
        

def make_cols(phrase_serie):
    all_mots= []
    phrase_serie.apply(lambda x: _make_cols(x, all_mots))
    return list(set(all_mots))


<<<<<<< HEAD
def _mot_2(phrase):
=======
def _mot_2(phrase, index_table_des_mots):
>>>>>>> b56d4e0d6cd4e41294ea5764d80bb868dd0192a4
    '''sert a créer la table du nombre d occurence de chaque couple de mot'''
    global table_des_mots
#    print phrase
    mots = phrase.replace('.', ' ').split()
    mots = list(set(mots))
    mots = [mot.lower() for mot in mots]
    for point in itertools.combinations(mots, 2):
        table_des_mots.loc[point] += 1
<<<<<<< HEAD
=======
    table_des_mots_dict[index_table_des_mots] = table_des_mots

>>>>>>> b56d4e0d6cd4e41294ea5764d80bb868dd0192a4


def initiate_tab_and_slice(nb, nb_processeurs, test):
    slice_len = len(test) // nb_processeurs
    assert nb in range(nb_processeurs)
    if nb in range(nb_processeurs - 1):
        test_slice = test.iloc[range(slice_len * nb, slice_len * (nb + 1))]
        all_mots_slice = make_cols(test_slice)
        table_des_mots = pd.DataFrame(0, index = all_mots_slice, columns = all_mots_slice)
    elif nb == nb_processeurs-1:
        test_slice = test.iloc[slice_len * nb_processeurs:]
        all_mots_slice = make_cols(test_slice)
        table_des_mots = pd.DataFrame(0, index = all_mots_slice, columns = all_mots_slice)
    return [table_des_mots, test_slice]
        

<<<<<<< HEAD
def create_table(nb, test):
    global nb_processeurs
=======
def create_table(nb):
    global nb_processeurs
    global test
>>>>>>> b56d4e0d6cd4e41294ea5764d80bb868dd0192a4
    global table_des_mots
    [table_des_mots, test_slice] = initiate_tab_and_slice(nb, nb_processeurs, test)
    nb = str(nb)
    print 'Start : Thread nb : ' + nb 
<<<<<<< HEAD
    test_slice.apply(lambda phrase: _mot_2(phrase))
=======
    test_slice.apply(lambda phrase: _mot_2(phrase, nb))
>>>>>>> b56d4e0d6cd4e41294ea5764d80bb868dd0192a4
    print '>>>>> End : Thread nb : ' + nb
    table_des_mots = table_des_mots + table_des_mots.T
    return table_des_mots


test = marches_2.objet
test = test.dropna()
test = test

nb_processeurs = 12



<<<<<<< HEAD
=======
[table_des_mots_dict, test_dict] = create_dicts(12)

>>>>>>> b56d4e0d6cd4e41294ea5764d80bb868dd0192a4
t = time.time()
pool = Pool(processes = nb_processeurs) 
return_tables = pool.map(create_table, range(nb_processeurs))
print time.time() - t

def appender(list_of_tabs):
<<<<<<< HEAD
    ''' Appends elements from list of tabs (divide and conquer)'''
=======
>>>>>>> b56d4e0d6cd4e41294ea5764d80bb868dd0192a4
    if len(list_of_tabs) == 1:
        return list_of_tabs[0]
    else:
        cut = len(list_of_tabs) // 2
        list_left = list_of_tabs[:cut]
        list_right = list_of_tabs[cut:]
        return appender(list_left).append(appender(list_right))


total_tab = appender(return_tables)

total_tab.fillna(0, inplace = True)
total_tab['temp_col'] = total_tab.index
grp = total_tab.groupby('temp_col')
total_tab = grp.sum()

assert total_tab.shape[0] == total_tab.shape[1]

    
#table_des_mots = pd.DataFrame()
#for key, value in table_des_mots_dict.iteritems():
#    table_des_mots = table_des_mots.append(value)



           
    





<<<<<<< HEAD




=======
#table_des_mots_2 = table_des_mots_2 + table_des_mots_2.T
#a = table_des_mots_2.sum()
#table_des_mots_2 = table_des_mots_2.loc[a != 0, a != 0]
#a = a[a!=0]
#a = a.apply(lambda x: float(math.sqrt(x)))
#
#table_des_freq_mots_2 = table_des_mots_2.apply(lambda x: x / a)
#table_des_freq_mots_2 = table_des_freq_mots_2.apply(lambda x: x / a, axis = 1)
>>>>>>> b56d4e0d6cd4e41294ea5764d80bb868dd0192a4
#sel = table_des_mots_2.sum() > 1000
#mini_tab = table_des_freq_mots_2.loc[sel, sel]
#mini_tab.drop(a.iloc[:27].index, inplace = True)
#mini_tab.drop(a.iloc[:27].index, inplace = True, axis = 1)
