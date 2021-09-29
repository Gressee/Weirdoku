import re
from defines import *
from utils import clamp
import numpy as np
import random


class Game:

    # This class handles all the game logic
    # In here are NO references to kivy widgets
    # The ScrGame creates one instances and then pushes
    # the user inputs to the game via some methods
    # every frame all the grid widgets pull their value from here

    # The ORIGIN of the grid is at the TOP LEFT
    # There are 3 types of cells:
    #   - SUM: Surroundigs must sum up to its value
    #   - HINT: Given to the user to make solveable
    #   - NORMAL: User changes those

    def __init__(self) -> None:
        # The value that the player has selected to fill squares with
        self.selected_value: int = None
        
        # Width and Height of the grid
        self.grid_size = (0, 0)


    ''' CREATE A NEW INSTANCE OF A GAME'''

    def create(self, grid_size: tuple,  game_data: dict=None):
        
        # Id the game data var is set to a dict with a game save
        # then this data is used, but when not a new game is generated

        if game_data == None:
            game_data = self.generate_new(grid_size)
            self.grid_size = grid_size
            self.init_grid()
        else:
            # Reag the game from the dict
            self.grid_size = tuple(game_data[K_GRID_SIZE])
            self.init_grid()
        
        # From the now set game_data set values in the arrays
        for cell in game_data[K_CELLS]:
            x = cell[K_X]
            y = cell[K_Y]
            self.grid_values[y][x] = cell[K_VAL]
            self.grid_types[y][x] = cell[K_TYPE]


    def init_grid(self):
        # Create the arrays that store the values and types

        # Np array that stores the values of the grid cells
        self.grid_values = np.empty((self.grid_size[1], self.grid_size[0]), dtype=int)
        self.grid_values[:] = NO_VALUE
        # Np array that stores the type of a cell
        self.grid_types = np.empty((self.grid_size[1], self.grid_size[0]),  dtype=int)
        self.grid_types[:] = TYPE_NORMAL


    ''' GENERATE A NEW GAME '''

    def generate_new(self, grid_size: tuple) -> dict:
        # This returs a dict and not the arrays, so its later easyer to store
        # and reload games
        
        # TODO make a good generation algorithm which poduces 
        # games with only one solution and without guessing


        # Create temp array
        grid_values = np.empty((grid_size[1], grid_size[0]), dtype=int)
        grid_values[:] = NO_VALUE
        grid_types = np.empty((grid_size[1], grid_size[0]),  dtype=int)
        grid_types[:] = TYPE_NORMAL


        # For now this works like this
        # 1.    Fill grid with random vals
        # 2.    Make a percentage sums and calc their value
        # 3.    Make a percentage hints


        # Set types and values
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                grid_values[y][x] = random.randrange(MIN_GRID_VALUE, MAX_GRID_VALUE+1)

                # Chance for sum
                if random.randrange(0, 11) == 0:
                    grid_types[y][x] = TYPE_SUM
                elif random.randrange(0, 20) == 0:
                    grid_types[y][x] = TYPE_HINT

        # Calc the value of sums
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                if grid_types[y][x] == TYPE_SUM:
                    s = 0
                    for check_x in range(clamp(x-1, 0, grid_size[0]-1), clamp(x+2, 0, grid_size[0]-1)):
                        for check_y in range(clamp(y-1, 0, grid_size[1]-1), clamp(y+2, 0, grid_size[1]-1)):
                            if not grid_types[check_y][check_x] == TYPE_SUM:
                                s += grid_values[check_y][check_x]
                    
                    grid_values[y][x] = s
        
        # Remove the normal cells
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                if grid_types[y][x] == TYPE_NORMAL:
                    grid_values[y][x] = NO_VALUE

        # Make this gris into a dict
        d = {}
        d[K_GRID_SIZE] = grid_size
        d[K_CELLS] = []
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                d[K_CELLS].append(
                    {
                        K_X: x,
                        K_Y: y,
                        K_VAL: grid_values[y][x],
                        K_TYPE: grid_types[y][x]
                    }
                )

        return d


    ''' CHECK IF ITS SOLVED '''

    def check_solved(self) -> bool:
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):

                # Check if this cell even has a value
                if self.get_value(x, y) == NO_VALUE:
                    return False

                # Check the sum square
                if self.get_type(x, y) == TYPE_SUM:
                    s = 0
                    for check_x in range(x-1, x+2):
                        for check_y in range(y-1, y+2):
                            if self.in_bound(check_x, check_y):
                                if not self.get_value(check_x, check_y) == NO_VALUE and not self.get_type(check_x, check_y) == TYPE_SUM:
                                    s += self.get_value(check_x, check_y)
                    print(f'{x}:{y} = {s}')
                    if not s == self.get_value(x, y):
                        return False
                

        return True


    ''' METHODS USED BY WIDGETS '''

    def get_grid_size(self):
        return self.grid_size

    def get_value(self, x, y) -> int:
        if not self.in_bound(x, y): return None
        return self.grid_values[y][x]
    
    def get_type(self, x, y):
        if not self.in_bound(x, y): return None
        return self.grid_types[y][x]
    
    def get_selected_value(self) -> int:
        return self.selected_value
            
    def set_value(self, x, y, value):
        if not self.in_bound(x, y): return
        if self.grid_types[y][x] == TYPE_NORMAL and not value == None:
            self.grid_values[y][x] = value
    
    def set_type(self, x, y, cell_type):
        if cell_type in [TYPE_NORMAL, TYPE_HINT, TYPE_SUM]:
            self.grid_types[y][x] = cell_type

    def set_selected_value(self, value):
        if (value >= MIN_GRID_VALUE and value <= MAX_GRID_VALUE) or value == NO_VALUE:
            self.selected_value = value


    ''' OTHER '''

    def in_bound(self, x, y):
        if x < 0 or x >= self.grid_size[0] or y < 0 or y >= self.grid_size[1]:
            return False
        else:
            return True
    