from utils import parse_file_lines
import re
from numpy import floor
import time
import math

class Monkey():
    items: list
    operation: str
    test_val: int
    band: object
    f_monkey: str
    t_monkey: str
    inspections: int
    
    def __init__(self, 
                 starting_items: list,
                 operation: str,
                 test_val: int,
                 f_monkey: str,
                 t_monkey: str,
                 band: object):
        self.items = starting_items
        self.operation = operation
        self.test_val = test_val
        self.band = band
        self.f_monkey, self.t_monkey = f_monkey, t_monkey
        self.inspections = 0

    def worry_test(self, worry_level: int):
        return (worry_level%self.test_val==0)

    def run_operation(self, worry_level: int):
        old=worry_level
        op = re.split('= ', self.operation)[1]
        op = op.replace('old', str(old))
        #print(f'worry level pre op: {old}')
        #print(f'execute operation: {op}')
        new=eval(op)
        #print(f'new = {new}')
        new %= self.band.test_prod
        if self.worry_test(new):
            self.band.monkeys[self.t_monkey].throw(new)
        else:
            self.band.monkeys[self.f_monkey].throw(new)
    
    def throw(self, new_val):
        self.items.append(new_val)
    
    def play_round(self):
        while len(self.items) > 0:
            worry_level = self.items.pop(0)
            self.run_operation(worry_level)
            self.inspections += 1
    
    def monkey_items(self):
        s=''
        for item in self.items:
            s+=f'{item}, '
        return s

class Band():
    monkeys: dict
    init_state: list
    test_prod: int

    def __init__(self, input: list):
        self.monkeys={}
        self.init_state = input
        self.monkey_parser(input)
        self.test_prod = self.test_product()
    
    def test_product(self):
        vals = [monkey.test_val for mnum, monkey in self.monkeys.items()]
        out = vals[0]
        for val in vals[1:]:
            out = out * val
        return out

    def monkey_parser(self, input: list):
        while len(input)>0:
            line = input.pop(0)
            if line[:6]=='Monkey':
                monkey_num = line[7]
                monkey_attr = []
                while len(input)>0 and input[0][:6]!='Monkey':
                    monkey_attr.append(input.pop(0))
                self.add_monkey_to_band(monkey_num, monkey_attr)
    
    def re_init(self):
        self.monkeys = {}
        self.monkey_parser(self.init_state)
                
    def add_monkey_to_band(self, monkey_num, monkey_attr):
        for attr in monkey_attr:
            print(attr)
            if 'Starting items' in attr:
                items = self.s_item_parser(attr)
                #print(f'parsed items: {items}')
            elif 'Operation' in attr:
                operation = re.split(': ', attr)[1]
                #print(f'parsed operation: {operation}')
            elif 'Test' in attr:
                test_val = int(attr[-2:])
                #print(f'parsed test val: {test_val}')
            elif 'If true' in attr:
                t_monkey = re.split('throw to monkey ', attr)[1]
                #print(f'parsed true monkey: {t_monkey}')
            elif 'If false' in attr:
                f_monkey = re.split('throw to monkey ', attr)[1]
                #print(f'parsed false monkey: {f_monkey}')
        new_monkey = Monkey(items, operation, test_val, f_monkey, t_monkey, self)
        self.monkeys[monkey_num] = new_monkey

    def s_item_parser(self, line):
        nums = re.split(': ', line)[1]
        return [int(n) for n in re.split(', ', nums)]
    
    def play_monkey_games(self, rounds):
        for i in range(1,rounds+1):
            print(f'Round {i}')
            start_time = time.time()
            for m_num, monkey in self.monkeys.items():
                monkey.play_round()
            print(f'Round {i} finished in {time.time()-start_time} seconds')
            print('#.#.#.#.#.#.#.#')
            #print(f'After round {i}, the monkeys are holding the following items:')
            #self.list_monkey_items()
            #print(f'....')
        print('Monkey Inspection Stats:')
        self.print_inspections()
        print(f'Monkey Business Score: {self.monkey_business_score()}')
    
    def monkey_business_score(self):
        f_active = 0
        s_active = 0
        for num, monkey in self.monkeys.items():
            i = monkey.inspections
            if i >= f_active:
                s_active = f_active
                f_active = i
            elif i > s_active:
                s_active = i
        return f_active * s_active

    def print_inspections(self):
        for num, monkey in self.monkeys.items():
            print(f'Monkey {num} inspected items {monkey.inspections} times')

    def list_monkey_items(self):
        for m_num, monkey in self.monkeys.items():
            print(f'Monkey {m_num}: {monkey.monkey_items()}')


if __name__ == '__main__':
    input_file = './data/monkeys.txt'
    input = parse_file_lines(input_file)
    gorillaz = Band(input)
    gorillaz.play_monkey_games(10000) 
