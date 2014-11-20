# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 11:24:40 2014

@author: work
"""
import hotels

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
  
def retrieve_info(driver, denomination, localisation, adresse, une_boucle = None):
    max_wait = 10
    try:
        une_boucle += 1
    except:
        une_boucle = 0

    driver.get("https://www.infogreffe.fr/societes/recherche-siret-entreprise/chercher-siret-entreprise.html")
    elem = driver.find_element_by_id('p1_deno')
    elem.send_keys(denomination)
    elem = driver.find_element_by_id('localisation')
    elem.send_keys(localisation)
#    elem = driver.find_element_by_name('familleActivite')
#    elem.send_keys("55")
    elem.send_keys(Keys.RETURN)
    
    wait = max_wait
    while wait != 0:
        try: ### Cas parfait
            test = driver.find_element_by_id('colChiffresCles')
            test = test.find_element_by_css_selector('tbody')
            test = test.find_elements_by_css_selector('td')
            wait = 0
            return_list = [test[i].text for i in range(len(test))]
#            driver.close()
            return (return_list)
        except:
            pass
        try: ### Pas de résultats : il faut décontraindre
            test = driver.find_element_by_id('aucunResultatEntrepriseTrouve')
            return []
#            if test != '':
#                denomination = pas_de_res(denomination, localisation)
#                print 'pas_de_res'
#                if une_boucle < 1:
#                    return retrieve_info(driver, denomination, localisation, 'adresse', une_boucle)
#                else:
#                    return([])
##                driver.close()
        except:
            pass
        try: ### Trop de resultats : il faut  contraintdre
#            print 'what'
            test = driver.find_element_by_id('resultatsTrouvesEntreprise')
            return []
#            print 'now'
#            if test != '':
#                localisation = trop_de_res(localisation, adresse)
#                print une_boucle
#                if une_boucle < 1:
#                    return retrieve_info(driver, denomination, localisation, adresse, une_boucle)
#    #                    driver.close()
#                else:
#                    return([])
        except: 
            sleep(0.5)
            wait -=0.5

    return([])
    
def make_table(info):
    '''Transformer la liste en Serie Panda + corrections en int'''
    info = rewrite_list(info)
    assert len(info)%4 == 0
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
    
    file = os.path.join(path, 'hotels_scrap.csv')
    hotels_scrap = pd.read_csv(file, sep=';', header = False) 
    for i in hotels_scrap.index[range(range_min, range_max)]:
        if i%50 == 0:
            print i
        #Si on n'a pas déjà rempli cette ligne, on la remplit
        if not hotels_scrap.iloc[i].loc['checked']:
            print i
            denomination = hotels_scrap['NOM'].iloc[i]
            localisation = hotels_scrap['COMMUNE'].iloc[i]
            adresse = hotels_scrap['ADRESSE'].iloc[i]
                        
            info = retrieve_info(driver, denomination, localisation, adresse)
            ligne = make_table(info)
            try:
                for col_name in ligne.index:
                    if not col_name in hotels_scrap.columns:
                        hotels_scrap[col_name] = None
                    hotels_scrap.loc[i, col_name] = ligne[col_name]
            except:
                pass
            hotels_scrap['checked'].iloc[i] = True
    hotels_scrap.to_csv(file, sep = ';', index=False)
    return hotels_scrap

def scrap_machine_infogreffe(path):
    driver = webdriver.Chrome()
    '''Utilise la fonction scrap ci dessus avec des intervalles réguliers de sauvegarde '''
    for i in range(1800, 3000):
        scrap_infogreffe(driver, path, 5*i, 5*i+5)
    driver.close()