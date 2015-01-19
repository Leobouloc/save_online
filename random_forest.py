# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 14:50:10 2014

@author: work
"""

import pandas as pd
import math
import numpy as np


'''Classification Trees '''

def entropy(serie_of_outcomes):
    # List of outcomes is the number of apparitions of each variable that has to be predicted
    frequencies = serie_of_outcomes / serie_of_outcomes.sum()
    list_s = []
    for p in frequencies:
        if p==0:
            list_s += [0]
        else:
            list_s += p*math.log(p, 2)
    return sum(list_s)

def entropy_tab(table_group):
    return table_group.apply(lambda x: sum(x) * entropy(x), axis = 1).sum() / table_group.sum().sum()

def feature_entr(table, feature, variable):
    # variable is what has to be classified
    table_count = pd.crosstab(table[feature], table[variable])
    return table_count.apply(lambda x: sum(x) * entropy(x), axis = 1).sum() / table_count.sum().sum()
    
class decision_tree(object):
    def __init__(self, type_, free_features, constr_features, const_features_values, value):
        # type is either leaf or node
        # value is either variable or 
        self.type=type_
        self.free_features=free_features # is a list
        self.constr_features=constr_features # Constrained features
        self.const_features_values=const_features_values # Constrained features values
        self.value=value # Value is either leaf value or list of trees

    def explore(self, function):
        assert self.type in ['node', 'leaf']
        if self.type =='leaf':
            function(self)
        else:
            function(self)
            for son in self.value:
                son.explore(function)

    def print_leaves(self):
        def print_func(x):
            if x.type == 'leaf':
                string = ''
#                print 'length : ' + str(len(x.constr_features))
                for i in range(len(x.constr_features)):
                    string += str(x.constr_features[i]) + ' : ' + str(x.const_features_values[i]) + ' // '
#                    print x.const_features_values[i]
                print string + ' ---> ' + str(x.value)
        self.explore(print_func)
        
    
    def create_decision_tree(self, table, variable):
        if table[variable].nunique() == 1: # entropy == 0
            print 'here'
            value = (table[variable].iloc[0], 1)
            return decision_tree('leaf', list(self.free_features), 
                                 list(self.constr_features),
                                list(self.const_features_values), value)

        if len(self.free_features) == 0:
            print 'there'
            pred_value = table[variable].value_counts().argmax()
            pred_confidence = float(sum(table[variable] == pred_value)) / float(len(table))
            value = (pred_value, pred_confidence)
            return decision_tree('leaf', list(self.free_features),
                                 list(self.constr_features), list(self.const_features_values), value)

        if len(table[self.free_features].drop_duplicates()) == 1: #len(self.free_features) == 0:
            print 'haha'
            pred_value = table[variable].value_counts().argmax()
            pred_confidence = float(sum(table[variable] == pred_value)) / float(len(table))
            value = (pred_value, pred_confidence)
            return decision_tree('leaf', list(self.free_features),
                                 list(self.constr_features), list(self.const_features_values), value)
    
        self.type = 'node'

        # If we are not at a leaf
        free_features = list(self.free_features)
        features_entropy = dict(zip(free_features, [feature_entr(table, feature, variable) for feature in free_features]))
        # Select feature minimizing entropy        
        best_feature = free_features[0]
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
        
        
        
        print 'sfs : '+ str(new_free_features)
        
        print 'sfdssfds : ' + str(new_constr_features)

        value = [decision_tree(None, new_free_features, new_constr_features, new_const_features_values + [feat_val], None).create_decision_tree(table[table[best_feature] == feat_val], variable)  for feat_val in table[best_feature].unique()]

        self.value = value
        
        return self

    
def tree(table, features, variable):
    tree = decision_tree(None, features, [], [], None)
    tree.create_decision_tree(table, variable)
    return tree
