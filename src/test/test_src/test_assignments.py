from src.assignments import Assignment, AssignmentPair
from src.utils import parse_file_lines

def test_assignment_pairs():
    assignment_pairs = parse_file_lines('./test/test_data/test_assignments.txt')
    count_contains = 0
    overlap_count = 0
    for pair in assignment_pairs:
        apair = AssignmentPair(pair)
        print(apair)
        if apair.inclusive_pair():
            count_contains += 1
        if apair.overlap():
            overlap_count += 1
    assert count_contains == 2
    assert overlap_count == 4

def test_assignment():
    ass_range_1 = '2-6'
    ass_range_2 = '6-6'
    ass_1 = Assignment(ass_range_1)
    ass_2 = Assignment(ass_range_2)
    assert ass_1.lower_bound == 2
    assert ass_1.upper_bound == 6
    assert ass_1.contains(ass_2)