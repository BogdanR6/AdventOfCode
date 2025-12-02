from functools import reduce

def is_invalid_2(s: str) -> bool:
    for strlen in range(1, len(s) // 2 + 1):
        if len(s) % strlen != 0:
            continue
        first = s[:strlen]
        ok = False
        for i in range(strlen, len(s) - strlen + 1, strlen):
            if s[i:i+strlen] == first:
                ok = True
                continue
            ok = False
            break
        if ok:
            return True
    return False

def is_invalid_1(s: str) -> bool:
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:]

def find_invalid_ids(start: int, end: int) -> tuple[list[int], list[int]]:
    inv_ids_1 = []
    inv_ids_2 = []
    for id in range(start, end + 1):
        if (is_invalid_1(str(id))):
            inv_ids_1.append(id)
        if (is_invalid_2(str(id))):
            inv_ids_2.append(id)
    return inv_ids_1, inv_ids_2


def solve(input_file: str) -> tuple[int, int]:
    sum1: int = 0 # for first half
    sum2: int = 0 # for second half
    with open(input_file, 'r') as f:
        line = f.readline()
        ranges: list[str] = line.split(',')
        for range in ranges:
            range = range.split('-')
            res1, res2 = find_invalid_ids(int(range[0]), int(range[1]))
            sum1 += reduce(lambda x, y: x+y, res1, 0)
            sum2 += reduce(lambda x, y: x+y, res2, 0)
    return (sum1, sum2)


ex_input_file = '../ex_input.in'
input_file = '../input.in'
print(f"Input: '{ex_input_file}'; Output: {solve(ex_input_file)}")
print(f"Input: '{input_file}'; Output: {solve(input_file)}")
