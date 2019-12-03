import math


class FuelCounterUpper:
    def calculate_fuel_required(self, mass):
        result = mass / 3
        result = math.floor(result)
        result -= 2
        return result

    def fuel_requirement(self, file_input):
        sum_result = 0
        with open(file_input) as data:
            for line in data:
                number = int(line)
                fuel = self.calculate_fuel_required(number)
                sum_result += fuel
        return sum_result

if __name__ == "__main__":

    sol = FuelCounterUpper()

    result = sol.calculate_fuel_required(12)
    assert result == 2

    result = sol.calculate_fuel_required(14)
    assert result == 2

    result = sol.calculate_fuel_required(1969)
    assert result == 654

    result = sol.calculate_fuel_required(100756)
    assert result == 33583

    result = sol.fuel_requirement("Day_1/input.txt")
    print(result)