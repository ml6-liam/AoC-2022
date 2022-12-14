from utils import parse_file_lines
import re
import sys

class GridPoint():
    def __init__(self, value,
                 grid, row, col, 
                 start_point:bool=False, end_point:bool=False):
        self.value = value
        self.grid = grid
        self.start_point = start_point
        self.end_point = end_point
        self.pos = (row, col)
        self.connections = []
        self.parents = []
        self.connected_to_end = False
        #print(f'created point with val {self.value} at {self.pos} - is start: {self.start_point} - is end: {self.end_point}')
    
    def describe(self):
        print(f'point at pos {self.pos} with connections: {[point.pos for point in self.connections]}, and parents: {[point.pos for point in self.parents]}')
    
    def test_path(self, current_route):
        return 0

    def update_connections(self):
        #print(f'find connections from pos {self.pos}')
        self.grid.visited.append(self.pos)
        row, col = self.pos
        for i, j in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if (0 <= i <= self.grid.height-1) and (0<=j<=self.grid.width-1):
                is_connection = (i,j) in [point.pos for point in self.connections]
                is_parent = (i,j) in [point.pos for point in self.parents]
                visited = (i,j) in self.grid.visited
                if  (not is_connection) and (not is_parent) and (not visited):  
                    #print(f'checking neighbour at ({i}, {j})')
                    if (i,j) in self.grid.grid_point:
                        neighbour = self.grid.grid_point[(i,j)]
                    else:
                        neighbour_val = self.grid.value_grid[i][j]
                        neighbour_end = (neighbour_val == 'E')
                        neighbour = GridPoint(neighbour_val, self.grid, i, j, False, neighbour_end)
                        self.grid.grid_point[(i,j)] = neighbour
                        if neighbour_end:
                            self.grid.end_point = neighbour
                    if 0 <= ord(neighbour.value)-ord(self.value) <= 1:
                        self.connections.append(neighbour)
                        neighbour.parents.append(self)
        print(f'Found {len(self.connections)} connections for point at {self.pos}')
        for neighbour in self.connections:
            neighbour.find_connections()
    
    def search_connections(self, search_depth, prv_point) -> list:
        onward_paths = []
        search_depth += 1
        #print(f'searching {self.pos}, current depth: {search_depth}')
        if search_depth < self.grid.search_limit:
            for point in self.connections:
                if point != prv_point:
                    if point.end_point:
                        #print('found end!')
                        onward_paths.append([self.value, point.value])
                    else:
                        returned_paths = list(point.search_connections(search_depth, self))
                        if len(returned_paths) > 0:
                            for path in returned_paths:
                                onward_paths.append([self.value]+path)
        return onward_paths

    def propagate_connection(self):
        self.connected_to_end = True
        for point in self.parents:
            point.propagate_connection()
    
    def prune_connections(self):
        pruned_connections = []
        for point in self.connections:
            if point.connected_to_end:
                pruned_connections.append(point)



class Grid():
    def __init__(self):
        self.grid_point = {}
        self.width, self.height = 0, 0
        self.search_limit = 0
        self.start_point = None
        self.end_point = None
        self.value_grid = []
        self.visited = []

    def parse_value_grid(self, input):
        value_grid = []
        self.height = len(input)
        for line in input:
            row = re.split('', line)[1:-1]
            self.width = len(row)
            value_grid.append(row)
        self.value_grid = value_grid
        sys.setrecursionlimit(self.height*self.width)
    
    def find_start(self):
        for row_id, row in enumerate(self.value_grid):
            for col_id, val in enumerate(row):
                if val == 'S':
                    print(f'found start at ({row_id}, {col_id})')
                    self.start_point = GridPoint('a', self, row_id, col_id, True, False)
                    self.grid_point[(row_id, col_id)] = self.start_point
    
    def find_connections(self):
        self.start_point.find_connections()
    
    def find_grid_points(self, input):
        for idx, line in enumerate(input):
            row = re.split('', line)[1:-1]
            output_row = []
            for col, val in enumerate(row):
                if val == 'S':
                    point = GridPoint(val, self, idx, col, True, False)
                    self.start_point = point
                if end_point:
                    self.end_point = point
                output_row.append(point)
            self.grid.append(output_row)
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.search_limit = self.width*self.height
        sys.setrecursionlimit(1000)
        self.update_connections()
        self.describe()
        self.end_point.propagate_connection()
        self.prune_connections()

    def grid_search(self): 
        print(f'searching with depth limit {self.search_limit}')
        paths = self.start_point.search_connections(0, self.start_point)
        #print(paths)
        shortest_path = []
        for path in paths:
            if len(path)>1:
                if len(shortest_path)==0 or (len(path) < len(shortest_path)):
                    shortest_path = path
        print(f'shortest route to summit ({len(shortest_path)-1} steps): {shortest_path}')
    
    def describe(self):
        print(f'current points')
        for pos, point in self.grid_point.items():
            point.describe()
    
    def update_connections(self):
        for row_id, row in enumerate(self.grid):
            for col_id, col in enumerate(row):
                self.grid[row_id][col_id].update_connections()

    def prune_connections(self):
        for row_id, row in enumerate(self.grid):
            for col_id, col in enumerate(row):
                self.grid[row_id][col_id].prune_connections()

if __name__ == '__main__':
    input = parse_file_lines('./data/signal_map.txt')
    grid = Grid()
    grid.parse_value_grid(input)
    print('Grid Parsed - finding start')
    grid.find_start()
    print('start found - find connections from start')
    grid.find_connections()
    print('Connections found')
    grid.describe()
  #  grid.grid_search()