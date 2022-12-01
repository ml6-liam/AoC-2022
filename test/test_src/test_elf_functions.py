from src.elf_functions import hungry_elves
from src.utils import top_three, parse_file_lines
from src.elf import Elf

def test_hungry_elves():
    assert hungry_elves("./test/test_data/test_elf_calories.txt") == [6000, 4000, 11000, 24000, 10000]

def test_top_three():
    test_list = [1,2,3,4,5,6]
    exp_list = [6,5,4]
    exp_val = 15
    acc_list, acc_val = top_three(test_list)
    assert acc_list == exp_list
    assert acc_val == exp_val

def test_parse_file_lines():
    lines = parse_file_lines("./test/test_data/test_lines.txt")
    assert lines == ['a','b','c','d']

def test_elf():
    test_elf = Elf()
    assert test_elf.carry_cals == 0
    test_elf.count_calories(1)
    assert test_elf.carry_cals == 1