# -*- coding:cp1252 -*-

'''
Created on 26 juin 2014
'''
import pandas as pd
import numpy as np
import re
import pdb

pd.set_option('max_colwidth', 100)

path_data = "C:\\Users\\work\\Documents\\ETALAB_data\\"
#Derniere mise � jour BDM
maj_bdm = 'maj_20140915122241\\'


dico_variables = dict(
    bdpm=['CIS', 'Nom', 'Forme', 'Voies', 'Statut_AMM', 'Type_AMM', 'Etat',
          'Date_AMM', 'Statut_BDM', 'Num_Europe', 'Titulaires', 'Surveillance'],
    CIP_bdpm=['CIS', 'CIP7', 'Label_presta', 'Statu_admin_presta',
              'etat_commercialisation', 'Date_declar_commerc', 'CIP13',
              'aggrement_collectivites', 'Taux_rembours', 'Prix',
              'indic_droit_rembours'],
    GENER_bdpm=['Id_Groupe', 'Nom_Groupe', 'CIS', 'Type', 'Num_Tri'],
    COMPO_bdpm=['CIS', 'Element_Pharma', 'Code_Substance', 'Nom_Substance',
                'Dosage', 'Ref_Dosage', 'Nature_Composant',
                'Substance_Fraction'],
    HAS_SMR_bdpm=['CIS', 'HAS', 'Evalu', 'Date', 'Valeur_SMR', 'Libelle_SMR'],
    HAS_ASMR_bdpm=['CIS', 'HAS', 'Evalu', 'Date', 'Valeur_ASMR',
                   'Libelle_ASMR'],
    )

unite_standard = ['ml', 'mg', 'litre']
element_standard = [u'comprim�', u'g�lule', u'capsule', u'flacon', u'ampoule',
                    u'dispositif', u'lyophilisat', u'pastille', u'seringue',
                    u'sachet-dose', u'suppositoire', u'dose', u'ovule',
                    u'sachet', u'gomme', u'tube', u'b�ton', u'creuset', u'insert',
                    u'r�cipient', u'poche', u'cartouche', u'pression', u'film',
                    u'cm^2', u'g�n�rateur', u'stylo', u'empl�tre',
                    u'goutte', u'anneau', u'�ponge', u'p�te', u'compresse',
                    u'implant', u'r�cipient', u'pot', u'bouteille', u'unit�',
                    u'pilule', u'seringue pr�remplie']
                    # u'mole',  pour les gaz
            #contenants = ['plaquette','flacon','tube', 'r�cipient', 'sachet',
#              'cartouche', 'boite', 'pochette', 'seringue', 'poche',
#              'pilulier', 'ampoule', 'pot', 'stylo', 'film', 'inhalateur',
#              'bouteille', 'vaporateur', 'enveloppe', 'g�n�rateur',
#              'bo�te', 'aquette', 'sac', 'pompe', 'distributeur',
#              'applicateur', 'f�t'
#              ]
element_standard = [x.encode('cp1252') for x in element_standard]


def recode_dosage(table):
    assert 'Dosage' in table.columns
    table = table[table['Dosage'].notnull()]
    table['Dosage'] = table['Dosage'].str.replace(' 000 ', '000 ')
    # il faut le faire 2 fois
    table['Dosage'] = table['Dosage'].str.replace(' 000 ', '000 ')
    table['Dosage'] = table['Dosage'].str.replace('7 500', '7500')
    table['Dosage'] = table['Dosage'].str.replace('4 500', '4500')
    table['Dosage'] = table['Dosage'].str.replace('3 500', '3500')
    table['Dosage'] = table['Dosage'].str.replace('2 500', '2500')
    table['Dosage'] = table['Dosage'].str.replace('1 500', '1500')
    table['Dosage'] = table['Dosage'].str.replace('1 200', '1200')
    table['Dosage'] = table['Dosage'].str.replace('3 700', '3700')
    table['Dosage'] = table['Dosage'].str.replace(',', '.')
    table['Dosage'] = table['Dosage'].str.replace('\. ', '.')
    return table


def recode_ref_dosage(table):
    # TODO: on a des probl�me de ref dosage.
    assert 'Ref_Dosage' in table.columns
    table = table[table['Ref_Dosage'].notnull()]
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('un ','')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('une ','')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('1ml','1 ml')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('L','l')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace("\(s\)",'')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace(',','.')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('100. 0 g','100.0 g')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('00ml','00 ml')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('1g','1 g')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('1ml','1 ml')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('ml</p>', 'ml')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('comrpim�','comprim� ')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('comprimer','comprim� ')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('comprim�.','comprim� ')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('comprimp�','comprim� ')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('gelule','g�lule')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('g�lulle','g�lule')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('gramme','g')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('r�cipent','r�cipient')
    table['Ref_Dosage'] = table['Ref_Dosage'].str.replace('pr�-remplie' ,'pr�remplie')
    return table


def recode_label_presta(table):
    assert 'Label_presta' in table.columns
    # TODO: identifier d'o� viennent les label nuls
    table = table[table['Label_presta'].notnull()]
    table['Label_presta'] = table['Label_presta'].str.replace(',', '.')
    table['Label_presta'] = table['Label_presta'].str. \
        replace("\(s\)", '')
    # 1 seul cas, qui n'est pas grave car flacon
    table['Label_presta'] = table['Label_presta'].str.replace('1 1', '1')
    table['Label_presta'] = table['Label_presta'].str.replace('00 00', '0000')
    table['Label_presta'] = table['Label_presta'].str.replace('1500 m', '0 ml')
    # Note tr�s risqu�...
    table['Label_presta'].loc[24] = '2 plaquette thermoform�e PVC-aluminium de 10 comprim�'
    # un oubli du nombre de comprim�
    table['Label_presta'] = table['Label_presta'].str.replace(
        'plaquette thermoform�e PVC poly�thyl�ne PVDC aluminium comprim�',
        'plaquette thermoform�e PVC poly�thyl�ne PVDC aluminium 60 comprim�')
    return table


def load_medic_gouv(maj_bdm, var_to_keep=None, CIP_not_null=False):
    ''' renvoie les tables fusionn�es issues medicament.gouv.fr
        si var_to_keep est rempli, on ne revoit que la liste des variables
    '''
    # chargement des donn�es
    path = path_data + "medicament_gouv\\" + maj_bdm
    output = None
    for name, vars in dico_variables.iteritems():
        # teste si on doit ouvrir la table
        if var_to_keep is None:
            intersect = vars
        if var_to_keep is not None:
            intersect = [var for var in vars if var in var_to_keep]
        if len(intersect) > 0:
            ############
            tab = pd.read_table(path + 'CIS_' + name + '.txt', header=None)
            ##############
            if name in ['COMPO_bdpm', 'GENER_bdpm']:
                tab = tab.iloc[:, :-1]
            tab.columns = vars
            tab = tab[['CIS'] + intersect]
            # correction ad-hoc...
            if tab['CIS'].dtype == 'object':
                problemes = tab['CIS'].str.contains('REP', na=False)
                problemes = problemes | tab['CIS'].isin(['I6049513', 'inc     '])
                tab = tab.loc[~problemes, :]
                tab['CIS'].astype(int)

            if 'Ref_Dosage' in intersect:
                tab = recode_ref_dosage(tab)
            if 'Dosage' in intersect:
                tab = recode_dosage(tab)
            if 'Label_presta' in intersect:
                tab = recode_label_presta(tab)

            if output is None:
                output = tab
                print("la premi�re table est " + name + " , son nombre de " +
                      "lignes est " + str(len(output)))
            else:

                output = output.merge(tab, how='outer', on='CIS',
                                      suffixes=('', name[:-4]))
                if CIP_not_null:
                    if 'CIP7' in output.columns:
                        output = output[output['CIP7'].notnull()]
                print("apr�s la fusion avec " + name + " la base mesure " +
                      str(len(output)))
    return output

if __name__ == '__main__':
#table = load_medic_gouv(maj_bdm, ['Etat','Date_AMM','CIP7','Label_presta','Date_declar_commerc','Taux_rembours','Prix','Id_Groupe','Type',
#                                  'indic_droit_rembours', 'Statu_admin_presta','Element_Pharma','Code_Substance','Nom_Substance','Dosage',
#                                  'Ref_Dosage','Nature_Composant','Substance_Fraction'])
#     test = load_medic_gouv(maj_bdm)
    table = load_medic_gouv(maj_bdm, ['CIP7', 'Label_presta',
                                      'Element_Pharma','Code_Substance',
                                      'Nom_Substance','Dosage',
                                      'Ref_Dosage','Nature_Composant','Substance_Fraction',
                                      'Id_Groupe','Prearix'])

    table = table[~table['Element_Pharma'].isin(['pansement', 'gaz'])]

    for var in ['Ref_Dosage', 'Dosage', 'Label_presta']:
        print table[var].isnull().sum()
        table = table[table[var].notnull()]


def extract_quantity(label, reference):
    # TODO: douteux quand la r�f�rence apparait plusieurs fois
    # on ne garde que la partie avant la r�f�rence
    label = label[:label.index(reference)]
    # s'il y a un "et" ou un " - ", on ne prend que
    # la partie qui concerne la r�f�rence
    if " et " in label:
        label = label.split(' et ')[-1]
    if " - " in label:
        label = label.split(" - ")[-1]
    floats = re.findall(r"[-+]?\d*\.\d+|\d+", label)
    floats = [float(x) for x in floats]
    if len(floats) == 0:    
        pdb.set_trace()
        return 1
    return reduce(lambda x, y: x*y, floats)

table['nb_ref_in_label'] = pd.Series(0.0)
incoherence_identifiee = []
for i, row in table[['Ref_Dosage', 'Dosage', 'Label_presta', 'nb_ref_in_label']].iterrows():
    # travail de base sur la r�f�rence
    reference = row['Ref_Dosage']
    if reference[:2] == '1 ':
        reference = reference[2:]
    ref_floats = re.findall(r"[-+]?\d*\.\d+|\d+", reference)
    if len(ref_floats) > 0:
        ref_floats = [float(x) for x in ref_floats]
        reference_dose = reduce(lambda x, y: x*y, ref_floats)
    else:
        reference_dose = 1
    print reference
    # travail de base sur le label
    label = row['Label_presta']
    if label.split()[0] in element_standard:
        label = '1 ' + label

    if reference in label:
        # TODO: douteux quand la r�f�rence apparait plusieurs fois
        label_dose = extract_quantity(label, reference)
        row['nb_ref_in_label'] = label_dose/reference_dose

    if row['nb_ref_in_label'] == 0:
        for unite in ['ml', 'l', 'mg', 'g', 'dose']:
            if len(reference) >= len(unite) + 1:
                if ' ' + unite + ' ' in reference or \
                   reference[-(len(unite) + 1):] == ' ' + unite:
                   row['nb_ref_in_label'] = extract_quantity(label, ' ' + unite)

    if row['nb_ref_in_label'] == 0:
        reference = row['Ref_Dosage']
        contenant = [var for var in element_standard
                     if var in reference]
        if len(contenant) == 1:
            var = contenant[0]
            if var in label:
                label_dose = extract_quantity(label, var)
                row['nb_ref_in_label'] = label_dose

    if row['nb_ref_in_label'] == 0:
        reference = row['Ref_Dosage']
        if reference in ['lyophilisat', '1 flacon']:
            row['nb_ref_in_label'] = extract_quantity(label, 'flacon')

    if row['nb_ref_in_label'] == 0:
        reference = row['Ref_Dosage']
        if (('mg' in  reference and 'ml' in label) or
            ('ml' in  reference and 'mg' in label)):
            incoherence_identifiee += [i]

    if row['nb_ref_in_label'] == 0:
        print(row)
        pdb.set_trace()

