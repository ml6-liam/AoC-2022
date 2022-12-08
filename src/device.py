from utils import parse_file_lines
class Device:
    def __init__(self):
        self.id = 0

    def find_start_marker(self, input: str, mode: str):
        window_modes = {'message': 14, 'packet':4}
        marker_len = window_modes[mode]
        for i in range(marker_len, len(input)):
            if len(set(input[i-marker_len:i])) == marker_len:
                return i


if __name__=='__main__':
    device = Device()
    inputs = parse_file_lines('./data/input_messages.txt')
    for input in inputs:
        print('part 1')
        print(f'String with start marker at pos {device.find_start_marker(input, mode="packet")}')
        print('part 2')
        print(f'String with start marker at pos {device.find_start_marker(input, mode="message")}')