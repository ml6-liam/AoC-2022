from utils import parse_file_lines
from elf import Elf

def hungry_elves(data_path: str):
    cal_vals = parse_file_lines(data_path)
    print(f"parsed {len(cal_vals)} lines from input")

    elf_cals = []
    elf = Elf()
    for cal_val in cal_vals:
        try:
            elf.count_calories(int(cal_val))
        except ValueError as e:
            elf_cals.append(elf.carry_cals)
            elf = Elf()

    elf_cals.append(elf.carry_cals)   
    print(f"{len(elf_cals)} elves found") 
    print(f"hungriest elf is carrying {max(elf_cals)}")
    return elf_cals
