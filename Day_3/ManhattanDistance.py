from enum import Enum
import pprint
pp = pprint.PrettyPrinter(indent=2)


class ManhattanDistance:
    class DIRECTION(Enum):
        UP = 'U'
        DOWN = 'D'
        LEFT = 'L'
        RIGHT = 'R'

    def __init__(self):
        self.central_coordinates = (0, 0)
        # coordinate tuple to type
        self.seen_coords = {}
        self.distance = None

    def compute_manhattan_distance(self, coordinate):
        # absolute value since distance is never negative1
        return abs(coordinate[0]) + abs(coordinate[1])

    def compute(self, start, direction, dist, wire_type, total_dist):
        '''
        Marks all coordinate from start position in a direction and adds to set
        Will simultaneously check if wires cross and update closest coordinate
        :param start: the starting coordiante
        :param dist: the distance upwards to travel
        :return last_coordinate: the last coordinate in this direction
        '''
        current = start
        for i in range(dist):
            # coordinate builds on previous coordinate
            if direction is self.DIRECTION.UP.value:
                coordinate = (current[0], current[1] + 1)
            elif direction is self.DIRECTION.DOWN.value:
                coordinate = (current[0], current[1] - 1)
            elif direction is self.DIRECTION.LEFT.value:
                coordinate = (current[0] - 1, current[1])
            elif direction is self.DIRECTION.RIGHT.value:
                coordinate = (current[0] + 1, current[1])

            total_dist += 1

            # handle if this coordinate is the first time being seen
            if coordinate not in self.seen_coords:
                self.seen_coords[coordinate] = {}
            self.seen_coords[coordinate][wire_type] = total_dist

            # add the wire type
            # if there is more than 1 wire type at a coordinate there is an overlap
            if len(self.seen_coords[coordinate]) > 1:
                if self.distance is None:
                    self.distance = self.compute_manhattan_distance(coordinate)
                else:
                    self.distance = min(self.compute_manhattan_distance(coordinate), self.distance)

            # update current to end of last coordinate
            current = coordinate
        return current

    def add_wire(self, start, dir_dist, wire_type):
        '''
        adds a wire to the control panel
        :param dir_dist: direction distance
        :return:
        '''

        # go through all direction distances and populate seen coordinates
        last_coordinate = start
        total_distance = 0
        for item in dir_dist:
            direction = item[0]
            amount = int(item[1:])
            last_coordinate = self.compute(last_coordinate, direction, amount, wire_type, total_distance)
            total_distance += amount

    def compute_distance_file(self, file_input):
        # wire num to distances
        wires = []
        with open(file_input) as data:
            for line in data:
                distances = line.split(',')
                wires.append(distances)

        self.compute_distance(wires)

    def compute_distance(self, wires):
        wire_type = 0
        for wire in wires:
            self.add_wire(self.central_coordinates, wire, wire_type)
            wire_type += 1

    def get_least_steps(self):
        min_distance = None
        for coordinate, wire in sol.seen_coords.items():
            if len(wire) > 1:
                if min_distance is None:
                    min_distance = 0
                    for value in wire.values():
                        min_distance += value
                else:
                    temp_distance = 0
                    for value in wire.values():
                        temp_distance += value
                    if temp_distance < min_distance:
                        min_distance = temp_distance
        return min_distance


if __name__ == "__main__":
    sol = ManhattanDistance()
    result = sol.compute((0, 0), 'U', 50, 1, 0)
    assert result == (0, 50)
    assert len(sol.seen_coords) == 50

    sol = ManhattanDistance()
    result = sol.compute((0, 0), 'D', 50, 1, 0)
    assert result == (0, -50)
    assert len(sol.seen_coords) == 50

    sol = ManhattanDistance()
    result = sol.compute((0, 0), 'L', 50, 1, 0)
    assert result == (-50, 0)
    assert len(sol.seen_coords) == 50

    sol = ManhattanDistance()
    result = sol.compute((0, 0), 'R', 50, 1, 0)
    assert result == (50, 0)
    assert len(sol.seen_coords) == 50

    sol = ManhattanDistance()
    result = sol.compute((0, 0), 'U', 50, 1, 0)
    assert result == (0, 50)
    assert len(sol.seen_coords) == 50
    result = sol.compute((0, 0), 'U', 50, 2, 0)
    assert result == (0, 50)
    assert len(sol.seen_coords) == 50

    sol = ManhattanDistance()
    sol.compute_distance([['R8', 'U5', 'L5', 'D3'],
                          ['U7', 'R6', 'D4', 'L4']])
    assert sol.distance == 6

    sol = ManhattanDistance()
    sol.compute_distance([['R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53', 'R51'],
                          ['U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7']])
    assert sol.distance == 135

    sol = ManhattanDistance()
    sol.compute_distance([['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
                          ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83']])
    assert sol.distance == 159

    sol = ManhattanDistance()
    sol.compute_distance_file("input.txt")
    steps = sol.get_least_steps()
    assert sol.distance == 399
    assert steps == 15678

