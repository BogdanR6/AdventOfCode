def solve(input_file: str):
    wrapping_paper = 0
    ribbon = 0
    with open(input_file, 'r') as f:
        dimensions = list(map(lambda s: tuple(map(int, s.split('x'))), [s.strip() for s in f.readlines()]))
        for l, w, h in dimensions:
            present_surface_aread = 2*l*w + 2*w*h + 2*h*l
            area_of_smallest_size = min(l*w, w*h, h*l)
            wrapping_paper += present_surface_aread + area_of_smallest_size

            present_volume = l*w*h
            perimeter_of_smallest_size = min(2*(l + w), 2*(w+h), 2*(h*l))
            ribbon += perimeter_of_smallest_size + present_volume
        return wrapping_paper, ribbon



ex_input_file = "../ex_input.in"
input_file = '../input.in'
print(f"Input: '{ex_input_file}'; Output: {solve(ex_input_file)}")
print(f"Input: '{input_file}'; Output: {solve(input_file)}")