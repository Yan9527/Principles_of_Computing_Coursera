"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    lst = [0] * len(line)
    lst_idx = 0
    for dummy_entry in line:
        if dummy_entry != 0:
            lst[lst_idx] = dummy_entry
            lst_idx += 1
    for dummy_i in range(0, len(line)-1):
        if lst[dummy_i] == lst[dummy_i+1]:
            lst[dummy_i] *= 2
            if dummy_i == len(line)-2:
                lst[len(line)-1] = 0
            else:
                for dummy_j in range(dummy_i+1, len(line)-1):
                    lst[dummy_j] = lst[dummy_j+1]
                    lst[dummy_j+1] = 0

    return lst

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.reset()
        
        #create initial tiles
        initial_up = []
        initial_down = []
        initial_left = []
        initial_right = []
        
        for dummy_j in range(self.grid_width):
            initial_up.append((0, dummy_j))
        for dummy_j in range(self.grid_width):
            initial_down.append((self.grid_height-1, dummy_j))
        for dummy_i in range(self.grid_height):
            initial_left.append((dummy_i, 0))
        for dummy_i in range(self.grid_height):
            initial_right.append((dummy_i, self.grid_width-1))
            
        #create dictionary for initial tiles
        self.initial_tile_dic = {UP: initial_up, 
                            DOWN: initial_down, 
                            LEFT: initial_left,
                            RIGHT: initial_right}
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.cells = [ [0 for dummy_col in range(self.grid_width)] for dummy_row in range(self.grid_height)]
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return self.cells

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        for dummy_idx in self.initial_tile_dic[direction]:
            line_to_merge = []
            temp_lst = []
            row = dummy_idx[0]
            col = dummy_idx[1]
            while 0 <= row < self.grid_height and 0 <= col < self.grid_width:
                initial_tile_idx = [row, col]
                line_to_merge.append(initial_tile_idx)
                tile_value = self.get_tile(row, col)
                temp_lst.append(tile_value)
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]

            merged_lst = merge(temp_lst)

            for dummy_i in range(len(merged_lst)):
                self.set_tile(line_to_merge[dummy_i][0], line_to_merge[dummy_i][1], merged_lst[dummy_i])

        self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        if random.random() < 0.9:
            new_num = 2
        else:
            new_num = 4
            
        non_empty_lst = []
        selected_idx = []
        for dummy_i in range(self.grid_height):
            for dummy_j in range(self.grid_width):
                if self.cells[dummy_i][dummy_j] == 0:
                    non_empty_lst.append([dummy_i, dummy_j])
        if non_empty_lst != []:
            selected_idx = random.choice(non_empty_lst)
            self.cells[selected_idx[0]][selected_idx[1]] = new_num
        else:
            pass
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.cells[row][col]
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
