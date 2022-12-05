from src.rock_paper_scissors import Strategy
from src.utils import parse_file_lines

def test_strategy():
    strat_guide = parse_file_lines("./test/test_data/test_strategy.txt")
    print(strat_guide)
    test_strat = Strategy(strat_guide)
    assert test_strat.score == 0
    assert test_strat.score_strategy() == 15
    assert test_strat.score_strat_2() == 12
