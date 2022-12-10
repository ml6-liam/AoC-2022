from utils import parse_file_lines
import re

class CathodeCommander():
    input: list
    output: dict = {'20':0, '60':0, '100':0, '140':0, '180':0, '220':0 }
    buffer = dict
    current_row: list
    output_rows: list
    cathode_pixel: int
    cathode_row: list

    def __init__(self, input: list):
        self.input = input
        self.buffer ={}
        self.output_rows = []
        self.cathode_row = []
        
    def executor(self):
        self.cathode_pixel = 0
        sprite_val = 1
        self.current_row = self.new_row()
        cycle = 0
        for command in self.input:
            print(f'Sprite Position: {self.sprite_row(sprite_val)}')
            print(' ')
            cycle += 1
            print(f'Start of cycle {cycle}: begin executing {command}')
            if command == 'noop':
                self.eval_cycle(sprite_val, cycle)
                print(f'End of Cycle {cycle}: finish executing {command}')
            else:
                _, val = re.split(' ', command)
                self.eval_cycle(sprite_val, cycle)
                self.cathode_pixel +=1
                cycle += 1
                print(' ')
                self.eval_cycle(sprite_val, cycle)
                sprite_val += int(val)
                print(f'End of cycle {cycle}: finish executing {command} (Register X is now at {sprite_val})')
            self.cathode_pixel +=1 
        self.output_rows.append(self.current_row)
        self.print_image()
                
    def eval_cycle(self, sprite_val, cycle):
        self.cathode_length()
        print(f'During cycle {cycle}: CRT Draws pixel at position {self.cathode_pixel}')
        self.add_to_cathode_row()
        print(f'Current CRT Row: {self.print_row(self.cathode_row)}')
        sprite_pixels = [sprite_val-1, sprite_val, sprite_val+1]
        if (self.cathode_pixel in sprite_pixels): # (self.cathode_pixel%4 <= 1) and  
            self.current_row[self.cathode_pixel] = '#'
    
    def add_to_cathode_row(self):
        if self.cathode_pixel%4 <= 1:
            self.cathode_row.append('#')
        else:
            self.cathode_row.append('.') 

    def cathode_length(self):
        if self.cathode_pixel == 40:
            print("new row")
            self.output_rows.append(self.current_row)
            self.current_row = self.new_row()
            self.cathode_pixel = 0
            self.cathode_row = []

    def new_row(self):
        return ['.' for i in range(0, 40)]

    def sprite_row(self, sprite_val):
        row_to_print = self.new_row()
        sprite_locs = [sprite_val-1,sprite_val,sprite_val+1]
        for i in sprite_locs:
            if 0 <= i <= 39:
                row_to_print[i] = '#'
        return self.print_row(row_to_print)

    def print_row(self, row):
        output_s = ''
        for i in row:
            output_s += str(i)
        return output_s

    def print_image(self):
        for row in self.output_rows:
            print(self.print_row(row))

        
if __name__ == '__main__':
    test_input = parse_file_lines('./data/cathode_commands.txt')
    cathode_commander = CathodeCommander(test_input)
    cathode_commander.executor()

