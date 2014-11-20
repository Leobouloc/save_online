# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 15:53:59 2014

@author: work
"""

#import re
import pandas as pd
import os
import numpy as np
import numpy
#from mechanize import Browser

import hotels_infogreffe

from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import matplotlib.pyplot as plt

### NOTES:
#Regarder le CA par employé
#Normaliser par an le CA et res

path = 'C:\\Users\\work\\Documents\\ETALAB_data'

denomination = 'Le clos joli'
localisation = 'BAGNOLES-DE-L ORNE'

infos = ["DATE DE CLASSEMENT", "DATE DE PUBLICATION DE L'ETABLISSEMENT",
               "TYPOLOGIE ÉTABLISSEMENT", "CLASSEMENT", "CATÉGORIE", "MENTION",
               "NOM COMMERCIAL", "ADRESSE", "CODE POSTAL", "COMMUNE", "TÉLÉPHONE",
               "COURRIEL", "SITE INTERNET", "TYPE DE SÉJOUR", "CAPACITÉ D'ACCUEIL (PERSONNES)",
             "NOMBRE DE CHAMBRES", "NOMBRE D'EMPLACEMENTS", "NOMBRE D'UNITES D'HABITATION",
             "NOMBRE DE LOGEMENTS"]
             
infos_utiles= [u"DATE_DE_CLASSEMENT", u"DATE_DE_PUBLICATION",
               u"TYPOLOGIE", u"CLASSEMENT", u"NOM", 
               u"ADRESSE", u"CODE_POSTAL", u"COMMUNE", u"TELEPHONE",
               u"SITE_INTERNET",  u"CAPACITE",
             u"NOMBRE_DE_CHAMBRES"]

period = [2009, 2010, 2011, 2012, 2013, 2014]
period = [2010, 2011, 2012, 2013]
employes = ['employes_' + str(date) for date in period]
ca = ['ca_' + str(date) for date in period]
resultat = ['resultat_' + str(date) for date in period]

infos_utiles = [x.replace(' ', '_') for x in infos_utiles]
infos_utiles = [x.replace("'", '_') for x in infos_utiles]
infos_utiles = [str(x) for x in infos_utiles]


def load(path):
    file = os.path.join(path, 'hotels_scrap.csv')
    table = pd.read_csv(file, sep=';', header = False)
    return table
    
def rewrite(path, table):
    file = os.path.join(path, 'hotels_scrap.csv')
    table.to_csv(file, sep = ';', index=False)    
    
def save_copy(path):
    file = os.path.join(path, 'hotels_scrap.csv')
    table = pd.read_csv(file, sep=';', header = False)
    file = os.path.join(path, 'hotels_scrap_save.csv')
    table.to_csv(file, sep = ';', index=False)

def load_hotels(path, infos_utiles):
    file = os.path.join(path, 'hotels_scrap.csv')
    table = pd.read_csv(file, sep=';', header = False)
    table.columns = [x.replace(' ', '_') for x in table.columns]
    table.columns = [x.replace("'", '_') for x in table.columns]
    table.columns = [x.replace(u'É', 'E') for x in table.columns]
    table = table.replace('-', np.nan)
    
    table.columns = [rename_columns(x) for x in table.columns]
    table = table.loc[:,infos_utiles]
    
    print 'yes'
    for champ in ['NOM', 'COMMUNE']:
        table[champ] = table[champ].apply(lambda x: x.replace('\xd6', 'O')) #Ô
        table[champ] = table[champ].apply(lambda x: x.replace('\xf6', 'o')) #ô
        table[champ] = table[champ].apply(lambda x: x.replace('\xd4', 'O')) #Ö
        table[champ] = table[champ].apply(lambda x: x.replace('\xf4', 'o')) #ö    
        table[champ] = table[champ].apply(lambda x: x.replace('\xcf', 'I')) #Ï
        table[champ] = table[champ].apply(lambda x: x.replace('\xef', 'i')) #ï
        table[champ] = table[champ].apply(lambda x: x.replace('\xcb', 'E')) #Ë
        table[champ] = table[champ].apply(lambda x: x.replace('\xeb', 'e')) #ë
        table[champ] = table[champ].apply(lambda x: x.replace('\xc7', 'e')) #Ç
        table[champ] = table[champ].apply(lambda x: x.replace('\xeb', 'e')) #ç     
        table[champ] = table[champ].apply(lambda x: x.replace('\xc8', 'E')) #È  
        table[champ] = table[champ].apply(lambda x: x.replace('\xe8', 'e')) #è
        table[champ] = table[champ].apply(lambda x: x.replace('\xc9', 'E')) #É
        table[champ] = table[champ].apply(lambda x: x.replace('\xe9', 'e')) #é
        table[champ] = table[champ].apply(lambda x: x.replace('\xce', 'I')) #Î
        table[champ] = table[champ].apply(lambda x: x.replace('\xee', 'i')) #î
        table[champ] = table[champ].apply(lambda x: x.replace('\xc0', 'A')) #À
        table[champ] = table[champ].apply(lambda x: x.replace('\xe0', 'a')) #à
        table[champ] = table[champ].apply(lambda x: x.replace('\xca', 'E')) #Ê
        table[champ] = table[champ].apply(lambda x: x.replace('\xea', 'e')) #ê
        table[champ] = table[champ].apply(lambda x: x.replace('\xc2', 'A')) #Â
        table[champ] = table[champ].apply(lambda x: x.replace('\xe2', 'a')) #â        
        table[champ] = table[champ].apply(lambda x: x.replace("'", ' ')) #'
        table[champ] = table[champ].apply(lambda x: x.replace('\xae', '')) # ®
        table[champ] = table[champ].apply(lambda x: x.replace('\xce', '')) #  ??????      
        table[champ] = table[champ].apply(lambda x: x.replace('\xdb', 'U')) # Û
        table[champ] = table[champ].apply(lambda x: x.replace('\xfb', 'u')) # û
        table[champ] = table[champ].apply(lambda x: x.replace('\xfc', 'u')) # û    
        table[champ] = table[champ].apply(lambda x: x.replace('\xdc', 'U')) # û   
        table[champ] = table[champ].apply(lambda x: x.replace('\x92', ' ')) # '
        table[champ] = table[champ].apply(lambda x: x.replace('\xb0', ' ')) # °
        return table
    
def rename_columns(string):
    if string == 'DATE_DE_PUBLICATION_DE_L_ETABLISSEMENT':
        return 'DATE_DE_PUBLICATION'
    elif string == 'TYPOLOGIE_ETABLISSEMENT':
        return 'TYPOLOGIE'
    elif string == 'NOM_COMMERCIAL':
        return 'NOM'
    elif string == 'CAPACITE_D_ACCUEIL_(PERSONNES)':
        return 'CAPACITE' 
    else:
        return string    
    
'''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''    
    



def categorize(x, n, quantiles):
    for i in range(1, n):
        if x < quantiles.iloc[i]:
            return(i)
    return(n)

h = load(path)

selector = h[ca].apply(lambda x: sum(x.notnull()) >= 3, axis = 1)
h=h[selector]
selector = h[employes].apply(lambda x: sum(x.notnull()) >= 2, axis = 1)
h=h[selector]



def metriques(h):
    ca_moy = h[ca].mean(axis=1)
    res_moy = h[resultat].mean(axis=1)
    chambres = h['NOMBRE_DE_CHAMBRES']
    capacite = h['CAPACITE']
    employes_moy = h[employes].mean(axis = 1)
    etoile = h['CLASSEMENT'].apply(lambda x: int(x[0]))
    donnees = 'chambres, capacite, ca, resultat_moy, ca_moy, employes_moy, etoiles'
    
    res_sur_ca = res_moy/ca_moy
    h['res_sur_ca'] = res_sur_ca 
    n=int(6) 
    quantiles = res_sur_ca.quantile([1/float(n) * float(i) for i in range(0, int(n))])
    res_cat = res_sur_ca.apply(lambda x: categorize(x, n, quantiles))
    return [ca_moy, res_moy, chambres, capacite, employes_moy, etoile, donnees,
            res_sur_ca, res_cat]

[ca_moy, res_moy, chambres, capacite, employes_moy, etoile, donnees, res_sur_ca, res_cat] = metriques(h)

def get_dep(x):
    if len(str(x)) == 5:
        return str(x)[:2]
    else:
        return np.nan
        
h['dep'] = h['CODE_POSTAL'].apply(get_dep)
   
#br.set_handle_robots(False)
        
#br = Browser()
#r = br.open("https://www.infogreffe.fr/societes/recherche-siret-entreprise/chercher-siret-entreprise.html")
#br.select_form(nr = 1)
## Browser passes through unknown attributes (including methods)
## to the selected HTMLForm (from ClientForm).
#br.form["localisation"] = 'Biarritz'  
#br.form["deno"] = 'au bon coin'
##br.click(id='boutonRechercherEntreprise')
##sleep(0.3)
#br.submit()
#br.response = br.submit()  # submit current form