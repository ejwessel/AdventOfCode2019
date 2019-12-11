from enum import Enum


class IntcodeProgram:
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

    class Modes(Enum):
        POSITION = 0
        IMMEDIATE = 1

    def run_intcode_max_singal(self, file_input):
        '''
        To do this, before running the program,
        replace position 1 with the value 12 and
        replace position 2 with the value 2.
        What value is left at position 0 after the program halts?
        '''

        with open(file_input) as data:
            for line in data:
                # list comprehension to turn all strings in list to ints
                input_values = [int(str_num) for str_num in line.split(',')]

                # find best combination of input values for thruster signal

                result = self.run(input_values, 0)
                return result

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
        elif opcode == self.Opcodes.SAVE.value or opcode == self.Opcodes.READ.value:
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

        value_1 = param_1 if mode_1 == self.Modes.IMMEDIATE.value else input_codes[param_1]
        value_2 = param_2 if mode_2 == self.Modes.IMMEDIATE.value else input_codes[param_2]
        summed_val = value_1 + value_2

        save_idx = param_3 if mode_3 == self.Modes.POSITION.value else input_codes[param_3]
        input_codes[save_idx] = summed_val

    def mul(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2, mode_3] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]
        param_3 = input_codes[instruction_pointer + 3]

        value_1 = param_1 if mode_1 == self.Modes.IMMEDIATE.value else input_codes[param_1]
        value_2 = param_2 if mode_2 == self.Modes.IMMEDIATE.value else input_codes[param_2]
        product_val = value_1 * value_2

        save_idx = param_3 if mode_3 == self.Modes.POSITION.value else input_codes[param_3]
        input_codes[save_idx] = product_val

    def save(self, input_codes, input_signal, instruction_set, instruction_pointer):
        # value = input("ID of the system to test: ")
        value = input_signal
        [mode_1] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        save_idx = param_1 if mode_1 == self.Modes.POSITION.value else input_codes[param_1]

        input_codes[save_idx] = int(value)

    def output(self, input_codes, instruction_set, instruction_pointer):
        [mode_1] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        return_val = param_1 if mode_1 == self.Modes.IMMEDIATE.value else input_codes[param_1]
        return return_val

    def jump_t(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]

        value_1 = param_1 if mode_1 == self.Modes.IMMEDIATE.value else input_codes[param_1]
        value_2 = param_2 if mode_2 == self.Modes.IMMEDIATE.value else input_codes[param_2]

        # set the instruction pointer to the value from the second param
        if value_1 != 0:
            return value_2
        return None

    def jump_f(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]

        value_1 = param_1 if mode_1 == self.Modes.IMMEDIATE.value else input_codes[param_1]
        value_2 = param_2 if mode_2 == self.Modes.IMMEDIATE.value else input_codes[param_2]

        # set the instruction pointer to the value from the second param
        if value_1 == 0:
            return value_2
        return None

    def less_than(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2, mode_3] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]
        param_3 = input_codes[instruction_pointer + 3]

        value_1 = param_1 if mode_1 == self.Modes.IMMEDIATE.value else input_codes[param_1]
        value_2 = param_2 if mode_2 == self.Modes.IMMEDIATE.value else input_codes[param_2]
        save_indx = param_3 if mode_3 == self.Modes.POSITION.value else input_codes[param_3]

        if value_1 < value_2:
            input_codes[save_indx] = 1
        else:
            input_codes[save_indx] = 0

    def equal(self, input_codes, instruction_set, instruction_pointer):
        [mode_1, mode_2, mode_3] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        param_2 = input_codes[instruction_pointer + 2]
        param_3 = input_codes[instruction_pointer + 3]

        value_1 = param_1 if mode_1 == self.Modes.IMMEDIATE.value else input_codes[param_1]
        value_2 = param_2 if mode_2 == self.Modes.IMMEDIATE.value else input_codes[param_2]
        save_idx = param_3 if mode_3 == self.Modes.POSITION.value else input_codes[param_3]

        if value_1 == value_2:
            input_codes[save_idx] = 1
        else:
            input_codes[save_idx] = 0

    def run(self, input_codes, input_signal):
        instruction_pointer = 0
        while True:
            instruction = input_codes[instruction_pointer]
            instruction_set = self.get_instruction_set(instruction)
            opcode = instruction_set[0]

            if opcode == self.Opcodes.HALT.value:
                break
            elif opcode == self.Opcodes.ADD.value:
                self.add(input_codes, instruction_set, instruction_pointer)
                instruction_pointer += 4
            elif opcode == self.Opcodes.MUL.value:
                self.mul(input_codes, instruction_set, instruction_pointer)
                instruction_pointer += 4
            elif opcode == self.Opcodes.SAVE.value:
                self.save(input_codes, input_signal[0], instruction_set, instruction_pointer)
                input_signal = input_signal[1:]
                instruction_pointer += 2
            elif opcode == self.Opcodes.READ.value:
                return self.output(input_codes, instruction_set, instruction_pointer)
            elif opcode == self.Opcodes.JUMP_T.value:
                new_pointer = self.jump_t(input_codes, instruction_set, instruction_pointer)
                instruction_pointer = new_pointer if new_pointer is not None else instruction_pointer + 3
            elif opcode == self.Opcodes.JUMP_F.value:
                new_pointer = self.jump_f(input_codes, instruction_set, instruction_pointer)
                instruction_pointer = new_pointer if new_pointer is not None else instruction_pointer + 3
            elif opcode == self.Opcodes.LESS_THAN.value:
                self.less_than(input_codes, instruction_set, instruction_pointer)
                instruction_pointer += 4
            elif opcode == self.Opcodes.EQUAL.value:
                self.equal(input_codes, instruction_set, instruction_pointer)
                instruction_pointer += 4
            else:
                break


if __name__ == "__main__":
    sol = IntcodeProgram()

    input_codes = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    output = 0
    for num in [4, 3, 2, 1, 0]:
        output = sol.run(input_codes, [num, output])
    assert output == 43210

    input_codes = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
                   101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    output = 0
    for num in [0, 1, 2, 3, 4]:
        output = sol.run(input_codes, [num, output])
    assert output == 54321

    input_codes = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
                   1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
    output = 0
    for num in [1, 0, 4, 3, 2]:
        output = sol.run(input_codes, [num, output])
    assert output == 65210
