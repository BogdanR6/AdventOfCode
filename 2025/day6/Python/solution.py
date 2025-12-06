def solve(input_file: str) -> tuple[int, int]:
    def transpose(matrix: list[list]) -> list[list]:
        return list(map(list, zip(*matrix)))

    def col_to_int(col: list[str]) -> int:
        return int(''.join(digit for digit in col if digit.strip()))

    def col_has_digit(col: list[str]) -> bool:
        return any(ch.isdigit() for ch in col)

    lines = [line.rstrip('\n') for line in open(input_file)]
    rows = lines[:-1]
    signs = lines[-1].strip().split()

    horizontal_rows = [list(map(int, row.split())) for row in rows]
    horizontal_numbers_list = list(map(tuple, zip(*horizontal_rows)))

    digit_rows = list(map(list, rows))
    digit_cols = [col for col in transpose(digit_rows) if col_has_digit(col)]

    vertical_numbers = list(map(col_to_int, digit_cols))
    group_size = len(rows)
    it = iter(vertical_numbers)
    vertical_numbers_list = list(zip(*[it] * group_size))

    grand_total_1 = grand_total_2 = 0

    opr = {'+': lambda a, b: a + b, '*': lambda a, b: a * b}
    id = {'+': 0, '*': 1}
    for sign, v_numbers, h_numbers in zip(signs, vertical_numbers_list, horizontal_numbers_list):
        sum1 = sum2 = id[sign]
        for number in h_numbers: sum1 = opr[sign](sum1, number)
        for number in v_numbers: sum2 = opr[sign](sum2, number)
        grand_total_1 += sum1
        grand_total_2 += sum2

    return grand_total_1, grand_total_2

ex_input_file = '../ex_input.in'
input_file = '../input.in'
print(f"Input: '{ex_input_file}'; Output: {solve(ex_input_file)}")
print(f"Input: '{input_file}'; Output: {solve(input_file)}")