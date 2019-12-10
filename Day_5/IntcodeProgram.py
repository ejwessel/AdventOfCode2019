class IntcodeProgram:

    def __init__(self):
        self.HALT = 99
        self.ADD = 1
        self.MUL = 2
        self.SAVE = 3
        self.READ = 4
        self.POSITION = 0
        self.IMMEDIATE = 1


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

    def run(self, input_codes):
        # every 4 digits is an opcode
        program_counter = 0
        while True:
            instruction = input_codes[program_counter]
            instruction_set = self.get_instruction_set(instruction)
            opcode = instruction_set[0]

            if opcode == self.HALT:
                break
            elif opcode == self.ADD:
                # add
                [mode_1, mode_2, mode_3] = instruction_set[1:]
                param_1 = input_codes[program_counter + 1]
                param_2 = input_codes[program_counter + 2]
                param_3 = input_codes[program_counter + 3]

                value_1 = param_1 if mode_1 == self.IMMEDIATE else input_codes[param_1]
                value_2 = param_2 if mode_2 == self.IMMEDIATE else input_codes[param_2]
                summed_val = value_1 + value_2

                save_idx = param_3 if mode_3 == self.POSITION else input_codes[param_3]
                input_codes[save_idx] = summed_val
                program_counter += 4
            elif opcode == self.MUL:
                # multiply
                [mode_1, mode_2, mode_3] = instruction_set[1:]
                param_1 = input_codes[program_counter + 1]
                param_2 = input_codes[program_counter + 2]
                param_3 = input_codes[program_counter + 3]

                value_1 = param_1 if mode_1 == self.IMMEDIATE else input_codes[param_1]
                value_2 = param_2 if mode_2 == self.IMMEDIATE else input_codes[param_2]
                product_val = value_1 * value_2

                save_idx = param_3 if mode_3 == self.POSITION else input_codes[param_3]
                input_codes[save_idx] = product_val
                program_counter += 4
            elif opcode == self.SAVE:
                # Save
                value = input("ID of the system to test: ")

                [mode_1] = instruction_set[1:]
                param_1 = input_codes[program_counter + 1]
                save_idx = param_1 if mode_1 == self.POSITION else input_codes[param_1]

                input_codes[save_idx] = int(value)
                program_counter += 2
            elif opcode == self.READ:
                # output
                [mode_1] = instruction_set[1:]
                param_1 = input_codes[program_counter + 1]
                print(param_1) if mode_1 == self.IMMEDIATE else print(input_codes[param_1])
                program_counter += 2
            else:
                break
        return input_codes

    def get_instruction_set(self, instruction):
        # depending on the instruction we will parse the digits in some fashion
        instruction_set = []
        opcode = instruction % 100
        instruction_set.append(opcode)
        instruction = int(instruction / 100)

        if opcode == self.ADD or opcode == self.MUL:
            # look for three params
            for i in range(3):
                mode = instruction % 10
                instruction = int(instruction / 10)
                instruction_set.append(mode)
        elif opcode == self.SAVE or opcode == self.READ:
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
