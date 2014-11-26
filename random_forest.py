# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 14:50:10 2014

@author: work
"""

import pandas as pd
import math
import numpy as np
import random as rand



def categorizer(table, sort_string, cat_num = 2):
    a = table.copy()
    a.sort(sort_string, inplace = True)
    a = a[sort_string]
    quantiles = [a.quantile(1/float(cat_num) * n) for n in range(1, cat_num)]
#    a = a.cumsum()
#    max_val = a.max()
#    quantiles = [float(max_val)/cat_num * float(x) for x in range(1, cat_num)]
    
    i = 0
    indexes = []
    for val in quantiles:
        loop = True
        val_index =[]
        while loop:
            loop = (a.iloc[i] < val) | (np.isnan(a.iloc[i]))
            val_index += [a.index[i]]
            i += 1
        indexes += [val_index]   
    
    new_col_name = sort_string + '_cat_' + str(cat_num)
    table[new_col_name] = cat_num - 1
    for i in range(len(indexes)):
        table.loc[indexes[i], new_col_name] = i
    table.loc[table[sort_string].isnull(), new_col_name] = np.nan
    return table


def entropy(serie_of_outcomes):
    # Serie of outcomes is the number of apparitions of each variable that has to be predicted
    serie_of_outcomes = serie_of_outcomes.apply(float)    
    frequencies = serie_of_outcomes / serie_of_outcomes.sum()
    list_s = []
    for p in frequencies:
        if p==0:
            list_s += [0]
        else:
            list_s += [p*math.log(p, 2)]
    return sum(list_s)

def entropy_tab(table_group):
    return table_group.apply(lambda x: sum(x) * entropy(x), axis = 1).sum() / table_group.sum().sum()

def feature_entr(table, feature, variable):
    # variable is what has to be classified
    table_count = pd.crosstab(table[feature], table[variable])
    return table_count.apply(lambda x: sum(x) * entropy(x), axis = 1).sum() / table_count.sum().sum()
    
class decision_tree(object):
    def __init__(self, type_, free_features, constr_features, const_features_values, value, table_len):
        # type is either leaf or node
        # value is either variable or 
        self.type=type_
        self.free_features=free_features # is a list
        self.constr_features=constr_features # Constrained features
        self.const_features_values=const_features_values # Constrained features values
        self.value=value # Value is either leaf value or list of trees
        self.table_len = table_len

    def explore(self, function):
        assert self.type in ['node', 'leaf']
        if self.type == 'leaf':
            function(self)
        else:
            function(self)
            for son in self.value:
                son.explore(function)
    
    def depth(self):
        if self.type == 'leaf':
            return 0
        else:
            return (1 + max([val.depth() for val in self.value]))
            
    def num_leafs(self):
        if self.type == 'leaf':
            return 1
        else:
            return sum([val.num_leafs() for val in self.value])

    def num_nodes(self):
        if self.type == 'leaf':
            return 0
        else:
            return 1 + sum([val.num_nodes() for val in self.value])
        

# TODO: length of table at each leaf / node


    def print_leaves(self):
        def print_func(x):
            if x.type == 'leaf':
                string = ''
                for i in range(len(x.constr_features)):
                    string += str(x.constr_features[i]) + ' : ' + str(x.const_features_values[i]) + ' // '
                print string + ' ---> ' + str(x.value) + ' / ' + str(x.table_len)
        self.explore(print_func)
        
    
    def create_decision_tree(self, table, variable):
        '''Creates a decision Tree based on ID3 method'''
        if table[variable].nunique() == 1: # entropy == 0
            value = (table[variable].iloc[0], 1)
            return decision_tree('leaf', list(self.free_features), 
                                 list(self.constr_features),
                                list(self.const_features_values), value, len(table))

        if len(self.free_features) in [0]:
            pred_value = table[variable].value_counts().argmax()
            pred_confidence = float(sum(table[variable] == pred_value)) / float(len(table))
            value = (pred_value, pred_confidence)
            return decision_tree('leaf', list(self.free_features),
                                 list(self.constr_features), list(self.const_features_values), value, len(table))

        if len(table[self.free_features].drop_duplicates()) == 1:
            pred_value = table[variable].value_counts().argmax()
            pred_confidence = float(sum(table[variable] == pred_value)) / float(len(table))
            value = (pred_value, pred_confidence)
            return decision_tree('leaf', list(self.free_features),
                                 list(self.constr_features), list(self.const_features_values), value, len(table))
    
        self.type = 'node'

        # If we are not at a leaf
        free_features = list(self.free_features)
        selected_free_features = list(free_features)        
        
        ### For random forest algorithm
#        coef = 0.7
#        selected_free_features = rand.sample(list(free_features), int(round(len(free_features) * coef)))

        features_entropy = dict(zip(selected_free_features, [feature_entr(table, feature, variable) for feature in selected_free_features]))
        # Select feature minimizing entropy        
        best_feature = selected_free_features[0]
        best_feature_entropy = features_entropy[best_feature]
        for key in features_entropy.keys():
            if features_entropy[key] < best_feature_entropy:
                best_feature = key
                best_feature_entropy = features_entropy[key]

        new_free_features = list(self.free_features)
        new_free_features.remove(best_feature)
        new_constr_features = list(self.constr_features)
        new_constr_features += [best_feature]
        new_const_features_values = list(self.const_features_values)
        
        value = [decision_tree(None, new_free_features, new_constr_features, new_const_features_values + [feat_val], None, len(table)).create_decision_tree(table[table[best_feature] == feat_val], variable)  for feat_val in table[best_feature].unique()]

        self.value = value
        
        return self
        

    def predict_line(self, ligne):
        if self.type == 'leaf':
            return( [self.value, self.table_len])
        else:
            for val in self.value:
                if all(ligne[val.constr_features] == val.const_features_values):
                    return val.predict_line(ligne)
                    
    def predict_table(self, table):     
        return table.apply(lambda ligne: self.predict_line(ligne), axis = 1)


def tree(table, features, variable, features_split_num):    
    features_cat = [ft + '_cat_'  + str(num_split) for (ft, num_split) in zip(features, features_split_num)]   
   
    for (feature, feature_cat, num_split) in zip(features, features_cat, features_split_num):
        if not (feature_cat in table.columns):
            table = categorizer(table, feature, cat_num = num_split)
       
    print 'Calculating tree...'
    tree = decision_tree(None, features_cat, [], [], None, len(table))
    tree.create_decision_tree(table, variable)
    return [tree, villes2]
