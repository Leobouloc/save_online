# -*- coding: utf-8 -*-
"""
Created on Wed Feb  4 10:52:09 2015

@author: debian
"""

import os
import numpy as np
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def wait_until_found(selector, max_wait):
    wait = max_wait
    while wait != 0:
        try:
            test = driver.find_element_by_id('colChiffresCles')
            test = test.find_element_by_css_selector('tbody')
            test = test.find_elements_by_css_selector('td')
            wait = 0
            return_list = [test[i].text for i in range(len(test))]
            driver.close()
            return (return_list)
        except:
            sleep(0.5)
            wait -=0.5
#    driver.close()
    return([])
        
 
def trop_de_res(localisation, adresse):
#    print 'a'
    adresse = adresse.lower()
    adresse = adresse.split(' de la ')[-1]
    adresse = adresse.split(' du ')[-1]
    adresse = adresse.split(' de ')[-1]
    adresse = adresse.split(' des ')[-1]
    adresse = adresse.split('rue ')[-1]
    adresse = adresse.split(' route ')[-1]
    adresse = adresse.split('avenue ')[-1]
    localisation = localisation + ' ' + adresse
    print 'b'
    return localisation

def pas_de_res(denomination, localisation):
    denomination = denomination.lower()
    localisation = localisation.lower()
    #denomination = denomination.replace('hotel', '')
    denomination = denomination.replace(localisation, '')
    if len(denomination) > 2:
        return  denomination
    else:
        return ''
  
def retrieve_info(driver, siret, une_boucle = None):
    max_wait = 10
    try:
        une_boucle += 1
    except:
        une_boucle = 0

    driver.get("https://www.infogreffe.fr/societes/recherche-siret-entreprise/chercher-siret-entreprise.html")
    elem = driver.find_element_by_id('p1_siren')
    elem.send_keys(siret)
    elem.send_keys(Keys.RETURN)

    wait = max_wait
    while wait != 0:
        try: ### Cas parfait
            
            test = driver.find_element_by_id('colChiffresCles')
            test = test.find_element_by_css_selector('tbody')
            test = test.find_elements_by_css_selector('td') 
            wait = 0
            return_list = [test[i].text for i in range(len(test))]
            code_naf = [[x.text for x in driver.find_elements_by_class_name('identTitreValeur') if '(CODE NAF)' in x.text][0]]
            return (return_list, code_naf)
        except:
            try:
                code_naf = [x.text for x in driver.find_elements_by_class_name('identTitreValeur') if '(CODE NAF)' in x.text][0]
                return ([], code_naf)
            except:
                pass
        try: ### Pas de résultats : il faut décontraindre
            test = driver.find_element_by_id('aucunResultatEntrepriseTrouve')
            return ([], None)
        except:
            pass
        try: ### Trop de resultats : il faut  contraintdre
            print 'what'
            test = driver.find_element_by_id('resultatsTrouvesEntreprise')
            return ([], None)

        except: 
            sleep(0.5)
            wait -=0.5
    return ([], None)


def make_table(info_and_naf):
    '''Transformer la liste en Serie Panda + corrections en int'''
    info = rewrite_list(info_and_naf[0])
    assert len(info)%4 in [0, 1]
    index = []
    values = []
    for i in range(len(info)//4):
        k= i-1
        date = info[4*k]
#        assert date[]
        index = index + ['ca_' + date[-4:], 'resultat_' + date[-4:], 'employes_' + date[-4:]]
        CA = info[4*k + 1]
        if isinstance(CA, unicode):
            if CA.count('K') == 1:
                CA = CA.replace(' K', '000')
                CA = CA.replace(' ', '')
                CA = CA[:-2]
                CA = int(CA)
            else:
                CA = CA.replace(' ', '')
                CA = CA[:-1]
                CA = int(CA)
        res = info[4*k + 2]
        if isinstance(res, unicode):
            if res.count('K') == 1:
                res = res.replace(' K', '000')
                res = res.replace(' ', '')
                res = res[:-2]
                res = int(res)   
            else:
                res = res.replace(' ', '')
                res = res[:-1]
                res = int(res)
        employes = info[4*k + 3]
        
        values = values + [CA, res, employes]
    
    try:
        print info
        code_naf = info_and_naf[1]
    except:
        code_naf = []
    index = index + ['code_naf']
    values = values + [code_naf]
    sortie = pd.Series(values, index = index)
    return sortie    


def rewrite_list(test):
    '''Transformer la liste en liste utilisable'''
    k = 0
    for i in range(len(test)):
        if isinstance(test[i+k], unicode) and (('Comptes' in test[i+k]) or ('de tenue' in test[i+k]) or ('Consulter' in test[i+k])):
                test.insert(i+k+1, np.nan)
                test.insert(i+k+2, np.nan)
                k +=2
     
    for i in range(len(test)):
        # On remplace les cases vides par des nan
        if isinstance(test[i], unicode) and str(test[i]) == '': 
            test[i] = np.nan
        # On remplace les 'Comptes annuels ...' par des nan
        if isinstance(test[i], unicode) and (('Comptes' in test[i]) or ('de tenue' in test[i]) or ('Consulter' in test[i])):
            test[i] = np.nan
    return test



def scrap_infogreffe(driver, path, range_min = 0, range_max = 5):
    
    file = os.path.join(path, 'entreprise_scrap.csv')

    entreprise_scrap = pd.read_csv(file, sep=';', header = False)

    for i in entreprise_scrap.index[range(range_min, range_max)]:
        if i%50 == 0:
            print i
        #Si on n'a pas déjà rempli cette ligne, on la remplit
        if not entreprise_scrap.iloc[i].loc['checked']:
            print i
            siret = entreprise_scrap['siret'].iloc[i]
                        
            info = retrieve_info(driver, siret)
            ligne = make_table(info)
            try:
                for col_name in ligne.index:
                    if not col_name in entreprise_scrap.columns:
                        entreprise_scrap[col_name] = None
                    entreprise_scrap.loc[i, col_name] = ligne[col_name]
            except:
                pass
            entreprise_scrap['checked'].iloc[i] = True
    entreprise_scrap.to_csv(file, sep = ';', index=False)
    return entreprise_scrap

def scrap_machine_infogreffe(path):
    driver = webdriver.Chrome(os.path.join(path, 'chromedriver'))
    '''Utilise la fonction scrap ci dessus avec des intervalles réguliers de sauvegarde '''
    for i in range(0, 60):
        scrap_infogreffe(driver, path, 5*i, 5*i+5)
    driver.close()
    
def scrap_infogreffe_for_pool(driver, path, indice):
    
    file = os.path.join(path, 'to_scrap_' + str(indice) + '.csv')

    entreprise_scrap = pd.read_csv(file, sep=';', header = False)

    for i in entreprise_scrap.index[range(len(entreprise_scrap))]:
        if i%5 == 0:
            entreprise_scrap.to_csv(file, sep = ';', index=False)
        #Si on n'a pas déjà rempli cette ligne, on la remplit
        if not entreprise_scrap.iloc[i].loc['checked']:
            print i
            siret = entreprise_scrap['siret'].iloc[i]
                        
            info = retrieve_info(driver, siret)
            ligne = make_table(info)
            try:
                for col_name in ligne.index:
                    if not col_name in entreprise_scrap.columns:
                        entreprise_scrap[col_name] = None
                    entreprise_scrap.loc[i, col_name] = ligne[col_name]
            except:
                pass
            entreprise_scrap['checked'].iloc[i] = True
    
    return entreprise_scrap    
    
    
def scrap_machine_infogreffe_for_pool(indice):
    path = '/home/debian/Documents/data/strasbourg/entreprises'
    driver = webdriver.Chrome(os.path.join(path, 'chromedriver'))
    '''Utilise la fonction scrap ci dessus avec des intervalles réguliers de sauvegarde '''
    scrap_infogreffe_for_pool(driver, path, indice)
    driver.close()
        
    
    
    
if __name__ == '__main__':
    path = '/home/debian/Documents/data/strasbourg/entreprises'
    from multiprocessing import Pool
    pool = Pool(processes = 12)
    pool.map(scrap_machine_infogreffe_for_pool,range(12))