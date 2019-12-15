from enum import Enum
from itertools import permutations


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

    def __init__(self, program):
        self.instruction_pointer = 0
        self.program = program.copy()

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

    def run(self, input_signal):
        while True:
            instruction = self.program[self.instruction_pointer]
            instruction_set = self.get_instruction_set(instruction)
            opcode = instruction_set[0]

            if opcode == self.Opcodes.HALT.value:
                return "terminated"
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
                self.instruction_pointer += 2
                return result
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
            else:
                break


def run_intcode_max_signal(phase_settings, file_input):
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

            return run_max_signal(phase_settings, input_values)


def create_amplifiers(phase_setting, program):
    amplifiers = []
    for phase in phase_setting:
        amp = IntcodeProgram(program)
        amp.run([phase])
        amplifiers.append(amp)
    return amplifiers


def run_max_signal(phase_settings, program):
    permuted_phases = permutations(phase_settings)
    max_signal = 0

    for phases in permuted_phases:
        amplifiers = create_amplifiers(phases, program)
        input_signal = 0
        for amp in amplifiers:
            input_signal = amp.run([input_signal])

        if input_signal > max_signal:
            max_signal = input_signal

    return max_signal


def run_intcode_max_signal_feedback(phase_settings, file_input):
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

            return run_max_signal_feedback(phase_settings, input_values)


def run_through_amplifiers(amplifiers, input_signal):
    for amp in amplifiers:
        input_signal = amp.run([input_signal])
    return input_signal


def run_max_signal_feedback(phase_settings, program):
    permuted_phases = permutations(phase_settings)
    max_signal = 0

    for phases in permuted_phases:
        amplifiers = create_amplifiers(phases, program)
        input_signal = 0
        while True:
            new_output = run_through_amplifiers(amplifiers, input_signal)
            if new_output is "terminated":
                break
            input_signal = new_output

        if input_signal > max_signal:
            max_signal = input_signal
    return max_signal


if __name__ == "__main__":
    program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    sol = IntcodeProgram(program)
    result = sol.run([8])
    assert result == 1
    sol = IntcodeProgram(program)
    result = sol.run([9])
    assert result == 0
    sol = IntcodeProgram(program)
    result = sol.run([7])
    assert result == 0

    program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    sol = IntcodeProgram(program)
    result = sol.run([7])
    assert result == 1
    sol = IntcodeProgram(program)
    result = sol.run([8])
    assert result == 0
    sol = IntcodeProgram(program)
    result = sol.run([9])
    assert result == 0

    program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    sol = IntcodeProgram(program)
    result = sol.run([7])
    assert result == 0
    sol = IntcodeProgram(program)
    result = sol.run([8])
    assert result == 1
    sol = IntcodeProgram(program)
    result = sol.run([9])
    assert result == 0

    program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    sol = IntcodeProgram(program)
    result = sol.run([7])
    assert result == 1
    sol = IntcodeProgram(program)
    result = sol.run([8])
    assert result == 0
    sol = IntcodeProgram(program)
    result = sol.run([9])
    assert result == 0

    program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    sol = IntcodeProgram(program)
    result = sol.run([0])
    assert result == 0
    sol = IntcodeProgram(program)
    result = sol.run([1])
    assert result == 1

    program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    sol = IntcodeProgram(program)
    result = sol.run([0])
    assert result == 0
    sol = IntcodeProgram(program)
    result = sol.run([1])
    assert result == 1

    program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
    sol = IntcodeProgram(program)
    result = sol.run([7])
    assert result == 999
    sol = IntcodeProgram(program)
    result = sol.run([8])
    assert result == 1000
    sol = IntcodeProgram(program)
    result = sol.run([9])
    assert result == 1001

    # ===============================

    program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    sol = IntcodeProgram(program)
    result = sol.run([4, 0])
    sol = IntcodeProgram(program)
    result = sol.run([3, result])
    sol = IntcodeProgram(program)
    result = sol.run([2, result])
    sol = IntcodeProgram(program)
    result = sol.run([1, result])
    sol = IntcodeProgram(program)
    result = sol.run([0, result])
    assert result == 43210

    program = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
               1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
    sol = IntcodeProgram(program)
    result = sol.run([1, 0])
    sol = IntcodeProgram(program)
    result = sol.run([0, result])
    sol = IntcodeProgram(program)
    result = sol.run([4, result])
    sol = IntcodeProgram(program)
    result = sol.run([3, result])
    sol = IntcodeProgram(program)
    result = sol.run([2, result])
    assert result == 65210

    program = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
               101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    sol = IntcodeProgram(program)
    result = sol.run([0, 0])
    sol = IntcodeProgram(program)
    result = sol.run([1, result])
    sol = IntcodeProgram(program)
    result = sol.run([2, result])
    sol = IntcodeProgram(program)
    result = sol.run([3, result])
    sol = IntcodeProgram(program)
    result = sol.run([4, result])
    assert result == 54321

    program = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    signal = run_max_signal([0, 1, 2, 3, 4], program)
    print(signal)
    assert signal == 43210

    program = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
               101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    signal = run_max_signal([0, 1, 2, 3, 4], program)
    print(signal)
    assert signal == 54321

    program = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
               1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
    signal = run_max_signal([0, 1, 2, 3, 4], program)
    print(signal)
    assert signal == 65210

    signal = run_intcode_max_signal([0, 1, 2, 3, 4], "input.txt")
    assert signal == 17406
    print(signal)

    # ===============================

    program = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
               27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
    signal = run_max_signal_feedback([5, 6, 7, 8, 9], program)
    assert signal == 139629729
    print(signal)

    program = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
               -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
               53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
    signal = run_max_signal_feedback([5, 6, 7, 8, 9], program)
    assert signal == 18216
    print(signal)

    signal = run_intcode_max_signal_feedback([5, 6, 7, 8, 9], "input.txt")
    assert  signal == 1047153
    print(signal)
