class NBodyProblem:

    def __init__(self, file_input):
        self.planet_dict = dict() # maps coordinate to velocity
        with open(file_input) as data:
            for line in data:
                line = line.rstrip()
                line = line[1:-1]
                # this line extracts the x, y, z values into a list
                coordiantes = [int(comp.strip()[2:]) for comp in line.split(",")]
                self.planet_dict[tuple(coordiantes)] = [0, 0, 0]
        self.printState(self.planet_dict)

    def printState(self, plant_state):
        # print starting info
        for key, value in plant_state.items():
            print(f'{key} : {value}')
        print()

    def runSimulation(self, steps):
        # compute velocities
        current_step = 0
        while current_step < steps:
            planet_dict = self.planet_dict.copy()
            for coord in planet_dict.keys():
                for other_coord in planet_dict.keys():
                    # skip over coordinates that are the same
                    if other_coord is coord:
                        continue

                    # generate velocity for the the coordinate to update
                    velocity = planet_dict[coord]
                    deltas = self._compute_velocity_vals(coord, other_coord)
                    new_velocity = []
                    for (v1, v2) in zip(velocity, deltas):
                        new_velocity.append(v1 + v2)
                    planet_dict[coord] = new_velocity

            # update the coordinates with the generated velocity
            new_planet_dict = dict()
            for coord, velocity in planet_dict.items():
                new_coord = []
                for (item1, item2) in zip(coord, velocity):
                    new_coord.append(item1 + item2)
                new_planet_dict[tuple(new_coord)] = velocity

            # update state
            self.planet_dict = new_planet_dict
            self.printState(self.planet_dict)
            current_step += 1

    def _compute_velocity_vals(self, start_coord, other_coord):
        return_coord = [0, 0, 0]
        # X
        if start_coord[0] > other_coord[0]:
            return_coord[0] -= 1
        elif start_coord[0] < other_coord[0]:
            return_coord[0] += 1
        # Y
        if start_coord[1] > other_coord[1]:
            return_coord[1] -= 1
        elif start_coord[1] < other_coord[1]:
            return_coord[1] += 1
        # Z
        if start_coord[2] > other_coord[2]:
            return_coord[2] -= 1
        elif start_coord[2] < other_coord[2]:
            return_coord[2] += 1
        return return_coord

    def _computeEnergy(self, coordinate, velocity):
        potential = sum(abs(val) for val in coordinate)
        kinetic = sum(abs(val) for val in velocity)
        return potential * kinetic

    def computeTotalEnergy(self):
        total = 0
        for coord, velocity in self.planet_dict.items():
            total += self._computeEnergy(coord, velocity)
        return total


if __name__ == '__main__':

    sol = NBodyProblem('test_input_1.txt')

    delta = sol._compute_velocity_vals((-1, 0, 2), (2, -10, -7))
    assert delta == [1, -1, -1]

    delta = sol._compute_velocity_vals((-1, 0, 2), (-1, 0, 2))
    assert delta == [0, 0, 0]

    sol.runSimulation(10)
    assert sol.planet_dict == {(2, 1, -3): [-3, -2, 1], (1, -8, 0): [-1, 1, 3], (3, -6, 1): [3, 2, -3], (2, 0, 4): [1, -1, -1]}

    key = list(sol.planet_dict.keys())[0]
    value = sol.planet_dict[key]
    energy = sol._computeEnergy(key, value)
    assert energy == 36

    key = list(sol.planet_dict.keys())[1]
    value = sol.planet_dict[key]
    energy = sol._computeEnergy(key, value)
    assert energy == 45

    total_energy = sol.computeTotalEnergy()
    assert total_energy == 179

    sol = NBodyProblem('test_input_2.txt')
    sol.runSimulation(100)
    total_energy = sol.computeTotalEnergy()
    assert total_energy == 1940

    sol = NBodyProblem('input.txt')
    sol.runSimulation(1000)
    total_energy = sol.computeTotalEnergy()
    print(total_energy)
