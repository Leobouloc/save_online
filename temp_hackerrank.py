#!/bin/python

from random import randint

def get_all_points(x, y):
    return [[ix, iy] for ix in range(x) for iy in range(y)]
    
def val(list_xy, grid):
#    print 'list_cy : ', list_xy
    return grid[list_xy[0]][list_xy[1]]

def _get_block(ix, iy, x, y, grid):
    global already_in_block
#    print '\n un tour ...'a
    # Get neighbors
    
    if (ix == 0): 
        if (iy == 0): # Left upper corner
            neighbourghs = [[1,0], [0,1]]
        elif (iy == y-1): # Right upper corner
            neighbourghs = [[0, y-1-1], [1,y-1]]
        else: # Upper middle
            neighbourghs = [[0, iy-1], [0, iy+1], [1, iy]]
    elif (ix == x-1): 
        if (iy == 0): # Left lower corner
            neighbourghs = [[x-1-1,0], [x-1,1]]
        elif (iy == y-1): # Right lower corner
            neighbourghs = [[x-1, y-1-1], [x-1-1,y-1]]
        else: # Lower middle
            neighbourghs = [[x-1, iy-1], [x-1, iy+1], [x-1-1, iy]]
    else:
        if (iy == 0):
            neighbourghs = [[ix, 1], [ix-1, 0], [ix+1, 0]]
        elif (iy == y-1):
            neighbourghs = [[ix, y-1-1], [ix-1, y-1], [ix+1, y-1]]
        else:
            neighbourghs = [[ix + 1, iy], [ix - 1, iy], [ix, iy +1], [ix, iy - 1]]


    # neighbourgs not in blocks
#    print 'ix, iy : ', ix,'/', iy
#    print 'x, y : ', x, y
    neighbourghs_not_in_blocks = [neigh for neigh in neighbourghs if neigh not in already_in_block]
    neighbourghs_not_in_blocks_same = [neigh for neigh in neighbourghs_not_in_blocks if val(neigh, grid) == val([ix, iy], grid)]

    
#    print 'already in block : ', already_in_block
#    print 'not in block : ', neighbourghs_not_in_blocks
#    print 'not in block same : ', neighbourghs_not_in_blocks_same
    
    if len(neighbourghs_not_in_blocks_same) == 0:
        return [ix, iy]
    else:
        already_in_block += neighbourghs_not_in_blocks_same
        return_list = [[ix, iy]] + [_get_block(neigh[0], neigh[1], x, y, grid) for neigh in neighbourghs_not_in_blocks_same]     
        return return_list

def get_block(ix, iy, x, y, grid):
    '''Return coords of points in same block as [ix, iy]'''
    global already_in_block
    already_in_block = [[ix,iy]]
    temp = _get_block(ix, iy, x, y, grid)
    return list(already_in_block)

def get_all_blocks(x, y, grid):
    all_points = get_all_points(x, y)
    all_points = [point for point in all_points if val(point, grid) != '-']
    
    return_list = []
    while len(all_points) != 0:
        
        ix = all_points[0][0]
        iy = all_points[0][1]
        block = get_block(ix, iy, x, y, grid)
        block_val = val([ix, iy], grid)
        block_len = len(block)
        
        block_dict = dict()
        block_dict['points'] = block
        block_dict['len'] = block_len
        block_dict['val'] = block_val
        return_list += [block_dict]        
        
        all_points = [point for point in all_points if not(point in block)]
        
    return return_list
    
def new_grid(block_to_delete, x, y, grid):
    '''Calculates new_grid after deletion of group_to_delete'''
    points_to_delete = block_to_delete['points']
    new_grid = [list(val) for val in grid]
    for point in points_to_delete:
        ix = point[0]
        iy = point[1]
        new_grid[ix][iy] = '-'
    trans_grid = transpose_grid(x, y, new_grid)
    trans_return_grid = []
    for col in trans_grid:
        new_col = [val for val in col if val != '-']
        if len(new_col) > 0:
            new_col = ['-']*(x - len(new_col)) + new_col
            trans_return_grid += [new_col]
    trans_return_grid = trans_return_grid + (y - len(trans_return_grid)) * [x * ['-']]
    return transpose_grid(y,x, trans_return_grid)

    
def transpose_grid(x, y, grid):
    '''returns the grid transposed'''
    return [[grid[ix][iy] for ix in range(x)] for iy in range(y)]

def print_grid(grid):
    for x in grid:
        print x
    
def biggest(x, y, k, grid, counter, first_block = None):
    '''Returns a dict with the list of blocks to play and, the value'''
    '''counter marks the recursive level'''
    nb_best_blocks = 12
    nb_rand_blocks = 5
    
    if all([all([val == '-' for val in ligne]) for ligne in grid]):
        return 0
    if counter == 0:
        blocks = get_all_blocks(x, y, grid)
        max_len = max([block['len'] for block in blocks])
        return max_len
    else:
        blocks = get_all_blocks(x, y, grid)
        blocks = [val for val in blocks if val['len'] > 1]
        blocks.sort(key = lambda x: x['len'], reverse = True)
#        blocks = blocks[:nb_best_blocks]
        to_keep = list(set(range(nb_best_blocks) + [randint(0, len(blocks) - 1) for i in range(nb_rand_blocks)]))
        to_keep = [i for i in to_keep if i < len(blocks)]
        blocks = [blocks[i] for i in to_keep]
        all_values = []
        if len(blocks) == 0:
            return 0
        for block in blocks:
            n_grid = new_grid(block, x, y, grid)
            all_values += [block['len'] + biggest(x, y, k, n_grid, counter - 1)]
        return max(all_values)

def nextMove(x, y, k, grid):
    recursion_level = 3
    nb_best_blocks = 12
    nb_rand_blocks = 5
    
    blocks = get_all_blocks(x, y, grid)
    blocks = [val for val in blocks if val['len'] > 1]
    blocks.sort(key = lambda x: x['len'], reverse = True)
#    blocks = blocks[:nb_best_blocks]
    to_keep = list(set(range(nb_best_blocks) + [randint(0, len(blocks) - 1) for i in range(nb_rand_blocks)]))
    to_keep = [i for i in to_keep if i < len(blocks)]
    blocks = [blocks[i] for i in to_keep]    
    
    best_block = None
    best_val = 0
    for block in blocks:
        n_grid = new_grid(block, x, y, grid)
        profit = block['len'] + biggest(x, y, k, n_grid, recursion_level - 1)
        if profit >= best_val:
            best_val = profit
            best_block = block
    print best_block['points'][0][0], best_block['points'][0][1]
    

if __name__ == '__main__':
#    x,y,k = [ int(i) for i in raw_input().strip().split() ] 
#    grid = [[i for i in str(raw_input().strip())] for _ in range(x)] 
#    nextMove(x, y, k, grid)
    x = 40
    y = 20
    k = 4
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    grid = [['B', 'B', '-'], ['B', 'R', 'R'], ['B', 'B', 'R'], ['R', 'R', 'B']]
    grid = [[letters[randint(0,k)] for iy in range(y)] for ix in range(x)]
    nextMove(x, y, k, grid)

#    next_Move(x, y, k, grid)