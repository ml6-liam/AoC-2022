from utils import top_three, parse_file_lines
from elf import Elf
from elf_functions import hungry_elves
from rock_paper_scissors import Strategy
from rucksacks import Rucksack, RucksackGroup, make_groups
from assignments import AssignmentPair
from stacks import CrateStacks, Stack
from file_system import FileTreeParser

def day_1():
    prd_path = "../data/elf_calories.txt"
    elf_cals = hungry_elves(prd_path)
    top_three_elves, sum = top_three(elf_cals)
    return top_three_elves, sum

def day_2():
    data_path = "./data/rps_strat.txt"
    sguide = parse_file_lines(data_path)
    print(f"found strategy with {len(sguide)} moves")
    my_strat = Strategy(sguide)
    score = my_strat.score_strategy()
    v2_score = my_strat.score_strat_2()
    return score, v2_score

def day_3():
    rstrings = parse_file_lines('./data/rucksacks.txt')
    rucksack_scores = []
    rucksack_groups = make_groups(rstrings, 3)
    prio_total = 0
    for rstr in rstrings:
        rucksack = Rucksack(rstr)
        rucksack_scores.append(rucksack.prio_score)
    for i in rucksack_scores:
        prio_total += i
    badge_prio_total = 0
    for rgroup in rucksack_groups:
        group = RucksackGroup(rgroup)
        badge_prio_total += group.badge_prio
    return prio_total, badge_prio_total

def day_4():
    assignment_strings = parse_file_lines('./data/assignments.txt')
    contains_count = 0
    overlap_count = 0
    for assignment_pair in assignment_strings:
        pair = AssignmentPair(assignment_pair)
        if pair.inclusive_pair():
            contains_count += 1
        if pair.overlap() or pair.inclusive_pair():
            overlap_count += 1
    return contains_count, overlap_count

def all_days():
    d1result = day_1()
    print(f"Day 1 result is {d1result}")
    d2result = day_2()
    print(f"Day 2 result is {d2result}")
    d3result = day_3()
    print(f"Day 3 result is {d3result}")
    d4result = day_4()
    print(f"Day 4 result is {d4result}")

if __name__ == '__main__':
    lines = parse_file_lines('./src/test/test_data/test_fs_cmds.txt')
    parser = FileTreeParser()
    print(f"##### NEW PARSER CREATED #####")
    parser.load_commands(lines)
    print(f"##### COMMANDS LOADED PRINTING EMPTY TREE #####")
    parser.print_tree()
    print(f'##### PARSING {len(parser.commands)} COMMANDS TO GENERATE TREE ####')
    parser.run_commands()



class Human:
    name:str
    parent:object
    children:dict
    def __init__(self, name, parent):
        self.name=name
        self.parent=parent
        self.children={}
    def make_child(self, name):
        child = Human(name, self)
        self.children[name] = child
        return child