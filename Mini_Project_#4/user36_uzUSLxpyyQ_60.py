"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list) 
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for item in self._zombie_list:
            yield item

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for item in self._human_list:
            yield item
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        height = self.get_grid_height()
        width = self.get_grid_width()
        visited = poc_grid.Grid(height, width)
        for dummy_i in range(height):
            for dummy_j in range(width):
                if not self.is_empty(dummy_i, dummy_j):
                    visited.set_full(dummy_i, dummy_j)             
        distance_field = [[height * width for dummy_col in range(width)]
                          for dummy_row in range(height)]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for dummy_i in self.zombies():
                boundary.enqueue(dummy_i)
        elif entity_type == HUMAN:
            for dummy_i in self.humans():
                boundary.enqueue(dummy_i)
        for item in boundary:
            visited.set_full(item[0], item[1])
            distance_field[item[0]][item[1]] = 0
        while len(boundary) != 0:
            cell = boundary.dequeue()
            neighbors = self.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1
                    boundary.enqueue(neighbor)
        return distance_field
 
                    
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        humans_move_to = []
        for dummy_i in self._human_list:
            neighbors = self.eight_neighbors(dummy_i[0], dummy_i[1])
            for neighbor in neighbors:
                if not self.is_empty(neighbor[0], neighbor[1]):
                    neighbors.remove(neighbor)
            neighbors.append(dummy_i)
            distance_lst = []
            cell_lst = []
            for neighbor in neighbors:
                distance_lst.append(zombie_distance[neighbor[0]][neighbor[1]])
            for neighbor in neighbors:
                if zombie_distance[neighbor[0]][neighbor[1]] == max(distance_lst):
                    cell_lst.append(neighbor)
            humans_move_to.append(random.choice(cell_lst))   
        self._human_list = []
        for to_cell in humans_move_to:
            self.add_human(to_cell[0], to_cell[1])

    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombies_move_to = []
        for dummy_i in self._zombie_list:
            if dummy_i in self._human_list:
                zombies_move_to.append(dummy_i)
            else:
                neighbors = self.four_neighbors(dummy_i[0], dummy_i[1])
                distance_lst = []
                cell_lst = []
                for neighbor in neighbors:
                    distance_lst.append(human_distance[neighbor[0]][neighbor[1]])
                for neighbor in neighbors:
                    if human_distance[neighbor[0]][neighbor[1]] == min(distance_lst):
                        cell_lst.append(neighbor)
                zombies_move_to.append(random.choice(cell_lst))
        self._zombie_list = []
        for to_cell in zombies_move_to:
            self.add_zombie(to_cell[0], to_cell[1])


poc_zombie_gui.run_gui(Zombie(30, 40))
