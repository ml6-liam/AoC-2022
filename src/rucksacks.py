
class Rucksack:
    def __init__(self, content_string):
        total_contents = len(content_string)
        self.f_comp = content_string[:total_contents//2]
        self.s_comp = content_string[total_contents//2:]
        self.common_items = self.common_chars()
        self.prio_score = 0
        for item in self.common_items:
            self.prio_score += self.score_char(item)
    
    def score_char(self, char: str):
        score = ord(char.lower())-96
        if char.isupper():
            score = score+26
        return score
    
    def common_chars(self):
        cchars = list(set(self.f_comp)&set(self.s_comp))
        return cchars

class RucksackGroup(Rucksack):
    def __init__(self, group: list):
        self.r1=group[0]
        self.r2=group[1]
        self.r3=group[2]
        self.badge = self.find_badge()
        self.badge_prio = self.score_char(self.badge)
    
    def find_badge(self):
        badge_list = list(set(self.r1)&set(self.r2)&set(self.r3))
        return badge_list[0]
    
def make_groups(input: list, N: int):
    return [input[n:n+N] for n in range(0, len(input), N)]