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

path = 'C:\\Users\\work\\Documents\\ETALAB_data'
file = os.path.join(path, 'strasbourg_marches_pub.csv')
file2 = os.path.join(path, 'strasbourg_stats_attractivite.csv')

marches = pd.read_csv(file, sep=';')
marches.dropna(how='all', inplace=True)
marches.columns = ['collectivite', 'annee', 'numero', 'objet_1', 'objet_2', 'type',
                   'attributaire', 'cp', 'debut', 'seuils']


attract = pd.read_csv(file2, sep=';')
attract.dropna(how='any', inplace=True)
attract.columns = ['code', 'num_procedure', 'num_dossier', 'libelle', 'type',
                   'date_lim_recep', 'nb_lots', 'nb_depots']

new_seuils = [10000, 50000, 0.1 * 10**6, 10**6, 5*10**6]
#new_seuils = ['+ 4 000', '+ de 20 000', '+ de 90 000', '+ de 200 000', '+ de 2M']
type_names = ['Travaux', 'Services', 'Fournitures']


# TODO : on trouve également STBG
cus = ['Bischheim', 'Blaesheim', 'Eckbolsheim', 'Eckwersheim', 'Entzheim',
        'Eschau', 'Fegersheim', 'Geispolsheim', 'Hoenheim', 'Holtzheim',
        'Illkirch-Graffenstaden', 'Lampertheim', 'La Wantzenau', 'Lipsheim',
        'Lingolsheim', 'Mittelhausbergen', 'Mundolsheim', 'Niederhausbergen',
        'Oberhausbergen', 'Oberschaeffolsheim', 'Ostwald', 'Plobsheim',
        'Reichstett', 'Schiltigheim', 'Souffelweyersheim', 'Strasbourg',
        'Vendenheim']
        


def to_serie(string):
    return pd.Series([villes.loc[villes['nom_commune'] == ville.upper(), string].iloc[0] for ville in cus])

# Renvoie le code insee et postal pour lesvilles ci dessus
#cus_code_insee = [villes.insee_code[villes.nom_comm == ville.upper()].iloc[0] for ville in cus]
#cus_code_postal = [villes.postal_code[villes.nom_comm == ville.upper()].iloc[0] for ville in cus]


def repere_ville(table, cus):
    '''Trouve le nom de ville dans le libelle et le place dans le champ ville'''
    def lambda_func(ligne, cus):
        libelle_1 = ligne['objet_1']
        libelle_2 = ligne['objet_2']
        list_villes = []
        for ville in cus:
            if ville == 'Strasbourg':
                if (ville.lower() in libelle_1.lower()) or ('stbg' in libelle_1.lower()):
                    list_villes = list_villes + [ville]
                if isinstance(libelle_2, str):
                    if (ville.lower() in libelle_2.lower()) or ('stbg' in libelle_2.lower()):
                        list_villes = list_villes + [ville]                
            else:
                if ville.lower() in libelle_1.lower():
                    list_villes = list_villes + [ville]
                if isinstance(libelle_2, str):
                    if ville.lower() in libelle_2.lower():
                        list_villes = list_villes + [ville]
        if len(set(list_villes)) == 1:
            return list_villes[0]
        else:
            return np.nan
    return table.apply(lambda ligne: lambda_func(ligne, cus), axis = 1)


for [table, champ] in  [[attract, 'libelle'], [marches, 'objet_1']]: #, [marches, 'objet_2']]:
    print 'reecriture'
    table[champ] = table[champ].apply(lambda x: x.replace('\xd6', 'O'))  # Ô
    table[champ] = table[champ].apply(lambda x: x.replace('\xf6', 'o'))  # ô
    table[champ] = table[champ].apply(lambda x: x.replace('\xd4', 'O'))  # Ö
    table[champ] = table[champ].apply(lambda x: x.replace('\xf4', 'o'))  # ö
    table[champ] = table[champ].apply(lambda x: x.replace('\xcf', 'I'))  # Ï
    table[champ] = table[champ].apply(lambda x: x.replace('\xef', 'i'))  # ï
    table[champ] = table[champ].apply(lambda x: x.replace('\xcb', 'E'))  # Ë
    table[champ] = table[champ].apply(lambda x: x.replace('\xeb', 'e'))  # ë
    table[champ] = table[champ].apply(lambda x: x.replace('\xc7', 'e'))  # Ç
    table[champ] = table[champ].apply(lambda x: x.replace('\xeb', 'e'))  # ç
    table[champ] = table[champ].apply(lambda x: x.replace('\xc8', 'E'))  # È
    table[champ] = table[champ].apply(lambda x: x.replace('\xe8', 'e'))  # è
    table[champ] = table[champ].apply(lambda x: x.replace('\xc9', 'E'))  # É
    table[champ] = table[champ].apply(lambda x: x.replace('\xe9', 'e'))  # é
    table[champ] = table[champ].apply(lambda x: x.replace('\xce', 'I'))  # Î
    table[champ] = table[champ].apply(lambda x: x.replace('\xee', 'i'))  # î
    table[champ] = table[champ].apply(lambda x: x.replace('\xc0', 'A'))  # À
    table[champ] = table[champ].apply(lambda x: x.replace('\xe0', 'a'))  # à
    table[champ] = table[champ].apply(lambda x: x.replace('\xca', 'E'))  # Ê
    table[champ] = table[champ].apply(lambda x: x.replace('\xea', 'e'))  # ê
    table[champ] = table[champ].apply(lambda x: x.replace('\xc2', 'A'))  # Â
    table[champ] = table[champ].apply(lambda x: x.replace('\xe2', 'a'))  # â
    table[champ] = table[champ].apply(lambda x: x.replace("'", ' '))  # '
    table[champ] = table[champ].apply(lambda x: x.replace('\xae', ''))  # ®
    table[champ] = table[champ].apply(lambda x: x.replace('\xce', ''))  # ??????
    table[champ] = table[champ].apply(lambda x: x.replace('\xdb', 'U'))  # Û
    table[champ] = table[champ].apply(lambda x: x.replace('\xfb', 'u'))  # û
    table[champ] = table[champ].apply(lambda x: x.replace('\xfc', 'u'))  # û
    table[champ] = table[champ].apply(lambda x: x.replace('\xdc', 'U'))  # û
    table[champ] = table[champ].apply(lambda x: x.replace('\x92', ' '))  # '
    table[champ] = table[champ].apply(lambda x: x.replace('\xb0', ' '))  # °
    table[champ] = table[champ].apply(lambda x: x.lower())


def rewrite_seuil(seuil):
    if unicode(seuil) == u'Marchés de 4 000 à 19 999,99 euros HT':
        return new_seuils[0]
    elif unicode(seuil) == u'Marchés de 20 000 à 89 999,99 euros HT':
        return new_seuils[1]
    elif unicode(seuil) == u'Marchés de 90 000 à 199 999,99 euros HT':
        return new_seuils[2]
    elif unicode(seuil) == u'Marchés de 200 000 à 5 000 000 euros HT':
        return new_seuils[3]
    elif unicode(seuil) == u'Marchés de 5 000 000 euros HT et plus':
        return new_seuils[4]


def rewrite_debut_mois(date):
    if isinstance(date, str):
        new_date = date[6:10] + date[3:5]
        return datetime.datetime.strptime(new_date, "%Y%m")
    else:
        return np.nan


def rewrite_debut_an(date):
    if isinstance(date, str):
        new_date = date[6:10]
        return datetime.datetime.strptime(new_date, "%Y")
    else:
        return np.nan


def rewrite_debut_jour(date):
    if isinstance(date, str):
        new_date = date[:4] + date[5:7] + date[8:]
        return new_date
    else:
        return np.nan


marches.loc[:, 'new_seuils'] = marches['seuils'].apply(rewrite_seuil)
marches.loc[:, 'debut_mois'] = marches['debut'].apply(rewrite_debut_mois)
marches.loc[:, 'debut_an'] = marches['debut'].apply(rewrite_debut_an)
marches.loc[:, 'debut_jour'] = marches['debut'].apply(rewrite_debut_jour)


'''Plot des marchés débutant mensuellement par catégorie de prix'''
#a = marches.groupby('type')['debut_mois'].value_counts()
#for x in type_names:
#    b = a[x].sort_index()
#    plt.plot(b.index, b, label = str(x))
#    plt.xlabel(u"Début d'éxecution du marché")
#    plt.ylabel(u'Nombre de contrats débutant dans le mois')
#    plt.title(u'Nombre de contrats débutant chaque mois passés dans la CUS et VDS')
#    plt.legend()
#plt.show()

#    b = b/b.mean() # On normalise pour repérere les saisonnalités

'''Plot des marchés débutant annuellement par catégorie de prix'''
#a = marches.groupby('new_seuils')['debut_an'].apply(lambda x: value_counts(x).sort_index())
#for x in new_seuils[:4]:
#    b = a[x].sort_index()
#    plt.plot(b.index, b, label = str(int(x)))
#    plt.legend()
#plt.show()

'''Pourcentage d'offres fermées avec un seul concurrent par type'''
#attract.groupby(['code','type']).apply(lambda x: sum(x['nb_depots']<2) / float(len(x))) * 100




def lambda_mot(table_des_mots, ligne):
    print ligne['num_procedure']
    cat_mot = ligne['type']
    mots = ligne['libelle'].split()[1:]
    for mot in mots:
        mot = mot.replace("d'", '')
        mot = mot.lower()
        if mot in list(table_des_mots.index):
            table_des_mots.loc[mot, cat_mot] += 1
        else:
            table_des_mots.loc[mot, :] = 0
            table_des_mots.loc[mot, :cat_mot] = 1
    return table_des_mots

'''Création d'un lexique pour classer les descriptions dans marché'''



try:
    file = os.path.join(path, 'table_des_mots.csv')
    table_des_mots = pd.load_csv(file)
except:
    table_des_mots = pd.DataFrame(columns = ['Travaux', 'Services', 'Fournitures'])
    attract.apply(lambda ligne: lambda_mot(table_des_mots, ligne), axis = 1)
    table_des_freq_mots = table_des_mots / table_des_mots.sum()
    file = os.path.join(path, 'table_des_mots.csv')
    table_des_mots.to_csv(file, sep = ';')


def caract_phrase(table_des_freq_mots, ligne):
    '''a partir de la table_des_freq_mots, détermine le type '''
    mots = ligne['objet_1'].split()
    p_trav = 1
    p_serv = 1
    p_fourn = 1
    count = 0
    for mot in mots:
        if mot in list(table_des_freq_mots.index):
            count += 1
            p_trav *= table_des_freq_mots.loc[mot, 'Travaux']
            p_serv *= table_des_freq_mots.loc[mot, 'Services']
            p_fourn *= table_des_freq_mots.loc[mot, 'Fournitures']
    maximum = max(p_trav, p_serv, p_fourn)
    print 'nb_mots en commun : ' + str(count)
    print (p_trav, p_serv, p_fourn)
    ligne['p_trav'] = p_trav
    ligne['p_serv'] = p_serv
    ligne['p_fourn'] = p_fourn
    ligne['count'] = count
    if maximum == p_trav:
        ligne['type_calcule'] = "Travaux"
    elif maximum == p_serv:
        ligne['type_calcule'] = "Services"
    elif maximum == p_fourn:
        ligne['type_calcule'] = "Fournitures"
    return ligne

#marches = marches.apply(lambda x: caract_phrase(table_des_freq_mots, x), axis = 1)

def pop_from_ville(table_ville):
    '''FAUX8FAUX8FAUX'''
    pop = table_ville.groupby('cp').apply(lambda x: x['population'].iloc[0])
    return pop.sum()

#mauvais = marches.loc[(marches.type != ' ') & (marches.type != marches.type_calcule)]
test = marches.merge(villes, how='left', left_on='cp', right_index=True)
test['dep'] = test['cp'].apply(lambda x: x[0:2])

test.loc[test['objet_2'].isnull(), 'objet_2'] = ''
test['objet'] = test['objet_1'] + ' ' + test['objet_2']
#
test['destination'] = repere_ville(test, cus)


cus_pop = [villes.loc[villes['nom_commune'] == ville.upper(), 'population'].iloc[0] for ville in cus]
cus_rev_fisc = [villes.loc[villes['nom_commune'] == ville.upper(), 'rev_fisc_de_ref_des_foy_fisc'].iloc[0] for ville in cus]
cus_nb_foy_fisc = [villes.loc[villes['nom_commune'] == ville.upper(), 'nb_foy_fisc'].iloc[0] for ville in cus]
cus_nb_marches = [test['destination'].value_counts()[ville] for ville in cus]
cus_val_marches = [test.groupby('destination')['new_seuils'].sum()[ville] for ville in cus]


## Crée une nouvelle colonne indiquant si le siège de l'entreprise est dans la CUS
test['is_in_cus'] = test['cp'].apply(lambda x: x in cus_code_postal)

## Selectionner les champs avec le mot "word"
word = 'amiante' # Has to be lower case
def ret_sel(word):
    return marches['objet_1'].apply(lambda x: word in x.lower()) | marches['objet_2'].apply(lambda x: word in str(x).lower())



# Compter les mots les plus usites
a = table_des_mots.sum(axis = 1)
a.sort(ascending = False)
inutiles = ['de', 'la', 'des', 'du', 'strasbourg', '-', 'l', 'le', 'en', 'et', 'd', 'a', 'les', 'au', 'dans', 'pour', ':', 'au', 'une', 'un', 'sur', 'dans', 'strasbourg.', 'urbaine', 'communaute']
selector = [not(x in inutiles) for x in a.index]
mots_frequents = list((a[selector][:50]).index)

for mot in mots_frequents:
    attract[mot] = 0

for mot in mots_frequents:
    attract[mot] = attract['libelle'].str.contains(mot)
    
mots_frequents_corr = pd.DataFrame(0, index = mots_frequents, columns = mots_frequents)    

for mot_x in mots_frequents:
    print mot_x
    for mot_y in mots_frequents:
        mots_frequents_corr.loc[mot_x, mot_y] = sum(attract[mot_x] & attract[mot_y])
    
def parcours(res):
    if len(res) == len(mots_frequents):
        return res
    else:
        a = list(mots_frequents)
        for deja in res:
            a.remove(deja)
        return parcours (res + [mots_frequents_corr.loc[a, res[-1]].argmax()])
        

#a = marches[selector].groupby(['attributaire', 'debut_jour']).apply(len).reset_index()
#b = a.pivot('attributaire', 'debut_jour', 0) 