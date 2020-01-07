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

    def __init__(self, program_input):
        self.camera = IntcodeProgram(program_input)
        self.current_coordinate = (0, 0)
        # TODO: determine how to represent direction
        self.direction = (math.pi / 2)
        self.coordinates_seen = {}

    def get_latest_output(self):
        return self.camera.output_buffer

    def update_direction(self, direction):
        if direction == 0:
            # go left
            self.direction = self.direction + (math.pi / 2)
            if self.direction >= (2 * math.pi):
                self.direction %= (2 * math.pi)

        elif direction == 1:
            # go right
            self.direction = self.direction - (math.pi / 2)
            if direction < 0:
                self.direction += (2 * math.pi)
        else:
            print("direction error")

        return 0

    def capture_photo(self, color):
        # TODO: determine what to do if this is not the first time visiting this cell

        self.camera.run(color)
        color = self.camera.output_buffer[0]
        direction = self.camera.output_buffer[1]

        # mark the color for a cell
        self.coordinates_seen[self.current_coordinate] = color

        self.update_direction(direction)



if __name__ == "__main__":
    with open("input.txt") as data:
        for line in data:
            # list comprehension to turn all strings in list to ints
            input_values = [int(str_num) for str_num in line.split(',')]

            robot = RobotCamera(input_values)
            robot.capture_photo([0])

    result = (3 * math.pi) % (2 * math.pi)
    print(result)
    print(math.pi)



