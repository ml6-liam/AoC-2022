from src.stacks import Stack, CrateStacks
from src.utils import parse_file_lines

def test_cratestacks():
    test_lines = parse_file_lines('./test/test_data/test_instructions.txt')
    crate_stacks = CrateStacks(test_lines)
    assert len(crate_stacks.stacks) == 3
    assert crate_stacks.crate_message == "MCD"