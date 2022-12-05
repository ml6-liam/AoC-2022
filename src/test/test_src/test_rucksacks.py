from src.rucksacks import Rucksack, RucksackGroup, make_groups
from src.utils import parse_file_lines

def test_rucksacks():
    rucksack_strings = parse_file_lines('./test/test_data/test_rucksacks.txt')
    rucksack_scores = []
    prio_total = 0
    for rstr in rucksack_strings:
        rucksack = Rucksack(rstr)
        rucksack_scores.append(rucksack.prio_score)
    assert len(rucksack_scores) == 6
    for i in rucksack_scores:
        prio_total += i
    assert prio_total == 157

def test_rucksack_group():
    rucksack_strings = parse_file_lines('./test/test_data/test_rucksacks.txt')
    rgroup_strings = make_groups(rucksack_strings, 3)
    rgroups = []
    prio_total = 0
    for grp in rgroup_strings:
        rgrp = RucksackGroup(grp)
        rgroups.append(rgrp)
        prio_total += rgrp.badge_prio
    assert len(rgroups) == 2
    assert prio_total == 70

def test_make_groups():
    input = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    groups = make_groups(input, 3)
    assert len(groups) == 3
