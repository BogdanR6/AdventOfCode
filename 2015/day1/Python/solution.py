def solve(input_file: str) -> tuple[int, int]:
    ans1 = 0
    ans2 = 0
    with open(input_file, 'r') as f:
        line = list(f.readline().strip())
        current_floor = 0
        for i, ch in enumerate(line):
            if ch == "(":
                ans1 += 1
                current_floor += 1
            elif ch == ")":
                ans1 -= 1
                current_floor -= 1
                if ans2 == 0 and current_floor == -1:
                    ans2 = i + 1
    return ans1, ans2

input_file = '../input.in'
print(f"Input: '{input_file}'; Output: {solve(input_file)}")