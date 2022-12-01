from elf import Elf

def test_elf():
    test_elf = Elf()
    assert test_elf.carry_cals == 0
    test_elf.count_calories(1)
    assert test_elf.carry_cals == 1