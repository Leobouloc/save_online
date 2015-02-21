# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 12:25:55 2015

@author: leo
"""

import matplotlib.pyplot as plt 

from panda_tools import panda_merge, bind_and_plot#, make_forest, use_forest
import pandas as pd
from os import listdir
import numpy as np
from os.path import isfile, join
from datetime import datetime

from StringIO import StringIO


inf = np.inf
#path = '/home/debian/Documents/data/foot'
path = 'C:\\Users\\work\\Documents\\ETALAB_data\\soccer\\greece'

def load_table(path):
    all_tab_names = [f for f in listdir(path) if isfile(join(path,f)) if '.csv' in f]

    table = pd.DataFrame()
    for tab_name in all_tab_names:
        tab = pd.read_csv(join(path,tab_name))
        tab['source'] = tab_name
        table = table.append(tab)

    table.columns = [x.lower() for x in table.columns]
    print table.columns
    table = table[['date', 'source', 'hometeam', 'awayteam', 'fthg', 'ftag', 'ftr', 'hthg', 'htag', 'whh', 'whd', 'wha']]
#    table = table[['date', 'hometeam', 'awayteam', 'fthg', 'ftag', 'ftr', 'hthg', 'htag', 'htr', 'hr', 'ar', 'whh', 'b365h', 'wha', 'bsh', 'bwh', 'gbh', 'iwh', 'lbh', 'psh', 'sbh', 'sjh', 'vch']]
#    table['cote'] = table[['whh', 'b365h', 'bsh', 'bwh', 'gbh', 'iwh', 'lbh', 'psh', 'sbh', 'sjh', 'vch']].apply(lambda x: max(x), axis = 1)
    table['date'] = table.date.apply(lambda date: datetime.strptime(date, "%d/%m/%y"))
    table.index = range(len(table))
    return table


def make_table_team(table):
    # Team home
    table_team_h = table[['date', 'source', 'hometeam', 'fthg', 'hthg',  'ftr']]
    table_team_h['win'] = table_team_h.ftr == 'H'
    table_team_h['draw'] = table_team_h.ftr == 'D'
    table_team_h['lose'] = table_team_h.ftr == 'A'
    table_team_h.drop('ftr', inplace = True, axis = 1)
    table_team_h['h_or_a'] = 'h'
    table_team_h.columns = ['date', 'source', 'team', 'ftg', 'htg', 'win', 'draw', 'lose', 'h_or_a']
    
    # Team away
    table_team_a = table[['date', 'source', 'awayteam', 'ftag', 'htag',  'ftr']]
    table_team_a['win'] = table_team_a.ftr == 'A'
    table_team_a['draw'] = table_team_a.ftr == 'D'
    table_team_a['lose'] = table_team_a.ftr == 'H'
    table_team_a.drop('ftr', inplace = True, axis = 1)
    table_team_a['h_or_a'] = 'a' 
    table_team_a.columns = ['date', 'source','team', 'ftg', 'htg',  'win', 'draw', 'lose', 'h_or_a']
    
    # Table away + home
    table_team = table_team_h.append(table_team_a)
    
    return [table_team, table_team_h, table_team_a]


def make_stats_table(table_team, five = 10):
    table_team.sort('date', inplace = True)    
    table_team['index'] = list(table_team.index)
    grp = table_team.groupby('team')
    # Num goals
    ftg_sum = grp.apply(lambda x: x.ftg.cumsum() - x.ftg)
    ftg_sum_minus_five = ftg_sum.reset_index(level = 'team').groupby('team').apply(lambda x: pd.Series(five*[inf] + list(x.ftg)[:-five], index = x.index)) #Cumsum at the time of 5 matchs before
    ftg_last_five = ftg_sum - ftg_sum_minus_five
    # Num wins
    win_sum = grp.apply(lambda x: x.win.cumsum() - x.win)
    win_sum_minus_five = win_sum.reset_index(level = 'team').groupby('team').apply(lambda x: pd.Series(five*[inf] + list(x.win)[:-five], index = x.index)) #Cumsum at the time of 5 matchs before
    win_last_five = win_sum - win_sum_minus_five
    # Num draws
    draw_sum = grp.apply(lambda x: x.draw.cumsum() - x.draw)
    draw_sum_minus_five = draw_sum.reset_index(level = 'team').groupby('team').apply(lambda x: pd.Series(five*[inf] + list(x.draw)[:-five], index = x.index)) #Cumsum at the time of 5 matchs before
    draw_last_five = draw_sum - draw_sum_minus_five
    ## Num lose
    #lose_sum = grp.apply(lambda x: x.lose.cumsum() - x.draw)
    #lose_sum_minus_five = lose_sum.reset_index(level = 'team').groupby('team').apply(lambda x: pd.Series(five*[inf] + list(x.lose)[:-five], index = x.index)) #Cumsum at the time of 5 matchs before
    #lose_last_five = lose_sum - lose_sum_minus_five
    
#    red_last = table_team.groupby('team').apply(lambda x: pd.Series([np.nan] + list(x.r.iloc[:-1]), index = x.index))
    num_matchs_in_last_2_weeks = table_team.groupby('team').apply(lambda all_matchs: all_matchs.date.apply(lambda date: sum((date > all_matchs.date) & ((date - all_matchs.date).apply(lambda x: x / np.timedelta64(1, 'D')) <= 14))))
    
    nb_matchs = grp.apply(lambda x: pd.Series(range(len(x)), index = x.index))
    ftg_per_match = ftg_sum / nb_matchs
    
    stats_table = pd.DataFrame(columns = ['team', 'level_1'])
    for metric in [ftg_last_five, win_last_five, draw_last_five, ftg_per_match, num_matchs_in_last_2_weeks]:
        metric = metric.reset_index()
        stats_table = stats_table.merge(metric, on = ['team', 'level_1'], how = 'outer')
        
    stats_table.columns = ['team', 'index', 'ftg_last_five', 'win_last_five', 'draw_last_five', 'ftg_per_match', 'num_matchs_in_last_2_weeks']
    
    table_team = table_team.merge(stats_table, on = ['team', 'index'])
    return table_team

def make_global_table(table):
    
    [table_team, table_team_h, table_team_a] = make_table_team(table)
#    table_team_h.columns = ['when_home_' + col for col in table_team_h.columns]
#    table_team_h.columns = ['when_away_' + col for col in table_team_h.columns]
    
    table_team = make_stats_table(table_team)
    columns = table_team.columns
    columns_h = ['h_' + x for x in list(columns)]
    columns_a = ['a_' + x for x in list(columns)]
    
    
    table_team.columns = columns_h
    table = table.merge(table_team, left_on = ['hometeam', 'date'], right_on = ['h_team', 'h_date'])
    table_team.columns = columns_a
    table = table.merge(table_team, left_on = ['awayteam', 'date'], right_on = ['a_team', 'a_date'])
    
    predictors = columns[10:]
    
    for col in predictors:
        table[col] = table['h_' + col].apply(float) / table['a_' + col].apply(float)
    table_team.columns = [x.replace('a_', '') for x in table_team.columns]
    return [table, predictors, table_team]
    
    
table = load_table(path)
[table, predictors, table_team] = make_global_table(table)

predictors = [u'ftg_last_five', u'win_last_five', u'draw_last_five', u'ftg_per_match', u'num_matchs_in_last_2_weeks']
sel = table[predictors].apply(lambda x: (x.notnull().all() & (x != np.inf).all()) & (x != inf).all(), axis = 1)
table= table[sel]
table['ftr_num'] = 0
table.loc[table.ftr == 'D', 'ftr_num'] = 1
table.loc[table.ftr == 'A', 'ftr_num'] = 2

table[predictors] = table[predictors] * 1000
table[predictors] = table[predictors].applymap(round)

train = table.iloc[:1700]
test = table.iloc[1700:]

################
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
forest = RandomForestClassifier(n_estimators = 100, min_samples_split = 4, min_samples_leaf = 2)
forest = DecisionTreeClassifier(max_depth=10, min_samples_leaf=1)

def test_func(x):
    try:
        return int(min(val, 10000))
    except:
        print val > 10
        print val
        print type(val)

to_predict = 'ftr'
X = []
for i in train.index:
    X += [[int(min(abs(val), 10000)) for val in list(train[predictors].loc[i])]]
y = list(train[to_predict])
forest.fit(X, y)

X = []
for i in test.index:
    X += [[int(min(abs(val), 10000)) for val in list(test[predictors].loc[i])]]
test['prediction'] = forest.predict(X)
print 'Proportion bien predite', (test.prediction == test.ftr).sum() / float(len(test))
test[['hometeam', 'awayteam'] + predictors + ['prediction'] + ['ftr']]

# Gains sur les pred away
test.loc[(test['prediction'] == 'A') & (test.ftr == 'A'), 'wha'].sum() - (test['prediction'] == 'A').sum()


table_team_copy = table_team
table_team['year'] = table_team.date.apply(lambda x: x.year)
#tab_te = table_team.groupby('source').get_group('L1_13_14.csv')
#
#tab_te = tab_te.sort('date')
#for x in tab_te.groupby('team'):
#    plt.plot(x[1].win.cumsum())
##    plt.plot(x.win.cumsum())




#table_team.groupby(['team', 'source']).apply(lambda x: x.win.cumsum())

################





#make_forest(train[predictors + ['ftr_num']], 'ftr_num', predictors)
