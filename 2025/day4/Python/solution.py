def is_valid(d: list[list[str]], x: int, y: int) -> bool:
    if x >= len(d) or x < 0 or y >= len(d[0]) or y < 0:
        return False
    return True

def can_be_lifted(d: list[list[str]], x: int, y: int) -> bool:
    cnt = 0
    dx = [1, 1, 0, -1, -1, -1, 0,   1] 
    dy = [0, 1, 1,  1,  0, -1, -1, -1]
    for ax, ay in zip(dx, dy):
        if is_valid(d, x + ax, y + ay) and (d[x + ax][y + ay] == "@" or d[x + ax][y + ay] == "x"):
            cnt += 1
            if cnt >= 4:
                return False
    return True
    

def solve(input_file: str) -> tuple[int, int]:
    count1 = 0
    with open(input_file, 'r') as f:
        diagram = [list(s.strip()) for s in f.readlines()]
        for i, row in enumerate(diagram):
            for j, col in enumerate(row):
                if col == '@':
                    count1 += 1 if can_be_lifted(diagram, i, j) else 0
        count2 = 0
        change = True
        while change:
            change = False
            for i, row in enumerate(diagram):
                for j, col in enumerate(row):
                    if col == '@':
                        if can_be_lifted(diagram, i, j):
                            diagram[i][j] = 'x'
                            count2 += 1
                            change = True
            for i, row in enumerate(diagram):
                for j, col in enumerate(row):
                    if col == 'x':
                       diagram[i][j] = '.' 
    return count1, count2

ex_input_file = '../ex_input.in'
input_file = '../input.in'
print(f"Input: '{ex_input_file}'; Output: {solve(ex_input_file)}")
print(f"Input: '{input_file}'; Output: {solve(input_file)}")