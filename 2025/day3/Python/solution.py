def solve(file_path: str) -> tuple[int, int]:
    sum1 = 0
    sum2 = 0
    with open(file_path, 'r') as f:
        line = f.readline().strip()
        while line:
            line_list = list(line)
            mx = ""
            for i in range(1, -1, -1):
                cmx = max(line_list[:len(line_list) - i])
                mx += cmx
                line_list = line_list[line_list.index(cmx) + 1:]
            sum1 += int(mx)

            line_list = list(line)
            mx = ""
            for i in range(11, -1, -1):
                cmx = max(line_list[:len(line_list) - i])
                mx += cmx
                line_list = line_list[line_list.index(cmx) + 1:]
            sum2 += int(mx)

            line = f.readline().strip()
    return sum1, sum2

ex_input_file = '../ex_input.in'
input_file = '../input.in'
print(f"Input: '{ex_input_file}'; Output: {solve(ex_input_file)}")
print(f"Input: '{input_file}'; Output: {solve(input_file)}")