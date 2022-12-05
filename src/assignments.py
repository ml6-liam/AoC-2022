import re

class Assignment():
    def __init__(self, r):
        bounds = re.split('-', r)
        self.lower_bound = int(bounds[0])
        self.upper_bound = int(bounds[1])
        self.tasks = list(range(self.lower_bound, self.upper_bound+1))
    
    def contains(self, input):
        if (input.lower_bound >= self.lower_bound) and (input.upper_bound <= self.upper_bound):
            return True
        else:
            return False

    def between_bounds(self, target):
        return self.lower_bound <= target <= self.upper_bound


class AssignmentPair():
    def __init__(self, pair):
        self.assignments = re.split(',', pair)
        self.a1 = Assignment(self.assignments[0])
        self.a2 = Assignment(self.assignments[1])
        

    def inclusive_pair(self):
        return (self.a1.contains(self.a2) or self.a2.contains(self.a1))

    
    def overlap(self):
        return (self.a1.between_bounds(self.a2.lower_bound) or self.a1.between_bounds(self.a2.upper_bound))