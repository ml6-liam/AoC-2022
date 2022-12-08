from utils import parse_file_lines
import re

class Stack():
    def __init__(self, id, pos):
        self.id = id
        self.pos = pos
        self.crates=[]

    def add_multiple_crates(self, input_crates:list, rev:bool):
        if rev:
            input_crates.reverse()
        for i,v in enumerate(input_crates):
            self.add_crate_to_top(v)
    
    def add_crate_to_top(self, val):
        self.crates.insert(0, val)
    
    def get_top_n(self, n):
        output = []
        print(f'pop {n} crates from crate list: {self.crates}')
        for i in range(0, n):
            top_val = self.crates.pop(0)
            output.append(top_val)
        return output
    
    def show_crates(self):
        print(self.crates)
    

class CrateStacks():

    def __init__(self, lines):
        break_idx = lines.index('')
        self.crate_state = lines[:break_idx]
        self.crate_instructions = lines[break_idx+1:]
        cs = self.crate_state
        stacks_row = cs[len(cs)-1]
        crate_rows = cs[:len(cs)-1]
        self.stacks = self.parse_stacks(stacks_row)
        self.parse_crates(crate_rows)
        self.parsed_instructions = self.parse_instructions(self.crate_instructions)
        for i, v in enumerate(self.parsed_instructions):
            self.move_crates(v)
        self.crate_message = self.get_top_crates()
        print(f'message from top crate values: {self.get_top_crates()}')


    def parse_stacks(self, stacks_row):
        found_stacks = []
        stacks_row_splits = re.split('', stacks_row)
        for idx, val in enumerate(stacks_row_splits):
            if val not in ['', ' ']:
                found_stacks.append(Stack(val, idx))
        return found_stacks
    
    def parse_crates(self, crate_rows: list):
        crate_rows.reverse()
        for i, crate_row in enumerate(crate_rows):
            crate_row_splits = re.split('', crate_row)
            print(crate_row_splits)
            for stack in self.stacks:
                if stack.pos > len(crate_row_splits):
                    continue
                if (crate_row_splits[stack.pos] not in [' ', '', '[', ']']):
                    stack.add_crate_to_top(crate_row_splits[stack.pos])
    
    def show_stacks(self):
        for stack in self.stacks:
            print(f'Crates in Stack {stack.id} (pos {stack.pos}): {stack.crates}')

    def parse_instructions(self, raw_instructions):
        outputs = []
        for line in raw_instructions:
            inst_splits = re.split(' ', line)
            n = int(inst_splits[1])
            f = int(inst_splits[3])
            t = int(inst_splits[5])
            outputs.append([n, f, t])
        return outputs
    
    def get_top_crates(self):
        message=""
        for stack in self.stacks:
            message += stack.crates[0]
        return message

    def move_crates(self, inst: list):
        n = inst[0]
        f = inst[1]
        t = inst[2]
        fstack = self.stacks[f-1]
        tstack = self.stacks[t-1]
        move_crates = fstack.get_top_n(n)
        tstack.add_multiple_crates(move_crates, rev=False)