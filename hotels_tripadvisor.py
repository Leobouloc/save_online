# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 13:59:09 2014

@author: work
"""
from hotels import load
import numpy as np
import os
import pandas as pd

from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


path = 'C:\\Users\\work\\Documents\\ETALAB_data'

#search_tag = 'Au bon coin biarritz'

    
def retrieve_info_tripadvisor(driver, search_tag):
    '''renvoie [nb_votes, nb_etoiles] pour le searchtag designe'''
    sleep_dummy = 40 #Unnecessary wait time to trick anti-scrap    
    
    max_wait_1 = 10
    max_wait_2 = 10
    
    sleep(2)
    elem = driver.find_element_by_id('mainSearch')
    elem.clear()
    elem.send_keys(search_tag)
    sleep(2)
#    elem.submit()
    elem.send_keys(Keys.RETURN)
#    elem = driver.find_element_by_name('sub-search')
    sleep(1)
#    elem.click()
    print 'a'
    wait = max_wait_1
    while wait != 0:
        try:
            elem = driver.find_element_by_id('SEARCHTAB_a')
            print 'a_prime'
            try :
                sleep(0.5)
                print 'a_double'
                elem = driver.find_element_by_id('SEARCHTAB_h')
                print 'a_triple'
                nb_hotels = int(elem.text[-2])
                print 'a_quadr'
                elem.click()
                print 'b'
                break
            except:
                sleep(sleep_dummy)
                print 'c'
                return [np.nan, np.nan]
        except:
            sleep(0.5)
            wait -=0.5
    if wait == 0:
        sleep(sleep_dummy)
        print 'd'
        return [np.nan, np.nan]
            
    if nb_hotels != 1:
        sleep(sleep_dummy)
        print 'e'
        return [np.nan, np.nan]


    wait = max_wait_2
    while wait != 0:
        try: ### Cas parfait
            elem = driver.find_element_by_css_selector('.searchResult.srLODGING.item1')
            elem = elem.find_element_by_class_name('rating')
            text = elem.text
            nb_votes = int(text.split()[0])
            etoile_elem = elem.find_element_by_class_name('sprite-ratings')
            nb_etoiles = etoile_elem.get_attribute("alt")
            nb_etoiles = nb_etoiles.split()[0]
            nb_etoiles = nb_etoiles.replace(',','.')
            nb_etoiles = float(nb_etoiles)
            print 'f'
            sleep(sleep_dummy)
            return [nb_votes, nb_etoiles]
        except:
            pass
        try: ### Pas de résultats 
            test = driver.find_element_by_class_name('searchError')
            sleep(sleep_dummy)
            print 'g'
            return [np.nan, np.nan]

        except:
            sleep(0.5)
            wait -=0.5
    
    print 'h'
    sleep(sleep_dummy)
    return [np.nan, np.nan]




def scrap_tripadvisor(driver, path, range_min = 0, range_max = 20):
    
    file = os.path.join(path, 'hotels_scrap.csv')
    hotels_scrap = pd.read_csv(file, sep=';', header = False) 
    for i in hotels_scrap.index[range(range_min, range_max)]:
        if i%50 == 0:
            print i
        #Si on n'a pas déjà rempli cette ligne, on la remplit
        if not hotels_scrap.iloc[i].loc['checked_tripadvisor']:
            denomination = hotels_scrap['NOM'].iloc[i]
            localisation = hotels_scrap['COMMUNE'].iloc[i]
            search_tag = denomination + ' ' + localisation
                        
            [nb_votes, nb_etoiles] = retrieve_info_tripadvisor(driver, search_tag)
            if nb_votes != hotels_scrap['votes_tripadvisor'].iloc[i-1] or nb_etoiles != hotels_scrap['note_tripadvisor'].iloc[i]:
                hotels_scrap['votes_tripadvisor'].iloc[i] = nb_votes            
                hotels_scrap['note_tripadvisor'].iloc[i] = nb_etoiles
                hotels_scrap['checked_tripadvisor'].iloc[i] = True
                print str(i) + ' // ' + str(nb_votes) + ' ont voté : ' + str(nb_etoiles)
            else:
                print str(i) + ' // same...'
    hotels_scrap.to_csv(file, sep = ';', index=False)
    return hotels_scrap

def scrap_machine_tripadvisor(path):
    driver = webdriver.Chrome()
    driver.get("http://www.tripadvisor.fr")
    sleep(5)
    '''Utilise la fonction scrap ci dessus avec des intervalles réguliers de sauvegarde '''
    for i in range(0, 3000):
        scrap_tripadvisor(driver, path, 5*i, 5*i+5)
    driver.close()

#driver = webdriver.Chrome()
#driver.get("http://www.tripadvisor.fr")
#scrap_tripadvisor(driver, path, range_min=0, range_max = 20)
  