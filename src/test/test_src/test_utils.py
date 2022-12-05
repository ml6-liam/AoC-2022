from src.utils import (top_three,
                       parse_file_lines)

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