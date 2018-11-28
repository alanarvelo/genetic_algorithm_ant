import numpy as np
import random
import json
import copy

from fsa import FSA

class Ant():
    # Ant Class with functionality to create an Ant from an FSA, walk the trail, and return the score.
    # score/fitness = # food eaten in 200 moves.

    direction = ["north", "east","south", "west"]
    dir_row = [-1, 0, 1, 0]
    dir_col = [0, 1, 0, -1]
    

    def __init__(self, genome, max_moves):
        self.max_moves = max_moves
        self.moves = 0
        self.eaten = 0
        self.fenotype = FSA(genome)
        self.current_state = self.fenotype.start_state
        self.memorize_map()

       
    def _reset(self):
        self.row = self.row_start
        self.col = self.col_start
        self.dir = self.fenotype.start_state % 4
        self.moves = 0
        self.eaten = 0
        self.current_state = self.fenotype.start_state
        self.matrix_state = copy.deepcopy(self.matrix)
        self.matrix_exc2 = copy.deepcopy(self.matrix_state)
        
        
    @property
    def position(self):
        return (self.row, self.col, self.direction[self.dir])
    
    def memorize_map(self):
        with  open("./map.json") as trail_file:
            self.matrix = json.load(trail_file)
            self.total_food = sum(map(sum, self.matrix))
            self.matrix = [["." if col == 0 else "X" for col in row] for row in self.matrix]
            self.row_start = self.row = 0
            self.col_start = self.col = 0
            self.matrix_row = len(self.matrix)
            self.matrix_col = len(self.matrix[0])
            self.matrix_state = copy.deepcopy(self.matrix)
            self.matrix_dir = copy.deepcopy(self.matrix)
            
    def turn_left(self):
        self.dir = (self.dir - 1) % 4

    def turn_right(self):
        self.dir = (self.dir + 1) % 4
        
    def move_forward(self):
        self.row = (self.row + self.dir_row[self.dir]) % self.matrix_row
        self.col = (self.col + self.dir_col[self.dir]) % self.matrix_col
        if self.matrix_state[self.row][self.col] == "X":
            self.eaten += 1

    def do_nothing(self):
        pass        
    
    def sense_food(self):
        ahead_row = (self.row + self.dir_row[self.dir]) % self.matrix_row
        ahead_col = (self.col + self.dir_col[self.dir]) % self.matrix_col 
        return self.matrix_state[ahead_row][ahead_col] == "X"
    

    def action_to_take(self, action):
        actions = {
        0: self.do_nothing,
        1: self.turn_right,
        2: self.turn_left, 
        3: self.move_forward,
        }
        return actions[action]
    
    
    def run(self):
        # walk the ant until max_moves or until all food is eaten
        self._reset()
        while (self.moves < self.max_moves) and (self.eaten < self.total_food):
            if self.sense_food():
                self.action_to_take(self.fenotype.actions_food[self.current_state % self.fenotype.num_states ])()
                self.current_state = self.fenotype.new_states_food[self.current_state % self.fenotype.num_states ]
            else:
                self.action_to_take(self.fenotype.actions_no_food[self.current_state % self.fenotype.num_states ])()
                self.current_state = self.fenotype.new_states_no_food[self.current_state % self.fenotype.num_states ]
            self.moves += 1
            self.matrix_state[self.row][self.col] = str(self.current_state)
            self.matrix_dir[self.row][self.col] = str(self.dir)

        return self.eaten
    
    