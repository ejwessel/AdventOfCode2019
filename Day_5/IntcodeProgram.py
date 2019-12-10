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

    def run_intcode(self, file_input):
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
                result = self.run(input_values)
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

    def save(self, input_codes, instruction_set, instruction_pointer):
        value = input("ID of the system to test: ")
        [mode_1] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        save_idx = param_1 if mode_1 == self.Modes.POSITION.value else input_codes[param_1]

        input_codes[save_idx] = int(value)

    def output(self, input_codes, instruction_set, instruction_pointer):
        [mode_1] = instruction_set[1:]
        param_1 = input_codes[instruction_pointer + 1]
        print(param_1) if mode_1 == self.Modes.IMMEDIATE.value else print(input_codes[param_1])

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

    def run(self, input_codes):
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
                self.save(input_codes, instruction_set, instruction_pointer)
                instruction_pointer += 2
            elif opcode == self.Opcodes.READ.value:
                self.output(input_codes, instruction_set, instruction_pointer)
                instruction_pointer += 2
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
        return input_codes

    def compute_noun_verb(self, file_input):
        '''
        To do this, before running the program,
        replace position 1 with the value 12 and
        replace position 2 with the value 2.
        What value is left at position 0 after the program halts?
        '''

        with open(file_input) as data:
            for line in data:
                input_values_initial = [int(str_num) for str_num in line.split(',')]
                for noun in range(99):
                    for verb in range(99):
                        input_values = input_values_initial.copy()
                        input_values[1] = noun
                        input_values[2] = verb
                        result = self.run(input_values)
                        if result[0] == 19690720:
                            return 100 * noun + verb
        return 0


if __name__ == "__main__":
    sol = IntcodeProgram()

    # input_list = [1002, 4, 3, 4, 33]
    # result = sol.run(input_list)
    # assert (result == [1002, 4, 3, 4, 99])
    #
    # input_list = [1101, 100, -1, 4, 0]
    # result = sol.run(input_list)
    # assert (result == [1101, 100, -1, 4, 99])
    #
    # input_list = [3, 0, 4, 0, 99]
    # result = sol.run(input_list)
    # # assert (result == [50, 0, 4, 0, 99]) # when input is 50
    #
    # result = sol.run_intcode("input.txt")
    # assert result[223] == 13818007

    # input_list = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    # result = sol.run(input_list)
    # assert (result == [3, 9, 8, 9, 10, 9, 4, 9, 99, 1, 8]) # when input is 8, using position mode

    # input_list = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    # result = sol.run(input_list)
    # assert (result == [3, 9, 8, 9, 10, 9, 4, 9, 99, 0, 8]) # when input is anything else, using position mode

    # input_list = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    # result = sol.run(input_list)
    # assert result == [3, 9, 7, 9, 10, 9, 4, 9, 99, 0, 8] # when input is > 8, using position mode

    # input_list = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    # result = sol.run(input_list)
    # assert result == [3, 9, 7, 9, 10, 9, 4, 9, 99, 1, 8] # when input is < 8, using position mode

    # input_list = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    # result = sol.run(input_list)
    # assert result == [3, 3, 1108, 1, 8, 3, 4, 3, 99] # when input is 8, using immediate mode

    # input_list = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    # result = sol.run(input_list)
    # assert result == [3, 3, 1108, 0, 8, 3, 4, 3, 99] # when input is anything else, using immediate mode

    # input_list = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    # result = sol.run(input_list)
    # assert result == [3, 3, 1107, 1, 8, 3, 4, 3, 99] # when input is < 8, using immediate mode

    # input_list = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    # result = sol.run(input_list)
    # assert result == [3, 3, 1107, 0, 8, 3, 4, 3, 99] # when input is > 8, using immediate mode

    # input_list = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    # result = sol.run(input_list)
    # assert result == [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 9, 1, 1, 9] # when input is not 0 in position mode
    #
    # input_list = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    # result = sol.run(input_list)
    # assert result == [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 0, 0, 1, 9] # when input is 0 in position mode

    # input_list = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1] # when input is not 0 in immediate mode
    # result = sol.run(input_list)
    # assert(result == [3, 3, 1105, 9, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
    #
    # input_list = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1] # when input is 0 in immediate mode
    # result = sol.run(input_list)
    # assert(result == [3, 3, 1105, 0, 9, 1101, 0, 0, 12, 4, 12, 99, 0])

    # if less than 8
    # input_list = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
    #               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
    #               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    # result = sol.run(input_list)
    # assert result == [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 7, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

    # if equal to 8
    # input_list = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
    #               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
    #               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    # result = sol.run(input_list)
    # assert result == [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 1000, 8, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

    # if greater than 8
    # input_list = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
    #               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
    #               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    # result = sol.run(input_list)
    # assert result == [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 1001, 9, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

    # input 5
    result = sol.run_intcode("input.txt")
    assert result == [314, 225, 1, 225, 6, 6, 1105, 1, 238, 225, 104, 0, 1101, 9, 90, 224, 1001, 224, -99, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 6, 224, 1, 223, 224, 223, 1102, 26, 62, 225, 1101, 11, 75, 225, 1101, 90, 43, 225, 2, 70, 35, 224, 101, -1716, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 4, 224, 224, 1, 223, 224, 223, 1101, 94, 66, 225, 1102, 65, 89, 225, 101, 53, 144, 224, 101, -134, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 5, 224, 1, 224, 223, 223, 1102, 16, 32, 224, 101, -512, 224, 224, 4, 224, 102, 8, 223, 223, 101, 5, 224, 224, 1, 224, 223, 223, 1001, 43, 57, 224, 101, -147, 224, 224, 4, 224, 102, 8, 223, 223, 101, 4, 224, 224, 1, 223, 224, 223, 1101, 36, 81, 225, 1002, 39, 9, 224, 1001, 224, -99, 224, 4, 224, 1002, 223, 8, 223, 101, 2, 224, 224, 1, 223, 224, 223, 1, 213, 218, 224, 1001, 224, -98, 224, 4, 224, 102, 8, 223, 223, 101, 2, 224, 224, 1, 224, 223, 223, 102, 21, 74, 224, 101, -1869, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 7, 224, 1, 224, 223, 223, 1101, 25, 15, 225, 1101, 64, 73, 225, 4, 223, 99, 3176266, 0, 20, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 1008, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 329, 1001, 223, 1, 223, 1007, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 344, 101, 1, 223, 223, 108, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 359, 101, 1, 223, 223, 108, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 374, 1001, 223, 1, 223, 7, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 389, 1001, 223, 1, 223, 8, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 404, 1001, 223, 1, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 419, 101, 1, 223, 223, 1008, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 434, 101, 1, 223, 223, 1107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 449, 1001, 223, 1, 223, 107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 464, 101, 1, 223, 223, 107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 479, 1001, 223, 1, 223, 8, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 494, 1001, 223, 1, 223, 1108, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 509, 101, 1, 223, 223, 1107, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 524, 101, 1, 223, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 539, 101, 1, 223, 223, 7, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 554, 101, 1, 223, 223, 1107, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 569, 1001, 223, 1, 223, 8, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 584, 101, 1, 223, 223, 1108, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 599, 101, 1, 223, 223, 108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 614, 101, 1, 223, 223, 1007, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 629, 1001, 223, 1, 223, 7, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 644, 101, 1, 223, 223, 1007, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 659, 1001, 223, 1, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 674, 101, 1, 223, 223, 4, 223, 99, 226]


