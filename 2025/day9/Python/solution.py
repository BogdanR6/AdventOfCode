from typing import Annotated
from itertools import combinations

Point = Annotated[tuple[int, int], "Tuple of point's coordinates"]

def dist(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + 1

def area(p1: Point, p2: Point) -> int:
    l = dist(p1, (p2[0], p1[1]))
    L = dist(p2, (p2[0], p1[1]))
    return l * L

def solve1(input_file: str):
    points: list[Point] = list(map(lambda line: (int(line.split(',')[0]), int(line.split(',')[1])), open(input_file, 'r')))
    mx = 0
    for i, p1 in enumerate(points[:-1]):
        for p2 in points[i + 1:]:
            a = area(p1, p2)
            if a > mx:
                mx = a
    return mx

def Compress(l: list[Point]) -> tuple[list[Point], dict[int, int], dict[int, int], dict[int, int], dict[int, int]]:
    x = [p[0] for p in l] 
    y = [p[1] for p in l]

    # Create sorted list of unique values
    x_su = sorted(set(x))
    y_su = sorted(set(y))
    
    # Map each value to its index in x_su and y_su
    x_encoding = {v: i for i, v in enumerate(x_su)}
    x_decoding = {i: v for i, v in enumerate(x_su)}
    y_encoding = {v: i for i, v in enumerate(y_su)}
    y_decoding = {i: v for i, v in enumerate(y_su)}
    
    
    # Return the compressed version
    return [(x_encoding[x], y_encoding[y]) for x, y in l], x_encoding, x_decoding, y_encoding, y_decoding

def connect(mat, p1: Point, p2: Point):
    vertical = False
    start, end = p1[1], p2[1]
    if start == end:
        vertical = True
        start, end = p1[0], p2[0]
    step = 1 if start < end else -1

    for i in range(start + step, end, step):
        if vertical:
            mat[i][p1[1]] = 'X'
        else:
            mat[p1[0]][i] = 'X'

def solve2(input_file: str) -> int:
    points: list[Point] = list(map(lambda line: ((int(line.split(',')[1]), int(line.split(',')[0]))), open(input_file, 'r')))

    compressed, x_encoding, x_decoding, y_encoding, y_decoding = Compress(points)

    matrix = [['.'] * (max(y_decoding) + 1) for _ in range(max(x_decoding) + 1)]
    for x, y in compressed:
        matrix[x][y] = "#"

    connect(matrix, compressed[0], compressed[-1])
    for i, p1 in enumerate(compressed[:-1]):
        p2 = compressed[i + 1]
        connect(matrix, p1, p2)

    interior_point = (1, 117) # put by hand for the exemple
    # fill
    fill(matrix, interior_point)
    for line in matrix:
        print(line)

    # thry all pairs and see witch denotes a rectangle filled with green (and gratest size)
    mxa = 0
    for p1, p2 in combinations(points, 2):
        a = area(p1, p2)
        ep1 = (x_encoding[p1[0]], y_encoding[p1[1]])
        ep2 = (x_encoding[p2[0]], y_encoding[p2[1]])
        if a > mxa and is_filled(matrix, ep1, ep2):
            mxa = a
    return mxa

def fill(matrix, start):
    stack = [start]

    while stack:
        i, j = stack.pop()

        if matrix[i][j] != '.':
            continue

        matrix[i][j] = 'X'

        # Push neighbors (same order as recursive)
        stack.append((i, j + 1))
        stack.append((i, j - 1))
        stack.append((i + 1, j))
        stack.append((i - 1, j))

def is_filled(mat, p1: Point, p2: Point) -> bool:
    for i in range(min(p2[0], p1[0]), max(p1[0], p2[0]) + 1):
        for j in range(min(p1[1], p2[1]), max(p2[1], p1[1]) + 1):
            if mat[i][j] == '.':
                return False
    return True

ex_input_file = '../ex_input.in'
input_file = '../input.in'
print(f"Input: '{input_file}'; Output: {solve1(input_file)} {solve2(input_file)}")