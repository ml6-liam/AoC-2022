from utils import parse_file_lines

def compair(left, right, level='-'):
    if type(left) == str:
        left = eval(left)
    if type(right) == str:
        right == eval(right)
    print(f'{level} Compare {left} v {right}')
    levelup = ' '+level
    if type(left) == type(right) == list:
        while (len(left)>0 or len(right)>0):
            if len(right) == 0:
                print(f'{level} right side is shorter so they are not in the right order')
                return False
            elif len(left) == 0:
                print(f'{level} left side is shorter so they are in the right order')
                return True
            else:
                new_left = left.pop(0)
                new_right = right.pop(0) 
                comparison = compair(new_left, new_right, levelup)
                if comparison is not None:
                    #found = True
                    return comparison
    elif type(left) == type(right) == int:
        if left > right:
            print(f'{level} right side is smaller so they are not in the right order')
            return False
        if left < right:
            print(f'{level} left side is smaller so they are in the right order')
            return True
    elif type(left) != type(right):
        if type(left) == int:
            left = [left]
            print(f'{level} Mixed types; convert left to {left} and retry')
            return compair(left, right, level)
        elif type(right) == int:
            right = [right]
            print(f'{level} Mixed type; convert right to {right} and retry')
            return compair(left, right, level)

def parse_pairs(input):
    pairs = []
    current_pair = []
    for line in input:
        if len(line) == 0:
            pairs.append(current_pair)
            current_pair = []
        else:
            line_arr = eval(line)
            current_pair.append(line_arr)
    pairs.append(current_pair)
    return pairs

def parse_packets(input):
    packets = []
    for line in input:
        if len(line) != 0:
            packets.append(line)
    return packets

def part_1(input):
    pairs = parse_pairs(input)
    correct_pairs = []
    pair_id_sum = 0
    divider_key = 1
    for pair_id, pair in enumerate(pairs):
        print(f'===== Pair {pair_id} =====')
        if compair(pair[0], pair[1]):
            correct_pairs.append(pair_id)
            pair_id_sum += pair_id+1
        print('           ----')
    print(correct_pairs)
    print(pair_id_sum)
    print(divider_key)

def part_2(input):
    packets = parse_packets(input)
    packets.append('[[2]]')
    packets.append('[[6]]')
    swapping = True
    while swapping:
        swapping = False
        for i in range(len(packets)):
            a = i
            while (a < len(packets)-1) and not (compair(eval(packets[a]), eval(packets[a+1]))):
                print(f'Swap Packets {packets[a]} & {packets[a+1]}')
                swapping = True
                p_a = packets[a]
                    #print(p_a)
                p_b =  packets[a+1]
                    #print(p_b)
                packets[a] = p_b
                packets[a+1] = p_a
                a += 1
    print(f'Sorted {len(packets)} packets:')
    for packet in packets:
        print(packet)
    divider_key = 1
    for packet_idx, packet in enumerate(packets):
        if packet in ['[[6]]','[[2]]']:
            divider_key = divider_key * (packet_idx+1)
    print(divider_key)

    

if __name__=='__main__':
    input = parse_file_lines('./data/pairs.txt')
    print(f'####### Part 1 #######')
    part_1(input)
    print('####### Part 2 #######')
    part_2(input)