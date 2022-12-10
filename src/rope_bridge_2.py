# Head and tail must always be touching
# 
import re
from utils import parse_file_lines

class Marker():
    m_disp: str
    m_pos: tuple # (row, col)
    visited: list
    tail: object

    def __init__(self, disp, tail, start_pos):
        self.m_disp = disp
        self.m_pos = start_pos
        self.visited = [self.m_pos]
        self.tail = tail

    def move(self, r_mag, c_mag, grid):
        prv_row, prv_col = self.m_pos
        new_row = int(prv_row+r_mag)
        new_col = int(prv_col+c_mag)
        self.m_pos = (new_row, new_col)
        if self.tail is not None:
            self.tail.follow(self, grid)

    def mag(self, val):
        if val != 0:
            return val/abs(val)
        else:
            return val
    
    def follow(self, head: object, grid: object):
        head_r, head_c = head.m_pos
        tail_r, tail_c = self.m_pos
        delta_r = head_r - tail_r
        delta_c = head_c - tail_c
        r_mag, c_mag = self.mag(delta_r), self.mag(delta_c)
        if abs(delta_r) > 1 or abs(delta_c) > 1:
            self.move(r_mag, c_mag, grid)
        self.visited.append(self.m_pos)
    
    def num_visited(self):
        return len(set(self.visited))

class Grid():
    grid: list
    height: int
    width: int
    markers: dict
    start_pos: tuple
    def __init__(self, height=5, width=6, num_markers=10, start_pos=(15,11)):
        self.height = height
        self.width = width
        self.markers = {}
        self.start_pos = start_pos
        self.make_markers(num_markers)
    
    def make_markers(self, num_markers):
        markers = []
        prv_marker = None
        for i in reversed(range(num_markers)):
            if i == 0:
                disp = 'H'
            else:
                disp = str(i)
            new_marker = Marker(disp, prv_marker, self.start_pos)
            markers.append((disp, new_marker))
            prv_marker = new_marker
        for disp, marker in markers:
            self.markers[disp] = marker
        
    
    def update_grid(self):
        rows = []
        for i in range(0, self.height):
            new_row = []
            for j in range(0,self.width):
                char = 's' if (i,j)==self.start_pos else '.'
                new_row.append(char)
            rows.append(new_row)
        for disp, marker in self.markers.items():
            rows[int(marker.m_pos[0])%self.height][int(marker.m_pos[1])%self.width] = disp
        self.grid = rows

    def exec_command(self, command):
        print(f'== {command} ==')
        direction, amount = re.split(' ', command)
        r_mags, c_mags = {'D': 1,'U':-1,'L':0,'R':0}, {'D':0,'U':0,'L':-1,'R': 1}
        r_mag, c_mag = r_mags[direction], c_mags[direction]
        for i in range(0, int(amount)):
            self.markers['H'].move(r_mag, c_mag, self)
        self.draw_grid()

    def draw_grid(self):
        self.update_grid()
        for row in self.grid:
            print(self.row_string(row))

    def row_string(self, row):
        s = ''
        for i in row:
            s = f'{s} {i}' if len(s)>=1 else i
        return s


test_input = ["R 5", "U 8", "L 8", "D 3", "R 17", "D 10", "L 25", "U 20"]
puzzle_input = parse_file_lines('./data/rope_commands.txt')
if __name__ =='__main__':
    myg = Grid(21,26,10, (15, 11))
    myg.draw_grid()
    for command in puzzle_input:
        myg.exec_command(command)
    print(myg.markers['9'].num_visited())