from time import time

class Elf():
    def __init__(self):
        print(f"New Elf created at {time()}")
        self.carry_cals = 0
    
    def count_calories(self, cals: int):
        self.carry_cals += cals
