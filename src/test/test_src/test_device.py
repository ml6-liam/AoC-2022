from src.device import Device
from src.utils import parse_file_lines

test_device = Device()

test_messages = [('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19),
                 ('bvwbjplbgvbhsrlpgdmjqwftvncz',23),
                 ('nppdvjthqldpwncqszvftbrmjlhg', 23),
                 ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29),
                 ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26)]

test_packets = [('bvwbjplbgvbhsrlpgdmjqwftvncz', 5),
                ('nppdvjthqldpwncqszvftbrmjlhg', 6),
                ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10),
                ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11)]

def test_message_marker():
    for test_case in test_messages:
        assert test_device.find_start_marker(test_case[0], "message") == test_case[1]

def test_packet_marker():
    for test_case in test_packets:
        assert test_device.find_start_marker(test_case[0], "packet") == test_case[1]