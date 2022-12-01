from typing import List

def parse_file_lines(path: str) -> List:
    with open(path) as f:
        lines = [line for line in f]
    return lines

def top_three(input_list: list):
    input_list.sort(reverse=True)
    top_three = input_list[:3]
    sum = 0
    for val in top_three:
        sum+=val
    print(f"""top three values found: {top_three} \n
              Total of Top 3: {sum}""")
    return top_three, sum