from utils import parse_file_lines
import re
import sys


class GridPoint():
    def __init__(self, value,
                 grid, row, col, 
                 start_point, end_point):
        self.value = value
        self.grid = grid
        self.shortest_path = float('inf')
        self.start_point = start_point
        self.end_point = end_point
        self.pos = (row, col)
        self.connections = []
        self.visited = False
        self.previous = (0,0)

    def update_connections(self):
        row, col = self.pos
        for i, j in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if (0 <= i <= self.grid.height-1) and (0<=j<=self.grid.width-1):
                neighbour = self.grid.points[(i,j)]  
                if 0 <= ord(neighbour.value)-ord(self.value) <= 1:
                    self.connections.append(neighbour)
        #self.grid.points[self.pos] = self       
        #print(f'Found {len(self.connections)} connections for point at {self.pos}')
        return self
    
    def describe(self):
        print(f'point with val {self.value} at pos {self.pos} with connections: {[point.pos for point in self.connections]}')
    
    def find_forward_path(self, searched_path):
        self.visited = True
        print(f'visit point at {self.pos}')
        self.shortest_path = len(searched_path+[self.pos])
        for point in self.connections:
            if not point.visited:
                if (len(searched_path+[point.pos]) < point.shortest_path):
                    print(f'new shortest path found for {point.pos}')
                    point.find_forward_path(searched_path)

        

class Grid():
    def __init__(self):
        self.point_grid = []
        self.points = {}
        self.width, self.height = 0, 0
        self.search_limit = 0
        self.start_point_pos = None
        self.end_point = None
        self.value_grid = []
        self.visited = []
        self.edges = {}

    def parse_value_grid(self, input):
        value_grid = []
        self.height = len(input)
        for line in input:
            row = re.split('', line)[1:-1]
            self.width = len(row)
            value_grid.append(row)
        self.search_limit = self.width*self.height
        self.value_grid = value_grid

    def find_grid_points(self):
        for row_id, row in enumerate(self.value_grid):
            output_row = []
            for col_id, val in enumerate(row):
                if val == 'S':
                    val = 'a'
                    point = GridPoint(val, self, row_id, col_id, True, False)
                    point.shortest_path = 0
                    self.start_point_pos = point.pos
                if val == 'E':
                    val = 'z'
                    point = GridPoint(val, self, row_id, col_id, False, True)
                    self.end_point_pos = point.pos
                else:
                    point = GridPoint(val, self, row_id, col_id, False, False)
                self.points[(row_id, col_id)] = point
                #output_row.append(point)
            #self.point_grid.append(output_row)
    
    def update_grid_connections(self):
        for point, point_obj in self.points.items():
                ret_obj = point_obj.update_connections()
                if ret_obj.start_point:
                    print('updated start point')
                    self.start_point = ret_obj
                self.points[point] = ret_obj
        for point_pos, point_obj in self.points.items():
            for neighbour in point_obj.connections:
                self.edges[point_pos][neighbour.pos] = 1
    
    def describe(self):
        print(f'current points')
        for point, point_obj in self.points.items():
            point_obj.describe()
        print(f'start point')
        self.points[self.start_point_pos].describe()
        print(f'end point')
        self.points[self.end_point_pos].describe()
    
    def find_paths(self):
        self.points[self.start_point_pos].find_forward_path(searched_path=[])
        print(self.points[self.end_point_pos].shortest_path)
    
if __name__ == '__main__':
    input = parse_file_lines('./data/signal_map.txt')
    grid = Grid()
    grid.parse_value_grid(input)
    print('Grid Parsed - finding points')
    grid.find_grid_points()
    print('points found - update connections')
    grid.update_grid_connections()
    print('Connections found - describe points')
    grid.describe()
    print('find paths')
    grid.find_paths()