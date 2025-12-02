from dataclasses import dataclass

UPPER_BOWND = 99
STARTING_POINT = 50

@dataclass
class Safe:
    current_position: int = STARTING_POINT
    new_security_protocol_password: int = 0 # for the first part
    newer_security_protocol_password: int = 0 # for the second part
    
    def left(self, ammount):
        times_passing_zero = (UPPER_BOWND - self.current_position + ammount) // (UPPER_BOWND + 1)
        if self.current_position == 0:
            times_passing_zero -= 1

        new_position = UPPER_BOWND - (UPPER_BOWND - self.current_position + ammount) % (UPPER_BOWND + 1)
        if new_position == 0:
            self.new_security_protocol_password += 1
            times_passing_zero += 1

        self.newer_security_protocol_password += times_passing_zero

        self.current_position = new_position

    def right(self, ammount):
        times_passing_zero = (self.current_position + ammount) // (UPPER_BOWND + 1)
        self.newer_security_protocol_password += times_passing_zero

        new_position = (self.current_position + ammount) % (UPPER_BOWND + 1)
        if new_position == 0:
            self.new_security_protocol_password += 1
        self.current_position = new_position


def solve(input_file: str) -> Safe:
    safe = Safe()

    with open(input_file, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break

            if line[0] == 'L':
                safe.left(int(line[1:]))
            else:
                safe.right(int(line[1:]))

    return safe

ex_input_file = '../ex_input.in'
input_file = '../input.in'
print(f"Input: '{ex_input_file}'; Output: {solve(ex_input_file)}")
print(f"Input: '{input_file}'; Output: {solve(input_file)}")