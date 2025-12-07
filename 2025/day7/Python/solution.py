from collections import defaultdict

def fall(diagram: list[list[str]], starting_point: int) -> tuple[int, int]:
    splits_count = 0
    tachyon_positions: set[int] = {starting_point}
    timelines: dict[int, int] = {starting_point: 1}
    for level in diagram:
        # calculate the number of splits
        new_tachyon_positions = set()
        for tachyon_pos in tachyon_positions:
            if level[tachyon_pos] == '^':
                splits_count += 1
                split_left = tachyon_pos - 1
                split_right = tachyon_pos + 1
                new_tachyon_positions.union({split_left, split_right})
            else:
                new_tachyon_positions.add(tachyon_pos)
        tachyon_positions = new_tachyon_positions

        # calculate the nuber of timelines
        new_timelines = defaultdict(int)
        for tachyon_pos, timelines_on_pos in timelines.items():
            if level[tachyon_pos] == '^':
                left = tachyon_pos - 1
                right = tachyon_pos + 1
                new_timelines[left] += timelines_on_pos
                new_timelines[right] += timelines_on_pos
            else:
                new_timelines[tachyon_pos] += timelines_on_pos
        timelines = dict(new_timelines)

    timelines_count = sum(timelines.values())

    return splits_count, timelines_count

def solve(input_file: str) -> tuple[int, int]:
    lines = [line.strip() for line in open(input_file)]
    diagram = list(map(list, lines))
    return fall(diagram, diagram[0].index('S'))


ex_input_file = '../ex_input.in'
input_file = '../input.in'
print(f"Input: '{ex_input_file}'; Output: {solve(ex_input_file)}")
print(f"Input: '{input_file}'; Output: {solve(input_file)}")