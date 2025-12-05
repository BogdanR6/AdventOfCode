def solve(input_file: str) -> tuple[int, int]:
    fresh_ing_count = 0 # for the first part
    all_fresh_ing_count = 0 # for the second part
    with open(input_file, 'r') as f:
        lines = [s.strip() for s in f.readlines()]
        ranges = lines[:lines.index('')]
        products: list[int] = list(map(int, lines[lines.index('') + 1:]))

        ranges = sorted(list(map(lambda s: tuple(map(int, s.split('-'))), ranges)))

        # merge the overlapping ranges
        simple_ranges = []
        n = len(ranges)
        for i in range(n):
            lower, upper = ranges[i][0], ranges[i][1]

            if simple_ranges and simple_ranges[-1][1] >= upper:
                continue

            for j in range(i + 1, n):
                if ranges[j][0] <= upper:
                    upper = max(upper, ranges[j][1])
            simple_ranges.append([lower, upper])

        ranges = simple_ranges

        for product in products:
            for r in ranges:
                lower, upper = r
                if lower <= product <= upper:
                    fresh_ing_count += 1
                    break


        for r in simple_ranges:
            all_fresh_ing_count += r[1] - r[0] + 1

    return fresh_ing_count, all_fresh_ing_count


ex_input_file = '../ex_input.in'
input_file = '../input.in'
print(f"Input: '{ex_input_file}'; Output: {solve(ex_input_file)}")
print(f"Input: '{input_file}'; Output: {solve(input_file)}")