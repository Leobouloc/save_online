# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 12:28:18 2015

@author: leo_cdo_intern

Scrap du site de meteo France.

Info : integer correspond toujours au nombre associe à une commune (visible 
dans l'url après une recherche)

"""
import requests
from bs4 import BeautifulSoup
from os.path import join
import os
import pandas as pd
import time
import datetime


# Utile pour le multiprocessing (prbl avec Windows)
#from multiprocessing import cpu_count
#from multiprocessing import Pool


def get_page(dep, integer, date, return_list = True):
    '''Renvoie une liste d infos si la page est trouvee, false sinon'''
    integer = str(integer).zfill(3)
    dep = str(dep).zfill(2) 
    
    page = requests.get('http://www.meteofrance.com/climat/meteo-date-passee?lieuId=' + str(dep) + str(integer) + '0&lieuType=VILLE_FRANCE&date=' + date)
    data = page.text
    soup = BeautifulSoup(data)     
      
    valid_code = 'style' in soup.find('div', {'id':'alertMessage'}).attrs
    if valid_code:
        zone_meteo = soup.find('div', {'class':'mod-article-wysiwyg wysiwyg-style-2 article-commentaire'})    
        
        info_mesure = zone_meteo.find('div', {'class':'mod-header'}).text
        ville = info_mesure.split(u'à')[-1]
        meteo = zone_meteo.find('ul')
        
        temp_min = zone_meteo.find('ul').find_all('li')[0].text.split(': ')[-1]
        temp_min = temp_min.replace(u'°C', '')
        
        temp_max = zone_meteo.find('ul').find_all('li')[1].text.split(': ')[-1]
        temp_max = temp_max.replace(u'°C', '')
        
        ensoleillement = zone_meteo.find('ul').find_all('li')[2].text.split(': ')[-1]
        ensoleillement = ensoleillement.replace('h', '')    
        
        precipitations = zone_meteo.find('ul').find_all('li')[3].text.split(': ')[-1]
        precipitations = precipitations.replace('mm', '')
        
        if return_list:
            return [ville, dep, integer, date, temp_min, temp_max, ensoleillement, precipitations]
        else:
            table_index = ['ville', 'integer', 'date', 'temp_min', 'temp_max', 'ensoleillement', 'precipitations']
            return pd.Series([ville, dep, integer, date, temp_min, temp_max, ensoleillement, precipitations], index = table_index)
    else:
        return valid_code
        


def initiate(path, num_cores):
    '''Initiates csv file with index num_cores'''
    table_index = ['ville', 'dep', 'integer', 'date', 'temp_min', 'temp_max', 'ensoleillement', 'precipitations']
    for i in range(num_cores):
        if not ('table_meteo_' + str(i) + '.csv') in os.listdir(path):
            f = open(join(path, 'table_meteo_' + str(i) + '.csv'), 'w')
            for col in table_index[:-1]:
                f.write(col + ';')
            f.write(table_index[-1] + '\n')
            f.close()
            print 'La table numero', i, 'a ete crée'
        else:
            print 'La table numero', i, 'n a pas ete crée'
            


def get_all(path, liste_a_faire, indice, num_cores):
    """Recupere toutes les dans les infos dans liste_a_faire et ecrit dans path"""
    try:
        # Si la table n'existe pas encore, on l'initialise
        try:
            if not ('table_meteo_' + str(indice) + '.csv') in os.listdir(path):
                initiate(path, num_cores)
            
            f = open(join(path, 'table_meteo_' + str(indice) + '.csv'), 'a')
        except:
            e = 'Problem while creating or opening file. Make sure it is not open in Excel'
            print e
            raise Exception(e)
        
        for (integer, dep, date) in liste_a_faire:
            for i in range(10):
                try:
                    retour = get_page(dep, integer, date, return_list = True)  
                    print retour
#                    print 'no error in retour', integer, dep, date
                    if not isinstance(retour, bool):
                        if len(retour) == 8:
                            for col in retour[:-1]:
                                f.write(col.encode('utf8') + ';')
        #                        print 'no problem with col', col, integer, dep, date
                            f.write(retour[-1] + '\n')
                            print retour
                        print dep, integer, date, 'had missing values'
                    else:
                        print dep, integer, date, 'had no values'
                    break
                except Exception, e:
                    print dep, integer, date, 'was passed ...'
                    print '   >>>', str(e)
                    time.sleep(30)
        'Process', indice, 'is finished'
    except:
        print Exception
        f.close()
        print 'Terminated process', indice,'before end. FILE CLOSED'

    
#def get_all_for_pool_2(indice):
##    path = '/home/debian/Documents/data/meteo'
#    print "get_all started for process : ", indice
#    path = 'C:\\Users\\work\\Documents\\ETALAB_data\\meteo'
#    csv_name = 'meteo.csv'
#    num_cores = cpu_count()
#    table = load_global(path, 12)
#    
#    # Preparation des dates
#    base = datetime.datetime(2009, 1, 1)
#    liste_des_dates = [base + datetime.timedelta(days=x) for x in range(0, 2200)]
#    liste_des_dates = [date.strftime('%d-%m-%Y') for date in liste_des_dates]
##    liste_des_dates = [str(jour) + '-' + str(mois) + '-' + str(annee) for annee in range(2009,2015) for mois in range(1,13) for jour in range(1,32)]
#    a_faire =  table.groupby(['dep', 'integer'])['date'].apply(lambda x: [date for date in liste_des_dates \
#                                                                if not(date in list(x))]).reset_index()
#    a_faire_list = [(a_faire['integer'].iloc[i], a_faire['dep'].iloc[i], date) \
#                    for i in range(len(a_faire)) for date in a_faire['date'].iloc[i]]    
#    len_for_threading = len(a_faire_list) // num_cores
#    liste_a_faire_list = [a_faire_list[i*len_for_threading:(i+1)*len_for_threading] for i in range(num_cores)]
#    get_all_2(path, liste_a_faire_list[indice], indice)
        
    
    
#def load_partial_table(path, indice, to_correct = False):
#    table = pd.read_csv(join(path, 'table_meteo_' + str(indice) + '.csv'), sep = ';')
#    return table


#def load_global(path, num_cores):
#    table = pd.DataFrame()
#    for i in range(num_cores):
#        tab = load_partial_table(path, i)
#        table = table.append(tab)
#    table['date'] = table.date.apply(lambda date: '-'.join([date.split('-')[0].zfill(2), date.split('-')[1].zfill(2), date.split('-')[2]]))
#    return table
    
    
    
if __name__ == '__main__':
    # !!! A FAIRE : génerer ou rentrer à la main la liste des variables "integer" et "dep"
    # associées aux villes souhaitées.
    # Je n'ai pas gardé le script de recherche.    
    
    
    ### PARAMETRES
    # path d'ecriture
    path = 'C:\\Users\\work\\Documents\\Python_data\\meteo'
    # Date debut de scrap
    annee_debut = 2009
    nombre_de_jours = 2200
    liste_de_villes = (['471', '91'], ['066', '93']) # format : [integer, dep]
    num_cores = 1
    ### FIN PARAMETRES
    

#    num_cores = cpu_count()
    
  # Preparation des dates
    base = datetime.datetime(annee_debut, 1, 1)
    liste_des_dates = [base + datetime.timedelta(days=x) for x in range(0, nombre_de_jours)]
    liste_des_dates = [date.strftime('%d-%m-%Y') for date in liste_des_dates]
#    len_for_threading = len(liste_des_dates) // num_cores
    
#    table = load_global(path, num_cores)
#    grp = table.groupby(['dep', 'integer', 'ville', 'date'])
#    new_table = grp.apply(lambda x: x.iloc[0])
#    new_table = new_table.drop(['ville', 'dep', 'integer', 'date'], axis = 1).reset_index()        
    
#    table_ref = pd.read_csv(join(path, 'table_ref.csv'), sep = ';')
#    table_ref = table_ref.groupby('dep').apply(lambda x: x.iloc[0])
#    table_ref['dep'] = range(1, 1+ len(table_ref))
   
    try:
        table = pd.read_csv(join(path, 'table_meteo_' + str(0) + '.csv'), sep = ';')   
       
        a_faire =  table.groupby(['dep', 'integer'])['date'].apply(lambda x: [date for date in liste_des_dates if not(date in list(x))]).reset_index()
        a_faire_list = [(a_faire['integer'].iloc[i], a_faire['dep'].iloc[i], date) for i in range(len(a_faire)) for date in a_faire['date'].iloc[i]]
    
    except:
        a_faire_list = [(liste_de_villes[i][0], liste_de_villes[i][1], date) for i in range(len(liste_de_villes)) for date in liste_des_dates]
      
    
#    print 'Il reste :', len(a_faire_list), 'lignes à faire'
#    len_for_threading = len(a_faire_list) // num_cores
#    liste_a_faire_list = [a_faire_list[i*len_for_threading:(i+1)*len_for_threading] for i in range(num_cores)]
#    liste_liste_des_dates = [liste_des_dates[i*len_for_threading:(i+1)*len_for_threading] for i in range(num_cores)]

#    # Preparations des variables integer

    get_all(path, a_faire_list, indice = 0, num_cores = num_cores)
    
##    initiate(path, num_cores)
#    pool = Pool(processes = num_cores)
#    pool.map(get_all_for_pool_2,range(num_cores))  

