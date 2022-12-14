from utils import parse_file_lines
import re
import time
class Vertex():
    def __init__(self, pos, val, grid):
        self.visited = False
        self.pos = pos
        self.distance = float('inf')
        if val == 'S':
            val = 'a'
        elif val == 'E':
            val = 'z'
        self.value = val
        self.grid = grid
    
    def update_connections(self):
        row, col = self.pos
        for i, j in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if (0 <= i < self.grid.height) and (0<=j<self.grid.width):
                neighbour = self.grid.vertices[(i,j)]  
                if ord(neighbour.value)-ord(self.value) <= 1:
                    self.grid.edges[self.pos][neighbour.pos] = 1
    
    def get_distance(self):
        return self.distance

class Graph():
    def __init__(self):
        self.edges = {}
        self.vertices = {}
        self.start_pos = None
        self.end_pos = None
        self.height = 0
        self.width = 0

    def parse_input(self, input):
        self.height = len(input)
        self.width = len(input[0])
        for row_id, row in enumerate(input):
            for col_id, val in enumerate(re.split('', row)[1:-1]):
                new_vertex = Vertex((row_id, col_id), val, self)
                self.edges[(row_id, col_id)] = {}
                if val == 'S':
                    self.start_pos = (row_id, col_id)
                elif val == 'E':
                    self.end_pos = (row_id, col_id)
                self.vertices[(row_id, col_id)]  = new_vertex
        print(f'found {len(self.vertices)} points - updating connections')
        for vertex_pos, vertex in self.vertices.items():
            vertex.update_connections()
        print(f'connections updated - fill empty connections in edges dict')
        #for vertex1_pos in self.vertices:
        #    for vertex2_pos in self.vertices:
        #        if vertex1_pos != vertex2_pos:
        #            if vertex2_pos not in self.edges[vertex1_pos]:
        #                self.edges[vertex1_pos][vertex2_pos] = 0

    def get_distance(distance, vertex):
        return distance
    
    def get_start_points(self):
        output = []
        for vertex_pos, vertex in self.vertices.items():
            if vertex.value == 'a':
                output.append(vertex_pos)
        print(f'Found {len(output)} possible start points')
        return output

    def dijkstras(self, start_point):
        vertex_queue = []
        vertex_queue.append((0, start_point))
        self.vertices[start_point].distance = 0

        while len(vertex_queue) > 0:
            vertex_queue.sort()
            distance, vertex_pos = vertex_queue.pop(0)
            #print(f'Visit Vertex at point {vertex_pos}')
            vertex = self.vertices[vertex_pos]
            vertex.visited=True
            for neighbour_pos, con_len in self.edges[vertex.pos].items():
                if con_len == 1:
                    #print(f'    Consider neighbour ar point {neighbour_pos}')
                    neighbour = self.vertices[neighbour_pos]
                    if not neighbour.visited:
                        old_cost = neighbour.distance
                        new_cost = vertex.distance + con_len
                        if new_cost < old_cost:
                            #print(f'        new distance shortest found: {new_cost}')
                            neighbour.distance = new_cost
                            vertex_queue.append((new_cost, neighbour.pos))
        path_len = self.vertices[self.end_pos].distance
        self.reset_vertices()
        print(f'Shortest Distance to end point at {self.end_pos} from start point at {start_point} is {path_len}')
        return path_len
    
    def multiple_starts(self):
        shortest_paths = {}
        shortest_path = float('inf')
        start_points = self.get_start_points()
        closest_point = None
        for point in start_points:
            path_len = self.dijkstras(point)
            if path_len < shortest_path:
                shortest_path = path_len
                closest_point = point
            if path_len != float('inf'):
                shortest_paths[point] = self.dijkstras(point)
        print(f'Found the following paths from {len(start_points)} start points:')
        for point, path_len in shortest_paths.items():
            print(f'    {point}: {path_len}')
        print(f'The shortest path of all was from point {closest_point} with length {shortest_path}')
        return shortest_paths
    
    def single_start(self):
        shortest_path = self.dijkstras(self.start_pos)
        print(f'Shortest path from start point {self.start_pos} is {shortest_path}')
        #self.reset_distances()
    
    def reset_vertices(self):
        print('Reset distances for all vertices')
        for vertex_pos, vertex in self.vertices.items():
            vertex.distance = float('inf')
            vertex.visited = False
        print(f'Reset complete')
        return 1

    def unvisited(self):
        print(f'The following points were not visited by the algo')
        for vertex_pos, vertex in self.vertices.items():
            if not vertex.visited:
                print(f'Vertex at {vertex_pos}')
    
    def print_edges(self):
        for node, connections in self.edges.items():
            print(f'Vertex at point {node} has {len(connections)} connections: ')
            print(f'    {connections}')
    
    def show_visited(self):
        output = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                ind = 0
                if self.vertices[(i,j)].visited:
                    ind = 1
                if (i,j) == self.end_pos:
                    ind = 3
                row.append(ind)
            output.append(row)
        for row in output:
            print(row)


if __name__ == '__main__':
    input = parse_file_lines('./data/signal_map.txt')
    graph = Graph()
    graph.parse_input(input)
    graph.single_start()
    graph.multiple_starts()
    #graph.show_visited()

