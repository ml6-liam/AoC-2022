from utils import top_three
from elf import Elf
from elf_functions import hungry_elves

print("Hungry Elves!!")

prd_path = "./data/elf_calories.txt"
dev_path = "./data/test_elf_calories.txt"
elf_cals = hungry_elves(prd_path)
top_three_elves, sum = top_three(elf_cals)

