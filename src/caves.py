import re
import sys
from utils import parse_file_lines
from time import sleep
from reprint import output

class SandGrain():
    def __init__(self, cave):
        self.cave = cave
        self.abyss = False
        self.pos = self.cave.start_point
    
    def move(self):
        cave = self.cave
        curr_row, curr_col = self.pos
        below = (curr_row + 1, curr_col)
        below_left = (curr_row+1, curr_col-1)
        below_right = (curr_row+1, curr_col+1)
        if cave.in_grid(below): 
            if cave.grid_point(below) == '.':
                self.update_grid(self.pos, below)
                return True
            elif cave.grid_point(below) in ['#','o']:
                if cave.in_grid(below_left): 
                    if cave.grid_point(below_left) == '.':
                        self.update_grid(self.pos, below_left)
                        return True
                    elif cave.grid_point(below_left) in ['#','o']:
                        if cave.in_grid(below_right): 
                            if cave.grid_point(below_right) == '.':
                                self.update_grid(self.pos, below_right)
                                return True
                            elif cave.grid_point(below_left) in ['#','o']:
                                return False
                        else:
                            self.abyss = True
                            return False
                else:
                    self.abyss = True
                    return False
        else:
            self.abyss = True
            return False

    def update_grid(self, old_pos, new_pos):
        self.cave.grid[old_pos[0]][old_pos[1]] = '.'
        self.cave.grid[new_pos[0]][new_pos[1]] = 'o'
        self.pos = new_pos


class Cave():
    def __init__(self):
        self.map = []
        self.rock_lines = []
        self.max_row = 0
        self.min_row = 0
        self.min_col = float('inf')
        self.max_col = 0
        self.start_point = (0, 500)
        self.grid = []
    
    def grid_point(self, point:tuple):
        return self.grid[point[0]][point[1]]
    
    def in_grid(self, pos):
        new_row, new_col = pos
        if new_col < self.min_col or new_col > self.max_col:
            return False
        elif new_row < self.min_row or new_row > self.max_row:
            return False
        return True

    def parse_rock_lines(self, input, with_floor=False):
        for line in input:
            coords = re.split(' -> ', line)
            for i in range(len(coords)-1):
                start = coords[i]
                end = coords[i+1]
                scol, srow = re.split(',', start)
                scol, srow = int(scol), int(srow)
                ecol, erow = re.split(',', end)
                ecol, erow = int(ecol), int(erow)
                self.rock_lines.append(((srow, scol), (erow, ecol)))
                if max(scol, ecol) > self.max_col:
                    self.max_col = max(scol, ecol)
                if max(srow, erow) > self.max_row:
                    self.max_row = max(srow, erow)
                if min(scol, ecol) < self.min_col:
                    self.min_col = min(scol, ecol)
        if with_floor:
            base = 1+(2*self.max_row)
            self.rock_lines.append(((self.max_row+2, self.start_point[1]-base), (self.max_row+2, self.start_point[1]+base)))
            self.max_row += 2
            self.min_col = self.start_point[1]-base
            self.max_col = self.start_point[1]+base
        self.normalise_coords()
        self.grid = self.gen_grid()
        self.draw_rocks_to_grid()
    
    def normalise_coords(self):
        output_buffer = []
        min_col = self.min_col
        for line in self.rock_lines:
            start, end = line
            srow, scol = start
            erow, ecol = end
            output_buffer.append(((srow, scol-min_col),(erow, ecol-min_col)))
        self.max_col = self.max_col-min_col
        self.min_col = self.min_col-min_col
        sprow, spcol = self.start_point
        self.start_point = (sprow, spcol-min_col)
        self.rock_lines = output_buffer
    
    def gen_grid(self):
        grid = []
        start_row, start_col = self.start_point
        for i in range(self.min_row, self.max_row+1):
            row = []
            for j in range(self.min_col, self.max_col+1):
                if i == start_row and j == start_col:
                    char = '+'
                else:
                    char = '.'
                row.append(char)
            grid.append(row)
        return grid
    
    def draw_grid(self):
        for idx, row in enumerate(self.grid):
            ids = str(idx)
            if len(ids)==2:
                ids = '0'+ids
            elif len(ids)==1:
                ids = '00'+ids
            row_str = f'{ids} '
            for val in row:
                row_str = row_str+val
            print(row_str)
    
    def draw_grid_to_dict(self):
        out = {}
        for idx, row in enumerate(self.grid):
            ids = str(idx)
            if len(ids)==2:
                ids = '0'+ids
            elif len(ids)==1:
                ids = '00'+ids
            row_str = f''
            for val in row:
                row_str = row_str+val
            out[ids] = row_str
        return out
            

    def draw_rocks_to_grid(self):
        for line in self.rock_lines:
            start, end = line
            srow, scol = start
            erow, ecol = end
            min_row, max_row = min(srow,erow), max(srow, erow)+1
            min_col, max_col = min(scol,ecol), max(scol,ecol)+1
            for i in range(min_row, max_row):
                for j in range(min_col, max_col):
                    self.grid[i][j] = '#'

 
if __name__=='__main__':
    input = parse_file_lines('./data/rocks.txt')
    cave = Cave()
    cave.parse_rock_lines(input, with_floor=True)
    breaker = False
    resting_grains = 0
    print_per_it = False
    final = True
    while not breaker:
        grain = SandGrain(cave)
        moving_grain = True
        while moving_grain:
            moving_grain = grain.move()
            if print_per_it:
                cave.draw_grid()
                print('='*cave.max_col)
        if not print_per_it and not final:
            cave.draw_grid()
            print('='*cave.max_col)
        if grain.pos == cave.start_point:
            breaker = True
        if not breaker:
            resting_grains +=1
    if final == True:
        cave.draw_grid()
        print('='*cave.max_col)

    
    print(f'Number of Grains that came to rest: {resting_grains}')


    