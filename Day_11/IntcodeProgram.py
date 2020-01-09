from enum import Enum
import math

class IntcodeProgram:

    EXTRA_MEMORY = 5000000

    class Opcodes(Enum):
        HALT = 99
        ADD = 1
        MUL = 2
        SAVE = 3
        READ = 4
        JUMP_T = 5
        JUMP_F = 6
        LESS_THAN = 7
        EQUAL = 8
        RELATIVE = 9

    class Modes(Enum):
        POSITION = 0
        IMMEDIATE = 1
        RELATIVE = 2

    def __init__(self, program):
        self.instruction_pointer = 0
        self.program = program.copy() + [0] * self.EXTRA_MEMORY
        self.relative_base = 0
        self.output_buffer = []

    def get_instruction_set(self, instruction):
        # depending on the instruction we will parse the digits in some fashion
        instruction_set = []
        opcode = instruction % 100
        instruction_set.append(opcode)
        instruction = int(instruction / 100)

        if opcode == self.Opcodes.ADD.value or opcode == self.Opcodes.MUL.value:
            # look for three params
            for i in range(3):
                mode = instruction % 10
                instruction = int(instruction / 10)
                instruction_set.append(mode)
        elif opcode == self.Opcodes.SAVE.value\
                or opcode == self.Opcodes.READ.value\
                or opcode == self.Opcodes.RELATIVE.value:
            # look for 2 params
            for i in range(1):
                mode = instruction % 10
                instruction = int(instruction / 10)
                instruction_set.append(mode)
        elif opcode == self.Opcodes.JUMP_T.value or opcode == self.Opcodes.JUMP_F.value:
            # look for 2 params
            for i in range(2):
                mode = instruction % 10
                instruction = int(instruction / 10)
                instruction_set.append(mode)
        elif opcode == self.Opcodes.EQUAL.value or opcode == self.Opcodes.LESS_THAN.value:
            # look for 3 params
            for i in range(3):
                mode = instruction % 10
                instruction = int(instruction / 10)
                instruction_set.append(mode)
        return instruction_set

    def add(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2, mode_3] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]
        param_3 = input_codes[instruction_pointer + 3]

        value_1 = self.read(param_1, mode_1, input_codes)
        value_2 = self.read(param_2, mode_2, input_codes)
        summed_val = value_1 + value_2
        self.write(param_3, mode_3, input_codes, summed_val)

    def mul(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2, mode_3] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]
        param_3 = input_codes[instruction_pointer + 3]

        value_1 = self.read(param_1, mode_1, input_codes)
        value_2 = self.read(param_2, mode_2, input_codes)
        product_val = value_1 * value_2
        self.write(param_3, mode_3, input_codes, product_val)

    def save(self, input_codes, input_signal, instruction_set, instruction_pointer):
        [mode_1] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        self.write(param_1, mode_1, input_codes, int(input_signal))

    def output(self, input_codes, instruction_set, instruction_pointer):
        [mode_1] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        return self.read(param_1, mode_1, input_codes)

    def jump_t(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]

        value_1 = self.read(param_1, mode_1, input_codes)
        value_2 = self.read(param_2, mode_2, input_codes)

        # set the instruction pointer to the value from the second param
        if value_1 != 0:
            return value_2
        return None

    def jump_f(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]

        value_1 = self.read(param_1, mode_1, input_codes)
        value_2 = self.read(param_2, mode_2, input_codes)

        # set the instruction pointer to the value from the second param
        if value_1 == 0:
            return value_2
        return None

    def less_than(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2, mode_3] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]
        param_3 = input_codes[instruction_pointer + 3]

        value_1 = self.read(param_1, mode_1, input_codes)
        value_2 = self.read(param_2, mode_2, input_codes)

        if value_1 < value_2:
            self.write(param_3, mode_3, input_codes, 1)
        else:
            self.write(param_3, mode_3, input_codes, 0)

    def equal(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2, mode_3] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]
        param_3 = input_codes[instruction_pointer + 3]

        value_1 = self.read(param_1, mode_1, input_codes)
        value_2 = self.read(param_2, mode_2, input_codes)

        if value_1 == value_2:
            self.write(param_3, mode_3, input_codes, 1)
        else:
            self.write(param_3, mode_3, input_codes, 0)

    def relative(self, input_codes, instruction_set, instruction_pointer):
        [mode_1] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        self.relative_base += self.read(param_1, mode_1, input_codes)

    def run(self, input_signal):
        while True:
            instruction = self.program[self.instruction_pointer]
            instruction_set = self.get_instruction_set(instruction)
            opcode = instruction_set[0]

            if opcode == self.Opcodes.HALT.value:
                return self.output_buffer
            elif opcode == self.Opcodes.ADD.value:
                self.add(self.program, instruction_set, self.instruction_pointer)
                self.instruction_pointer += 4
            elif opcode == self.Opcodes.MUL.value:
                self.mul(self.program, instruction_set, self.instruction_pointer)
                self.instruction_pointer += 4
            elif opcode == self.Opcodes.SAVE.value:
                if len(input_signal) == 0:
                    return "waiting"
                self.save(self.program, input_signal[0], instruction_set, self.instruction_pointer)
                self.instruction_pointer += 2
                input_signal = input_signal[1:]
            elif opcode == self.Opcodes.READ.value:
                result = self.output(self.program, instruction_set, self.instruction_pointer)
                self.output_buffer.append(result)
                self.instruction_pointer += 2
            elif opcode == self.Opcodes.JUMP_T.value:
                new_pointer = self.jump_t(self.program, instruction_set, self.instruction_pointer)
                self.instruction_pointer = new_pointer if new_pointer is not None else self.instruction_pointer + 3
            elif opcode == self.Opcodes.JUMP_F.value:
                new_pointer = self.jump_f(self.program, instruction_set, self.instruction_pointer)
                self.instruction_pointer = new_pointer if new_pointer is not None else self.instruction_pointer + 3
            elif opcode == self.Opcodes.LESS_THAN.value:
                self.less_than(self.program, instruction_set, self.instruction_pointer)
                self.instruction_pointer += 4
            elif opcode == self.Opcodes.EQUAL.value:
                self.equal(self.program, instruction_set, self.instruction_pointer)
                self.instruction_pointer += 4
            elif opcode == self.Opcodes.RELATIVE.value:
                self.relative(self.program, instruction_set, self.instruction_pointer)
                self.instruction_pointer += 2
            else:
                return "error"

    def read(self, param, mode, input_codes):
        if mode == self.Modes.IMMEDIATE.value:
            return param
        elif mode == self.Modes.POSITION.value:
            return input_codes[param]
        elif mode == self.Modes.RELATIVE.value:
            return input_codes[self.relative_base + param]

    def write(self, param, mode, input_codes, value):
        if mode == self.Modes.IMMEDIATE.value:
            input_codes[input_codes[param]] = value
        elif mode == self.Modes.POSITION.value:
            input_codes[param] = value
        elif mode == self.Modes.RELATIVE.value:
            input_codes[self.relative_base + param] = value


class RobotCamera:

    def __init__(self, program_input, starting_color):
        self.camera = IntcodeProgram(program_input)
        self.current_coordinate = (0, 0)
        self.direction = (math.pi / 2)  # always start facing up
        self.coordinates_seen = {}
        self.starting_color = starting_color

    def update_direction(self, direction):
        # go left
        if direction == 0:
            self.direction = self.direction + (math.pi / 2)
            if self.direction >= (2 * math.pi):
                self.direction %= (2 * math.pi)

        # go right
        elif direction == 1:
            self.direction = self.direction - (math.pi / 2)
            while self.direction < 0.0:
                self.direction += (2 * math.pi)
        else:
            print("direction error")

    def move_to_cell(self):
        # facing right
        if self.direction == 0:
            self.current_coordinate = (self.current_coordinate[0] + 1, self.current_coordinate[1])
        # facing up
        elif self.direction == (math.pi / 2):
            self.current_coordinate = (self.current_coordinate[0], self.current_coordinate[1] + 1)
        # facing left
        elif self.direction == math.pi:
            self.current_coordinate = (self.current_coordinate[0] - 1, self.current_coordinate[1])
        # facing down
        elif self.direction == 3 * (math.pi / 2):
            self.current_coordinate = (self.current_coordinate[0], self.current_coordinate[1] - 1)

    def paint(self):
        # program runs until termination on an internal condition
        while True:
            # if not the first time at this cell then retrieve the last color it was painted
            if len(self.coordinates_seen) == 0:
                current_color = self.starting_color
            elif self.current_coordinate in self.coordinates_seen:
                current_color = self.coordinates_seen[self.current_coordinate]
            else:
                # all colors start black
                current_color = 0

            # retrieve output data
            self.camera.run([current_color])
            if len(self.camera.output_buffer) == 0:
                break

            new_color = self.camera.output_buffer[0]
            new_direction = self.camera.output_buffer[1]

            # clear output buffer
            self.camera.output_buffer = []

            # mark the color for a cell
            self.coordinates_seen[self.current_coordinate] = new_color
            self.update_direction(new_direction)
            self.move_to_cell()


def normalize_coordinate_colorings(coordinates):
    min_x = None
    min_y = None
    for coordinate in coordinates.keys():
        if min_x is None and min_y is None:
            min_x = coordinate[0]
            min_y = coordinate[1]
        else:
            min_x = min(min_x, coordinate[0])
            min_y = min(min_y, coordinate[1])

    delta_x = abs(min_x)
    delta_y = abs(min_y)
    normalized = {}
    for coord, color in coordinates.items():
        new_coord = (coord[0] + delta_x, coord[1] + delta_y)
        normalized[new_coord] = color

    return normalized


def get_max_region(coordinates):
    max_x = None
    max_y = None
    for coord in coordinates.keys():
        if max_x is None and max_y is None:
            max_x = coord[0]
            max_y = coord[1]
        else:
            max_x = max(max_x, coord[0])
            max_y = max(max_y, coord[1])

    return (max_x, max_y)


def print_area(area):
    for row in area:
        print(' '.join(row))


def generate_painted_output(coordinate_colorings):
    (max_x, max_y) = get_max_region(coordinate_colorings)
    area = [[' ' for i in range(max_x + 1)] for j in range(max_y + 1)]

    for coord, color in coordinate_colorings.items():
        y = coord[1]
        x = coord[0]
        if color == 0:
            continue
        area[y][x] = "#"

    return area


if __name__ == "__main__":
    with open("input.txt") as data:
        for line in data:
            # list comprehension to turn all strings in list to ints
            input_values = [int(str_num) for str_num in line.split(',')]

            robot = RobotCamera(input_values, 0)
            robot.paint()
            assert len(robot.coordinates_seen) == 1934

            robot = RobotCamera(input_values, 1)
            robot.paint()
            normalized_colorings = normalize_coordinate_colorings(robot.coordinates_seen)
            area = generate_painted_output(normalized_colorings)
            print_area(area)







