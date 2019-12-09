class IntcodeProgram:

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
                input_values[1] = 12
                input_values[2] = 2
                result = self.run(input_values)
                return result

    def run(self, input_codes):
        # every 4 digits is an opcode
        i = 0
        while True:
            opcode = input_codes[i]
            if opcode == 99:
                break
            elif opcode == 1:
                # add
                n1_idx = input_codes[i + 1]
                n2_idx = input_codes[i + 2]
                summed_val = input_codes[n1_idx] + input_codes[n2_idx]
                save_idx = input_codes[i + 3]
                input_codes[save_idx] = summed_val
                i += 4
            elif opcode == 2:
                # multiply
                n1_idx = input_codes[i + 1]
                n2_idx = input_codes[i + 2]
                product_val = input_codes[n1_idx] * input_codes[n2_idx]
                save_idx = input_codes[i + 3]
                input_codes[save_idx] = product_val
                i += 4
            elif opcode == 3:
                # Save
                value = input("ID of the system to test: ")
                n1_idx = input_codes[i + 1]
                input_codes[n1_idx] = int(value)
                i += 2
            elif opcode == 4:
                # output
                n1_idx = input_codes[i + 1]
                value = input_codes[n1_idx]
                print(value)
                i += 2
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

    input_list = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    result = sol.run(input_list)
    assert result == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]

    input_list = [1, 0, 0, 0, 99]
    result = sol.run(input_list)
    assert result == [2, 0, 0, 0, 99]

    input_list = [2, 3, 0, 3, 99]
    result = sol.run(input_list)
    assert result == [2, 3, 0, 6, 99]

    input_list = [2, 4, 4, 5, 99, 0]
    result = sol.run(input_list)
    assert result == [2, 4, 4, 5, 99, 9801]

    input_list = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    result = sol.run(input_list)
    assert result == [30, 1, 1, 4, 2, 5, 6, 0, 99]

    result = sol.run_intcode("input.txt")
    assert result == [4714701, 12, 2, 2, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 13, 1, 60, 1, 5, 19, 61, 2, 10, 23, 244,
                      1, 27, 5, 245, 2, 9, 31, 735, 1, 35, 5, 736, 2, 6, 39, 1472, 1, 43, 5, 1473, 2, 47, 10, 5892, 2,
                      51, 6, 11784, 1, 5, 55, 11785, 2, 10, 59, 47140, 1, 63, 6, 47142, 2, 67, 6, 94284, 1, 71, 5,
                      94285, 1, 13, 75, 94290, 1, 6, 79, 94292, 2, 83, 13, 471460, 1, 87, 6, 471462, 1, 10, 91, 471466,
                      1, 95, 9, 471469, 2, 99, 13, 2357345, 1, 103, 6, 2357347, 2, 107, 6, 4714694, 1, 111, 2, 4714696,
                      1, 115, 13, 0, 99, 2, 0, 14, 0]
    assert result[0] == 4714701
    print(result[0])

    result = sol.compute_noun_verb("input.txt")
    print(result)

    input_list = [3, 0, 4, 0, 99]
    result = sol.run(input_list)
