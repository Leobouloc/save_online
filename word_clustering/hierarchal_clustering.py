# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 10:01:48 2015

@author: debian
"""
import pandas as pd
import os
import sys
import psutil
import gc

path = '/home/debian/Documents/data/strasbourg'
file = os.path.join(path, 'distance_tab.csv')
file_2 = os.path.join(path, 'table_des_mots_2.csv')
print u'Loading file'
#distance_tab = pd.read_csv(file, sep = ';', index_col = 0)
#table_des_mots_2 = pd.read_csv(file_2, sep = ';', index_col = 0)
print u'File loaded'
sys.setrecursionlimit(5000) 

def make_input(distance_tab):
    distance_table = distance_tab.copy()
    assert len(distance_table) == len(distance_table.columns)
    cluster_content = dict()
    for i in range(len(distance_table)):
        cluster_content[i] = [distance_table.columns[i]]
    distance_table.columns = range(len(distance_table))
    distance_table.index = range(len(distance_table))
    return [distance_table, cluster_content]


distance_param = 'min' 
ratio = 1.1


class ClusterProblem(object):
    
    # 'min' or 'max'
    
    def __init__(self, matrix, cluster_content, cluster_problem = None):
        self.distance_matrix = matrix # Matrix with integer keys
        self.cluster_content = cluster_content # Dict with integer keys and lists
        self.next_cluster_problem = cluster_problem
    
    def nb_levels(self):
        if self.cluster_content == None:
            return 1 + self.next_cluster_problem.nb_levels()
        if len(self.cluster_content) == 1:
            return 1
        else:
            return 1 + self.next_cluster_problem.nb_levels()
    
    def get_level(self, nb):
        a = self
        for i in range(nb):
            a = a.next_cluster_problem
        return a

    def print_cluster(self):
        for key, value in self.cluster_content.iteritems():
            print value
            print '\n'
        
    def get_min_coords(self):
#        coord_x = self.distance_matrix.min().argmin().copy()
#        coord_y = self.distance_matrix[coord_x].argmin().copy()
        coord_x = self.distance_matrix.min().argmin()
        coord_y = self.distance_matrix[coord_x].argmin()
        return [coord_x, coord_y]
    
    ## Nouvelles_distances
    def new_distance_matrix(self, coord_x, coord_y):
        '''Cree la nouvelle_matrice des distances'''
        distance_matrix = self.distance_matrix.copy()
#        assert all([distance_matrix.iloc[i, i] == inf for i in range(len(distance_matrix))])
        if distance_param == 'mean':
            new_dist = distance_matrix.apply(lambda x: (x[coord_x] + x[coord_y])/2.0)
        elif distance_param == 'min':
            new_dist = distance_matrix.apply(lambda x: min(x[coord_x], x[coord_y])) * ratio       
        new_dist = new_dist.append(pd.Series([inf]))
        distance_matrix[len(distance_matrix)] = inf
        distance_matrix.loc[len(distance_matrix), :] = inf
#        print distance_matrix
        ### C est necessaire de faire _a en deux temps pour des problemes de forme

        distance_matrix.loc[:, len(distance_matrix) - 1] = list(new_dist)
        distance_matrix.loc[len(distance_matrix) - 1, :] = list(new_dist)

        distance_matrix.drop(coord_x, inplace = True)
        distance_matrix.drop(coord_x, inplace = True, axis = 1)
        distance_matrix.drop(coord_y, inplace = True)
        distance_matrix.drop(coord_y, inplace = True, axis = 1)

        
        distance_matrix.columns = range(len(distance_matrix))
        distance_matrix.index = range(len(distance_matrix))
        return distance_matrix
        
    def new_cluster_content(self, coord_x, coord_y):
        cluster_content = self.cluster_content.copy()
        new_cluster_content_last = cluster_content[coord_x] + cluster_content[coord_y]
        new_cluster_content = dict()
        compteur = 0
        for key, value in cluster_content.iteritems():
            if key in [coord_x, coord_y]:
                compteur += 1
            else:
                new_cluster_content[key-compteur] = value
        new_cluster_content[len(new_cluster_content)] = new_cluster_content_last
        return new_cluster_content
    
    def step(self):
        print len(self.cluster_content)
        print 1, psutil.phymem_usage()
        if len(self.cluster_content) == 1:
            return self
        else:
            [coord_x, coord_y] = self.get_min_coords()
            print 2, psutil.phymem_usage()
            new_distance_matrix = self.new_distance_matrix(coord_x, coord_y)
            print 3, psutil.phymem_usage()
            new_cluster_content = self.new_cluster_content(coord_x, coord_y)
            print 4, psutil.phymem_usage()
            next_cluster_problem = ClusterProblem(new_distance_matrix, new_cluster_content)
            print 5, psutil.phymem_usage()
                        
            if len(self.cluster_content) > 200:
                self.cluster_content = None
                self.distance_matrix = None
           
            print 6, psutil.phymem_usage()
            
            del new_distance_matrix
            del new_cluster_content
            
            collected = gc.collect()
            print "Garbage collector: collected %d objects." % (collected)            
            print 7, psutil.phymem_usage()
            
#            self.next_cluster_problem = next_cluster_problem
            self.next_cluster_problem = next_cluster_problem.step()
            return self

            
            
#    def make_all(self):
#        next_cluster_problem = self.step()
#        if len(next_cluster_problem.cluster_content) != 1:
#            self.next_cluster_problem = next_cluster_problem.make_all()
#        else:
#            self.next_cluster_problem = next_cluster_problem


#a = table_des_mots_2.sum()
#a.sort(ascending = False)
#a = a[27:]
#sel = a.index[:1000]
#distance_tab_copy = distance_tab
#distance_tab = distance_tab.loc[sel, sel]
#distance_tab.dropna(how = 'all', axis = 0, inplace = True)
#distance_tab.dropna(how = 'all', axis = 1, inplace = True)


#def main(args):
[distance_matrix, cluster_content] = make_input(distance_tab)

cluster_problem = ClusterProblem(distance_matrix, cluster_content)
cluster_problem.step()


#while True:
#    next_cluster_problem = current_cluster_problem.step()
#    current_cluster_problem.cluster_problem = next_cluster_problem
#    current_cluster_problem = next_cluster_problem

#    return 0

#
#if __name__ == '__main__':
#    sys.exit(main(sys.argv[1:]))


#for rat in [1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4]:
#    ratio = rat
#    print ratio
#    [distance_matrix, cluster_content] = make_input(distance_tab)
#    clust_prob = cluster_problem(distance_matrix, cluster_content)
#    a = clust_prob.step()
#    cluster_content_list = [value for key, value in a.get_level(340).cluster_content.iteritems()]
#    cluster_content_len = [len(clust) for clust in cluster_content_list]
#    print 'std : ' + str(std(cluster_content_len))