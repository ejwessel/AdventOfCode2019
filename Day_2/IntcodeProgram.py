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
                input_values = line.split(',')
                input_values[1] = 12
                input_values[2] = 2
                print(input_values)
                result = self.run(input_values)
                print(result)

    def run(self, input):
        # every 4 digits is an opcode
        for i in range(0, len(input), 4):
            opcode = int(input[i])
            if opcode == 99:
                break
            elif opcode == 1:
                # add
                n1_idx = int(input[i + 1])
                n2_idx = int(input[i + 2])
                summed_val = int(input[n1_idx]) + int(input[n2_idx])
                save_idx = int(input[i + 3])
                input[save_idx] = summed_val
            elif opcode == 2:
                # multiply
                n1_idx = int(input[i + 1])
                n2_idx = int(input[i + 2])
                product_val = int(input[n1_idx]) * int(input[n2_idx])
                save_idx = int(input[i + 3])
                input[save_idx] = product_val
            else:
                break
        return input


if __name__ == "__main__":
    sol = IntcodeProgram()

    # input_list = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    # result = sol.run(input_list)
    # assert result == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    #
    # input_list = [1, 0, 0, 0, 99]
    # result = sol.run(input_list)
    # assert result == [2, 0, 0, 0, 99]
    #
    # input_list = [2, 3, 0, 3, 99]
    # result = sol.run(input_list)
    # assert result == [2, 3, 0, 6, 99]
    #
    # input_list = [2, 4, 4, 5, 99, 0]
    # result = sol.run(input_list)
    # assert result == [2, 4, 4, 5, 99, 9801]
    #
    # input_list = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    # result = sol.run(input_list)
    # assert result == [30, 1, 1, 4, 2, 5, 6, 0, 99]

    result = sol.run_intcode("input.txt")
    print(result)


