from src.elf_functions import hungry_elves

def test_hungry_elves():
    assert hungry_elves("./test/test_data/test_elf_calories.txt") == [6000, 4000, 11000, 24000, 10000]