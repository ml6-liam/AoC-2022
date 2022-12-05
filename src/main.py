from utils import top_three, parse_file_lines
from elf import Elf
from elf_functions import hungry_elves
from rock_paper_scissors import Strategy
from rucksacks import Rucksack, RucksackGroup, make_groups

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

def all_days():
    d1result = day_1()
    print(f"Day 1 result is {d1result}")
    d2result = day_2()
    print(f"Day 2 result is {d2result}")
    d3result = day_3()
    print(f"Day 3 result is {d3result}")

if __name__ == '__main__':
    d3result = day_3()
    print(f"Day 3 result is {d3result}")
