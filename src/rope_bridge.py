# Head and tail must always be touching
# 
import re
from utils import parse_file_lines

class Marker():
    m_disp: str
    m_pos: tuple # (row, col)

    def move(self, r_mag, c_mag, grid):
        prv_row, prv_col = self.m_pos
        new_row = int(prv_row+r_mag)
        new_col = int(prv_col+c_mag)
        self.m_pos = (new_row, new_col)

    def mag(self, val):
        if val != 0:
            return val/abs(val)
        else:
            return val

class Tail(Marker):
    visited: list
    def __init__(self):
        self.m_disp = 'T'
        self.m_pos = (4,0)
        self.visited = [self.m_pos]
    
    def update_tail(self, head: object, grid: object): #, move_mag):
        head_r, head_c = head.m_pos
        tail_r, tail_c = self.m_pos
        delta_r = head_r - tail_r
        delta_c = head_c - tail_c
        r_mag, c_mag = self.mag(delta_r), self.mag(delta_c)
        if abs(delta_r) > 1 or abs(delta_c) > 1:
            self.move(r_mag, c_mag, grid)
        grid_pos = (self.m_pos[0]%grid.height, self.m_pos[1]%grid.width)
        self.visited.append(self.m_pos) #grid_pos)
    
    def num_visited(self):
        return len(set(self.visited))
        

class Head(Marker):
    def __init__(self):
        self.m_disp = 'H'
        self.m_pos = (4,0)

class Grid():
    head: object
    tail: object
    grid: list
    height: int
    width: int
    def __init__(self, height=5, width=6):
        self.head = Head()
        self.tail = Tail()
        self.height = height
        self.width = width
    
    def update_grid(self):
        rows = []
        for i in range(0, self.height):
            new_row = []
            for j in range(0,self.width):
                char = 's' if (i,j)==(4,0) else '.'
                new_row.append(char)
            rows.append(new_row)
        head_pos, tail_pos = self.head.m_pos, self.tail.m_pos
        rows[int(tail_pos[0])%self.height][int(tail_pos[1])%self.width] = self.tail.m_disp
        rows[int(head_pos[0])%self.height][int(head_pos[1])%self.width] = self.head.m_disp
        self.grid = rows

    def exec_command(self, command):
        print(f'== {command} ==')
        direction, amount = re.split(' ', command)
        r_mags, c_mags = {'D': 1,'U':-1,'L':0,'R':0}, {'D':0,'U':0,'L':-1,'R': 1}
        r_mag, c_mag = r_mags[direction], c_mags[direction]
        #move_mag = r_mag if r_mag !=0 else c_mag
        for i in range(0, int(amount)):
            self.head.move(r_mag, c_mag, self)
            self.tail.update_tail(self.head, self)#, move_mag)
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


test_input = ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]
puzzle_input = parse_file_lines('./data/rope_commands.txt')
if __name__ =='__main__':
    myg = Grid()
    myg.draw_grid()
    for command in puzzle_input:
        myg.exec_command(command)
    print(myg.tail.num_visited())