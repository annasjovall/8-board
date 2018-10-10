# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 12:16:36 2018

@author: AnnaPS

The eight puzzle consists of a 3 x 3 grid with 8 consecutively
numbered tiles arranged on it. One space is left blank so that tiles
can be moved around to form different patterns. The goal is to find a
series of moves of the tiles into the blank space that places in the
board in a goal configuration. A number of different goal states are
used.

"""
import random
import numpy as np
from copy import deepcopy

GOAL_STATE = [[1,2,3], [8,0,4], [7,6,5]]
SIZE = 3
LEFT = 'l'
RIGHT = 'r'
UP = 'u'
DOWN = 'd'
MOVES = [UP, DOWN, LEFT, RIGHT]


def find_zero(state):
    temp = np.array(state)
    row, col = np.where(temp == 0)
    return (row[0], col[0])

def calc_h_merit(state):
    merit = 0
    for row in range(SIZE):
        for col in range(SIZE):
            value = state[row][col]
            if value != 0 and value != GOAL_STATE[row][col]:
                merit += 1
    return merit

class Board:
    """A class representing a board"""
    
    def __init__(self, state, path = []):
        self.state = state
        self.h_merit = calc_h_merit(state)
        self.path = path
        
    def print_board(self):
        for row in range(SIZE):
            print(self.state[row])

"""
Move is given by 'u', 'd', 'l' and 'r' which means move
up, down, left and right respectivly.

Returns the state if it was legal, otherwise return previous state
"""
def move(state, move):
    row_zero, col_zero = find_zero(state)
    if move is UP or move is DOWN:
        new_row = -1
        #Check if legal to move up
        if move is UP and row_zero > 0:
            new_row = row_zero - 1
        #Check if legal to move down
        elif 'd' in move and row_zero < 2:
            new_row = row_zero + 1
        #Return if illegal move
        else:
            return False
        #Move the tile
        state[row_zero][col_zero] =state[new_row][col_zero]
        row_zero = new_row
        state[row_zero][col_zero] = 0
        
    elif move is LEFT or move is RIGHT:
        new_col = -1
        #Check if legal to move left
        if 'l' in move and col_zero > 0:
            new_col = col_zero - 1
        #Check if legal to move right
        elif 'r' in move and col_zero < 2:
            new_col = col_zero + 1
        #Return if illegal move
        else:
            return False
        #Move the tile
        state[row_zero][col_zero] =state[row_zero][new_col]
        col_zero = new_col
        state[row_zero][col_zero] = 0
    return True

def shuffle(n):
    state = deepcopy(GOAL_STATE)
    for i in range(n):
        rand = random.randint(0, 3)
        move(state, MOVES[rand])
    return state

"""
Returns a list of the generated childen
"""
def generate_children(board):
    children = list()
    for m in MOVES:
        new_state = deepcopy(board.state)
        new_path = board.path.copy()
        successful = move(new_state, m)
        #Check if the move was successful, then add to list
        if successful:
            new_path.append(m)
            new_board = Board(new_state, new_path)
            children.append(new_board)
    return children

def sort_by_merit(board_list):
    return sorted(board_list, key=lambda x: x.h_merit)#, reverse=True) 

def state_in_list(board, board_list):
    for b in board_list:
        if board.state == b.state:
            return b
    return None

INIT_STATE = shuffle(10000)
root = Board(INIT_STATE)

print("INITIAL STATE:")
root.print_board() 
print(root.h_merit)
print()

open_state = list()
open_state.append(root)
closed_state = list()
winner = False

while len(open_state) != 0:
    #Remove the left most state from open
    x = open_state.pop(0)
    if x.state == GOAL_STATE:
        print(x.path)
        winner = True
        break
    children = generate_children(x)
    for child in children:
        in_open = state_in_list(child, open_state)
        in_closed = state_in_list(child, closed_state)
        #The child is already in open
        if in_open:
            if len(in_open.path) > len(child.path):
                in_open.path = child.path
        #The child is already in closed
        elif in_closed:
            if len(in_closed.path) > len(child.path):
                closed_state.remove(in_closed)
                open_state.append(child)
        #The child is not in open or closed
        else:
            open_state.append(child)
    closed_state.append(x)
    open_state = sort_by_merit(open_state)
if winner:
    print("You Won! Woho!")
else:
    print("FAIL")
                