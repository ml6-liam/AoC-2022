import re


class Strategy:
    score = 0
    v2_score = 0
    strategy_guide = []
    def __init__(self, sguide: list):
        self.score = 0
        self.v2_score = 0
        self.strategy_guide = self.parse_hands(sguide)
    
    def str_to_tuple(self, s: str):
        splits = re.split(' ', s)
        return (splits[0], splits[1])
    
    def parse_hands(self, hands: list):
        result = []
        for h in hands:
            result.append(self.str_to_tuple(h))
        return result
    
    def score_strategy(self):
        for hand in self.strategy_guide:
            hand_sc = self.asess_hand(hand)
            shape_sc = self.score_shape(hand[1])
            self.score += hand_sc+shape_sc
        return self.score
    
    def score_strat_2(self):
        scores = {'A':{'X':3,'Y':1,'Z':2}, 
                  'B':{'X':1,'Y':2,'Z':3},
                  'C':{'X':2,'Y':3,'Z':1}}
        score = 0
        for hand in self.strategy_guide:
            shape_sc = scores[hand[0]][hand[1]]
            out_sc = self.score_outcome(hand[1])
            score += shape_sc+out_sc
        self.v2_score = score
        return self.v2_score

    def asess_hand(self, hand: tuple):
        losses = [("A", "Z"), ("B", "X"), ("C", "Y")]
        wins = [("A", "Y"), ("B", "Z"), ("C", "X")]
        if hand in losses:
            return 0
        elif hand in wins:
            return 6
        else:
            return 3

    def score_shape(self, shape):
        if shape in ['X', "A"]:
            return 1
        elif shape in ["Y", 'B']:
            return 2
        elif shape in ["Z", 'C']:
            return 3

    def score_outcome(self, outcome: str):
        if outcome == 'X':
            return 0
        elif outcome == "Y":
            return 3
        elif outcome == "Z":
            return 6

    def reset_score(self):
        self.score=0
        return self.score
