from z3 import *
import re
from collections import deque


def solve_min_xor_steps(initial_bitmap, button_masks):
    """
    Find minimum XOR operations to transform initial bitmap to target.
    
    Uses BFS to explore all possible states reachable by applying
    button XOR masks, tracking the shortest path to the target.
    
    Args:
        initial_bitmap: Starting 16-bit state (integer)
        button_masks: List of XOR masks that can be applied
    
    Returns:
        Minimum number of button presses, or -1 if unreachable
    """
    TARGET = 0  # We want to reach all bits off
    
    # BFS setup
    queue = deque([(initial_bitmap, 0)])  # (current_state, steps)
    visited = {initial_bitmap}
    
    while queue:
        current_state, steps = queue.popleft()
        
        # Check if we've reached the target
        if current_state == TARGET:
            return steps
        
        # Try applying each button mask
        for mask in button_masks:
            next_state = current_state ^ mask  # XOR operation
            
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps + 1))
    
    return -1  # Target unreachable


def solve_min_button_presses(target_values, buttons):
    """
    Find minimum button presses to achieve target values.
    
    Uses Z3 constraint solver to find the optimal integer solution
    for a system of linear equations where each button increments
    specific positions by 1.
    
    Args:
        target_values: List of desired values for each position
        buttons: List of button definitions, where each button is
                 a list of position indices it increments
    
    Returns:
        Tuple of (solution vector, total presses), or None if no solution
    """
    num_positions = len(target_values)
    num_buttons = len(buttons)
    
    # Create Z3 variables for button press counts
    button_presses = [Int(f"button_{j}") for j in range(num_buttons)]
    
    # Setup optimizer
    optimizer = Optimize()
    
    # Constraint: All button presses must be non-negative integers
    for press_count in button_presses:
        optimizer.add(press_count >= 0)
    
    # Constraint: For each position, sum of button effects must equal target
    for position in range(num_positions):
        # Find all buttons that affect this position
        effect_sum = sum(
            button_presses[j] 
            for j in range(num_buttons) 
            if position in buttons[j]
        )
        optimizer.add(effect_sum == target_values[position])
    
    # Objective: Minimize total button presses
    total_presses = sum(button_presses)
    optimizer.minimize(total_presses)
    
    # Solve the optimization problem
    if optimizer.check() != sat:
        return None
    
    # Extract solution
    model = optimizer.model()
    solution = [model[var].as_long() for var in button_presses]
    
    return solution, sum(solution)


def parse_bitmap_string(bitmap_str):
    """
    Convert bitmap string like '.#.#' to integer.
    '.' = 0, '#' = 1, rightmost char is LSB.
    """
    value = 0
    for char in reversed(bitmap_str):
        value <<= 1
        if char == '#':
            value |= 1
    return value


def create_mask_from_positions(positions):
    """Create a bitmask with specified positions set to 1."""
    mask = 0
    for pos in positions:
        if 0 <= pos < 16:
            mask |= (1 << pos)
    return mask


def parse_input_line(line):
    """
    Parse a line of input into components.
    
    Format: [bitmap] (pos,pos,...) (pos,pos,...) {val,val,...}
    
    Returns:
        (initial_bitmap, button_masks, button_positions, target_values)
    """
    # Extract bitmap [...]
    bitmap_match = re.search(r'\[(.*?)\]', line)
    initial_bitmap = parse_bitmap_string(bitmap_match.group(1))
    
    # Extract button position lists (...)
    button_positions = []
    for match in re.findall(r'\(([\d,]+)\)', line):
        positions = [int(x) for x in match.split(',')]
        button_positions.append(positions)
    
    # Create XOR masks from positions
    button_masks = [create_mask_from_positions(pos) for pos in button_positions]
    
    # Extract target values {...}
    values_match = re.search(r'\{([\d,]+)\}', line)
    target_values = [int(x) for x in values_match.group(1).split(',')]
    
    return initial_bitmap, button_masks, button_positions, target_values


def main():
    """Process input file and solve both parts."""
    with open("../input.in", 'r') as f:
        lines = [line.strip() for line in f]
    
    part1_total = 0
    part2_total = 0
    
    for line in lines:
        initial_bitmap, button_masks, button_positions, target_values = parse_input_line(line)
        
        part1_result = solve_min_xor_steps(initial_bitmap, button_masks)
        if part1_result == -1:
            print(f"Part 1 - No solution for line: {line[:50]}...")
            continue
        part1_total += part1_result
        
        part2_result = solve_min_button_presses(target_values, button_positions)
        if part2_result is None:
            print(f"Part 2 - No solution for line: {line[:50]}...")
            continue
        
        _, presses = part2_result
        part2_total += presses
    
    print(f"Part 1 - Total minimum XOR operations: {part1_total}")
    print(f"Part 2 - Total minimum button presses: {part2_total}")


if __name__ == "__main__":
    main()