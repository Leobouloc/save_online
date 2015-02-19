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







tab_string = '''cp	montant_attribue
67000	89983593
67000	108526
67000	29373
67000	602000
67000	1454267
67000	264000
67000	855854
67000	3182861
67000	4101
67000	570488
67000	4235373
67000	13462450
67000	133850
67000	1075332
67000	2280524
67000	1368500
67000	60000
67000	3490054
67000	718100
67000	387191
67000	817894
67000	29120
67000	6872
67000	50000
67000	109487
67000	680000
67000	20728000
67000	1594178
67000	212350
67000	101878
67000	821685
67000	3617905
67000	489994
67000	168000
67000	23733
67100	181425275
67110	10890593
67114	23401898
67115	217525
67116	12913238
67117	1736819
67118	29608701
67360	203967
67120	30824778
67120	7174
67120	3936156
67120	3399706
67130	7355801
67130	77229
67140	4905545
67150	27576922
67150	24393107
67160	7200
67170	21192243
67170	5690007
67170	120000
67170	246466
67190	2542223
67200	33418925
67201	9562990
67202	17008818
67203	5750000
67204	8216473
67205	7136834
67207	4188734
67210	3626305
67210	45038
67220	3491545
67210	523102
67230	14877794
67230	362925
67240	4108295
67240	128000
67240	958197
67250	311069
67260	460089
67260	15009
67270	8332520
67280	405688
67290	7717392
67300	137834772
67300	27500
67300	1848616
67300	486774
67300	9874
67300	160000
67310	9660519
67310	285250
67320	8720114
67330	15175326
67340	290822
67350	1241138
67360	298791
67370	1724339
67380	6692762
67380	270189
67390	6476982
67400	21406182
67400	2125341
67400	3359305
67400	2746661
67400	1273679
67400	538327
67410	396051
67400	48321198
67400	2735848
67420	148570
67430	517901
67440	596602
67450	20591573
67450	1079667
67450	5938572
67450	456472
67460	4090885
67470	1713322
67480	84630
67490	779194
67500	5364045
67500	5495834
67500	181852
67500	2560000
67520	3945145
67530	203626
67540	77283415
67540	1409791
67540	2675300
67550	1318124
67560	3623861
67580	140000
67590	19286010
67600	9407171
67600	283282
67600	318394
67610	11354341
67620	25459029
67640	8204222
67650	160226
67670	11684279
67680	2105503
67700	6912199
67700	4716
67700	10203
67710	1605753
67720	12810339
67720	204287
67720	5411309
67720	237203
67720	3831728
67720	14344
67720	362600
67730	972571
67750	604752
67760	1842000
67770	2076969
67790	2534895
67800	83215120
67800	8866
67800	891327
67810 13002429
67380	82488
67380	159000
67840	5706511
67380	8936
67850	13126892
67860	658114
67870	14211097
67880	5338731
67920	10414
67000	2041674
67960	18589334
67970	1433219
67980	873275
'''




path = '/home/debian/Documents/data/strasbourg'
path_pop = '/home/debian/Documents/data/villes'
path_naf = '/home/debian/Documents/data/strasbourg/entreprises'
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


correspondance_cp = '''
cp_old	cp_new
67000	67000
67006	67000
67007	67000
67013	67000
67015	67000
67016	67000
67017	67000
67020	67000
67021	67000
67023	67000
67025	67000
67026	67000
67027	67000
67028	67000
67029	67000
67033	67000
67034	67000
67035	67000
67036	67000
67037	67000
67038	67000
67064	67000
67067	67000
67069	67000
67070	67000
67074	67000
67080	67000
67081	67000
67082	67000
67084	67000
67085	67000
67087	67000
67088	67000
67089	67000
67091	67000
67100	67100
67110	67110
67114	67114
67115	67115
67116	67116
67117	67117
67118	67118
67119	67360
67120	67120
67121	67120
67122	67120
67129	67120
67130	67130
67131	67130
67140	67140
67150	67150
67151	67150
67160	67160
67170	67170
67171	67170
67172	67170
67173	67170
67190	67190
67200	67200
67201	67201
67202	67202
67203	67203
67204	67204
67205	67205
67207	67207
67210	67210
67215	67210
67220	67220
67222	67210
67230	67230
67235	67230
67240	67240
67242	67240
67243	67240
67250	67250
67260	67260
67269	67260
67270	67270
67280	67280
67290	67290
67300	67300
67301	67300
67302	67300
67303	67300
67305	67300
67309	67300
67310	67310
67319	67310
67320	67320
67330	67330
67340	67340
67350	67350
67360	67360
67370	67370
67380	67380
67382	67380
67390	67390
67400	67400
67401	67400
67402	67400
67403	67400
67404	67400
67405	67400
67410	67410
67411	67411
67412	67412
67420	67420
67430	67430
67440	67440
67450	67450
67451	67451
67452	67452
67454	67454
67460	67460
67470	67470
67480	67480
67490	67490
67500	67500
67501	67501
67502	67502
67503	67503
67520	67520
67530	67530
67540	67540
67541	67540
67542	67540
67550	67550
67560	67560
67580	67580
67590	67590
67600	67600
67601	67601
67603	67603
67610	67610
67620	67620
67640	67640
67650	67650
67670	67670
67680	67680
67700	67700
67701	67700
67703	67700
67710	67710
67720	67720
67722	67720
67724	67720
67725	67725
67726	67720
67727	67720
67728	67720
67730	67730
67750	67750
67760	67760
67770	67770
67790	67790
67800	67800
67802	67800
67803	67800
67810 67810
67831	67380
67836	67380
67840	67840
67843	67380
67850	67850
67860	67860
67870	67870
67880	67880
67920	67920
67953	67000
67960	67960
67970	67970
67980	67980
'''

cp_cus = '''67800 67113 67201 67550 67960 67114 67640 67118 67800 67810 67400 67450
            67380 67640 67206 67450 67207 67205 67203 67540 67115 67116 67300 67460
            67000 67100 67200 67550 67610 67202 '''.split()

corr_tab = string_to_dataframe(correspondance_cp, 2, True)

new_cp_cus = []
for x in cp_cus:
    new_cp_cus = new_cp_cus + list(corr_tab.loc[corr_tab.cp_new == x, 'cp_old'])


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



# Industrie majoritaire par dep
#a.groupby('dep')['industrie'].apply(lambda x: x.value_counts().index[0]).to_csv(os.path.join(path_naf, 'industrie_majoritaire_par_dep.csv'), sep = ';')







# Pour les plots


info_villes = pd.read_csv(os.path.join(path_pop, 'info_villes.csv'), sep = ';')
table_pop = pd.DataFrame(info_villes.groupby('postal_code')['population'].sum())
table_pop['cp'] = list(table_pop.index)

marches_2['cp'] = marches_2.cp.apply(lambda x: str(x).zfill(5))
marches_2 = marches_2.merge(table_pop, on = 'cp', how = 'outer')

marches_2['montant_par_pop'] = marches_2.montant_attribue / marches_2.population

marches_2.groupby('cp')['montant_par_pop'].sum().dropna().apply(int).to_csv(os.path.join(path, 'montant_par_pop_par_cp.csv'))
marches_2['dep'] = marches_2.cp.str.slice(0,2)

##### BLOC : AVENANTS
### : Entreprises avec la plus grosse proportion d'avenants
mmm = marches_2.groupby('attributaire').filter(lambda x: len(x) >= 5) # Entreprises avec + de 5 marches
mmm = mmm[mmm.montant_attribue != 0]
a = mmm.groupby('attributaire')['avenants'].sum() / marches_2.groupby('attributaire')['montant_attribue'].sum()
a.sort()
a.dropna()
### : 
mmm = mmm[mmm.montant_attribue != 0]  
mmm['is_local'] = mmm.cp.isin(new_cp_cus)c = b.groupby('industrie').apply(lambda x: x.avenants.sum() / x.montant_attribue.sum()) * 100
mmm.groupby(['is_local', 'type']).apply(lambda x: (x.avenants / x.montant_attribue).mean())

mmm.groupby(['is_local', 'type']).apply(lambda x: x.montant_attribue.max())


marches_2['is_local'] = marches_2.cp.isin(new_cp_cus)

# Montant en bas-rhin par an
marches_2.groupby('annee_initiale').apply(lambda x: x[x.cp.apply(lambda st: st[:2]) == '67']['montant_attribue'].sum() / x.montant_attribue.sum())

marches_2.groupby(['type', 'annee_initiale']).apply(lambda x: x[x.cp.apply(lambda st: st[:2]) == '67']['montant_attribue'].sum() / x.montant_attribue.sum())
marches_2['an_mois'] = marches_2.debut.apply(lambda x: int(str(x)[:7].replace('-', '').replace('NaT', '0')))

table_entreprises = pd.DataFrame()
for tab_name in ['first_batch.csv', 'second_batch.csv', 'third_batch.csv']:
    tab = pd.read_csv(join(path_naf, tab_name), sep = ';')
    table_entreprises = table_entreprises.append(tab)
table_entreprises['siret'] = table_entreprises.siret.apply(str).str.strip(' ')
marches_2['siret'] = marches_2.siret.apply(str).str.strip(' ')

table_entreprises['code_naf_real'] = table_entreprises.code_naf.str.findall('\d{4}[A-Z]')
table_entreprises.loc[table_entreprises.code_naf_real.apply(len) != 0, 'code_naf_real'] = table_entreprises.loc[table_entreprises.code_naf_real.apply(len) != 0,'code_naf_real'].apply(lambda x: x[0])
table_entreprises.loc[table_entreprises.code_naf_real.apply(len) == 0, 'code_naf_real'] = np.nan
table_entreprises['code_naf_small'] = np.nan
table_entreprises.loc[table_entreprises.code_naf_real.notnull(), 'code_naf_small'] = table_entreprises.loc[table_entreprises.code_naf_real.notnull(), 'code_naf_real'].apply(lambda x: x[:2])

def _recode_naf_small(x):
    if x in range(0,4):
        return 'A'
    elif x in range(5, 10):
        return 'B'
    elif x in range(10, 34):
        return 'C'
    elif x == 35:
        return 'D'
    elif x in range(36, 40):
        return 'E'
    elif x in range(41, 44):
        return 'F'
    elif x in range(45, 48):
        return 'G'
    elif x in range(49, 54):
        return 'H'
    elif x in range(55, 57):
        return 'I'
    elif x in range(58, 64):
        return 'J'
    elif x in range(64, 67):
        return 'K'
    elif x == 68:
        return 'L'
    elif x in range(69, 76):
        return 'M'
    elif x in range(77, 83):
        return 'N'
    elif x == 84:
        return 'O'
    elif x == 85:
        return 'P'
    elif x in range(86, 89):
        return 'Q'
    elif x in range(90, 94):
        return 'R'
    elif x in range(94, 97):
        return 'S'
    elif x in range(97, 99):
        return 'T'
    elif x == 99:
        return 'U'
        
        
def _recode_naf_small(x):
    if x in range(0,4):
        return 'Agriculture Sylviculture Pêche;'
    elif x in range(5, 10):
        return 'Industries Extractives Agricoles Alimentaires;'
    elif x in range(10, 34):
        return 'Industries manufacturières;'
    elif x == 35:
        return 'Électricité gaz vapeur et air conditionné;'
    elif x in range(36, 40):
        return 'Production et distribution d eau assainissement gestion des déchets et dépollution;'
    elif x in range(41, 44):
        return 'Constructions et travaux de construction;'
    elif x in range(45, 48):
        return 'Commerce de gros et de détail réparation de véhicules automobiles et de motocycles;'
    elif x in range(49, 54):
        return 'Services de transport et d entreposage;'
    elif x in range(55, 57):
        return 'Services d hébergement et de restauration;'
    elif x in range(58, 64):
        return ' Services d information et de communication;'
    elif x in range(64, 67):
        return 'Services financiers et assurances;'
    elif x == 68:
        return 'Services immobiliers;'
    elif x in range(69, 76):
        return 'Services professionnels scientifiques et techniques;'
    elif x in range(77, 83):
        return 'Services administratifs et d assistance;'
    elif x == 84:
        return ' Services d administration publique et de défense services de sécurité sociale obligatoire;'
    elif x == 85:
        return 'Services de l éducation;'
    elif x in range(86, 89):
        return 'Services de santé et d action sociale;'
    elif x in range(90, 94):
        return 'Services artistiques et du spectacle et services récréatifs;'
    elif x in range(94, 97):
        return 'Autres services;'
    elif x in range(97, 99):
        return 'Services des ménages en tant qu employeurs;'
    elif x == 99:
        return 'Services extra-territoriaux;'

a = marches_2.merge(table_entreprises[['siret', 'code_naf_small']], on = 'siret')
a.loc[a.code_naf_small.notnull(), 'code_naf_small'] = a.loc[a.code_naf_small.notnull(), 'code_naf_small'].apply(int)
a['industrie'] = a.code_naf_small.apply(_recode_naf_small)
a['mini_naf'] = a.code_naf_small.str.slice(0,1)
FFFF = a.groupby('mini_naf').apply(len)

explode = (0.2,) * 10 # only "explode" the 2nd slice (i.e. 'Hogs')
colors = ['blue'] * 10


######################### Avenants par industries
industries = a.groupby('industrie').size()
industries.sort(ascending = False)
huit_plus_grosses_industries = industries.iloc[:8]
huit_plus_grosses_industries = list(huit_plus_grosses_industries.index)
b = a[a['industrie'].isin(huit_plus_grosses_industries)]
c = b.groupby('industrie').apply(lambda x: x.avenants.sum() / x.montant_attribue.sum()) * 100

########################" SAISONALITE

saisonalite = pd.DataFrame()
marches_2 = marches_2.sort('debut')
for x in ['Travaux', 'Services', 'Fournitures']:
    a = marches_2[marches_2.type == x].groupby('an_mois')['montant_attribue'].sum()
    if x == 'Travaux':
        a = a.iloc[1:]
    a.name = x
    saisonalite = saisonalite.append(a)    
#    p = plt.plot(a / a.mean())
    
    
cmap = ('Qualitative',    ['Accent', 'Dark2', 'Paired', 'Pastel1', 'Pastel2', 'Set1', 'Set2', 'Set3'])    
    
#saisonalite = saisonalite.T
#saisonalite.index = [str(x) for x in saisonalite.index]
#plt.plot(saisonalite, lw = 3, colormap= 'Qualitative')
#plt.xticks(range(len(saisonalite)), list(saisonalite.index), rotation = 45)
#plt.legend(['Travaux', 'Services', 'Fournitures'])
#
#saisonnalite.plot(colormap = 'Accent', lw=3)
#
#plt.plot(saisonnalite, lw = 3, c = 'g')
#plt.xticks([x for x in range(len(saisonnalite)) if x%2 == 0], [list(saisonnalite.index)[i] for i in range(len(saisonnalite)) if i%2 == 0], rotation = 45)
#plt.ylabel('Montant en euros')
#plt.xlabel('Annee-Mois de debut du marche')
#plt.title('Effets de saisonnalite sur les debuts de marches')


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