
class IntcodeProgram:

    def run_intcode(self, file_input):
        with open(file_input) as data:
            for line in data:
                input_values = line.split(',')
                print(input_values)
                # self.run_intcode(input)
        # turn input into an array so values are referenced by index
        # for loop over every 4 indices starting at 0
        # identify op code at index
        # identify numbers at indicies
        # perform arithmetic
        # save at new index
        # loop to next indix

    def run(self, input):
        pass

if __name__ == "__main__":
    sol = IntcodeProgram()

    sol.run_intcode("input.txt")
