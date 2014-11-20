# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 14:51:23 2014

@author: work
"""

#expr = [[2, '*', 'a'], '+', 'b']
expr = ['*', ['+', 4, 5, 6], 'a', 'b']
expr2 = ['+', ['+', 4, 5], 6]

operators = ['+', '*', '/']
operators_fois = ['*', '/']
operators_plus = ['+', '-']


#def print_expr(expr):
#    if isinstance(expr, str) or isinstance(expr, int):
#        return ' ' + str(expr) + ' '
#    else:
#        inside = ''
#        for expr_n in expr:
#            inside += print_expr(expr_n)
#        return '(' + inside + ')'

def print_expr(expr):
    '''print l'expression'''
    assert verif_expr(expr)
    
    if isinstance(expr, str) or isinstance(expr, int):
        return ' ' + str(expr) + ' '
    elif isinstance(expr[0], str) and expr[0] in operators:
        op = expr[0]
        distribute = '(' + print_expr(expr[1])
        for expr_n in expr[2:]:
            distribute += op + print_expr(expr_n)
        distribute += ') '
        return distribute
        
def print_egalite(expr1, expr2):
    verif_expr(expr)
    print print_expr(expr1) + ' = ' + print_expr(expr2)

def is_leaf(val):
    if (isinstance(val, str) or isinstance(val, int)) and (not val in operators):
        return True
    else:
        return False
        
def is_op(val):
    return val in operators 

def verif_expr(expr):
    if is_leaf(expr):
        return True
    if is_op(expr):
        return False
    else:
        operator_check = is_op(op(expr))
        expr_n_check = [verif_expr(expr_n) for expr_n in vals(expr)]
        return all(expr_n_check) and operator_check

#def simplest(expr):
#    '''Renvoie true si on n'a qu'un opérateur et des strings'''
#    operator_check = expr[0] in operators
#    string_check = [isinstance(val, str) for val in expr]
#    return all(string_check) and operator_check

def vals(expr):
    return expr[1:]

def op(expr):
    return expr[0]
    
def apply_f(expr, func):
    return_expr = [op(expr)] + [func(val) for val in vals(expr)]
    return return_expr

def mult(op, *expr):
    assert len(expr)>=2
    assert op in operators_fois
    return [op] + [expr_n for expr_n in expr]
    
def plus(op, *expr):
    assert len(expr)>=2
    assert op in operators_plus
    return [op] + [expr_n for expr_n in expr]
        

def distrib_fois_plus(expr):
    '''transforme [*, [+, a, a2, a3], b, c] en [+, [*, a, b, c], [*, a2, b, c], [*, a3, b, c]]'''
    assert expr[0] in operators_fois
    assert expr[1][0] in operators_plus
    op_fois = op(expr)
    op_plus = op(expr[1])
    return plus(op_plus, *[mult(op_fois, val, *expr[2:]) for val in vals(expr[1])])
    
def associativite_plus(expr):
    '''transforme en plus'''
    if is_leaf(expr):
        return expr
    else:
        if op(expr) in operators_plus:
            return_list = []
            for expr_n in vals(expr):
                if is_leaf(expr_n):
                    return_list += [expr_n]
                elif op(expr_n) == op(expr): # Attention ne distingue pas les feuilles 
                    # Si on a le même opérateur
                    return_list += [associativite_plus(val) for val in vals(expr_n)]
                else:
                    return_list += [associativite_plus(expr_n)]
            return plus(op(expr), *return_list)
        else:
            return_expr = apply_f(expr, associativite_plus)
            return return_expr
            
def associativite_fois(expr):
    '''transforme en plus'''
    if is_leaf(expr):
        return expr
    else:
        if op(expr) in operators_fois:
            return_list = []
            for expr_n in vals(expr):
                if is_leaf(expr_n):
                    return_list += [expr_n]
                elif op(expr_n) == op(expr): # Attention ne distingue pas les feuilles 
                    # Si on a le même opérateur
                    return_list += [associativite_fois(val) for val in vals(expr_n)]
                else:
                    return_list += [associativite_fois(expr_n)]
            return mult(op(expr), *return_list)
        else:
            return_expr = apply_f(expr, associativite_fois)
            return return_expr
