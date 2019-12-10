from enum import Enum


class IntcodeProgram:

    class Opcodes(Enum):
        HALT = 99
        ADD = 1
        MUL = 2
        SAVE = 3
        READ = 4

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

    def run(self, input_codes):
        # every 4 digits is an opcode
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
            else:
                break
        return input_codes

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
        return instruction_set

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

    input_list = [1002, 4, 3, 4, 33]
    result = sol.run(input_list)
    assert (result == [1002, 4, 3, 4, 99])

    input_list = [1101, 100, -1, 4, 0]
    result = sol.run(input_list)
    assert (result == [1101, 100, -1, 4, 99])

    input_list = [3, 0, 4, 0, 99]
    result = sol.run(input_list)
    # assert (result == [50, 0, 4, 0, 99]) # when input is 50

    result = sol.run_intcode("input2.txt")
    # print(result)
