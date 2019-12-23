import math
from operator import itemgetter

class MonitoringStation:

    def __init__(self, grid):
        self.grid = grid
        self.max_x = len(grid[0]) - 1
        self.max_y = len(grid) - 1
        self.asteroids = {}
        self.locate_asteroids()

    def locate_asteroids(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] is not '#':
                    continue

                # slope will be added to set if there is 1 asteroid on it
                self.asteroids[(x, y)] = set()

    def identify_visibility(self):
        for asteroid_start in self.asteroids:
            for asteroid_end in self.asteroids:
                if asteroid_start is asteroid_end:
                    continue

                rise = asteroid_start[1] - asteroid_end[1]
                run = asteroid_start[0] - asteroid_end[0]

                if run != 0:
                    slope = rise / run
                    rad_angle = math.atan(slope)

                    if run > 0 and rise > 0:
                        # quadrant 1
                        self.asteroids[asteroid_start].add(math.degrees(rad_angle))
                    elif run < 0 and rise > 0:
                        # quadrant 2
                        self.asteroids[asteroid_start].add(math.degrees(rad_angle + math.pi))
                    elif run < 0 and rise < 0:
                        # quadrant 3
                        self.asteroids[asteroid_start].add(math.degrees(rad_angle + 2 * math.pi))
                    elif run > 0 and rise < 0:
                        # quadrant 4
                        self.asteroids[asteroid_start].add(math.degrees(rad_angle + 3 * math.pi))
                    elif str(rad_angle) == "0.0":
                        # pointing directly to right
                        self.asteroids[asteroid_start].add(math.degrees(0.0))
                    elif str(rad_angle) == "-0.0":
                        # pointing directly to left
                        self.asteroids[asteroid_start].add(math.degrees(math.pi))
                else:
                    if rise > 0:
                        # pointing directly up
                        self.asteroids[asteroid_start].add(math.degrees(math.pi / 2))
                    else:
                        # pointing directly down
                        self.asteroids[asteroid_start].add(math.degrees(-math.pi / 2))

        max_key = None
        for key, value in self.asteroids.items():
            if max_key is None:
                max_key = key
            if len(value) > len(self.asteroids[max_key]):
                max_key = key

        return max_key, len(self.asteroids[max_key])

    def distance_between(self, coord_1, coord_2):
        y_delta = (coord_2[1] - coord_1[1])
        y_product = math.pow(y_delta, 2)
        x_delta = (coord_2[0] - coord_1[0])
        x_product = math.pow(x_delta, 2)
        y_x_sum = y_product + x_product
        return math.pow(y_x_sum, 0.5)

    def save_distance_from_pivot(self, angle_set, angle, pivot, asteroid):
        if angle not in angle_set:
            angle_set[angle] = []
        distance = self.distance_between(pivot, asteroid)
        angle_set[angle].append((asteroid, distance))

    def vaporize(self, pivot):
        angle_set = {}

        for asteroid in self.asteroids:
            if pivot == asteroid:
                continue

            rise = pivot[1] - asteroid[1]
            run = pivot[0] - asteroid[0]

            if run != 0:
                slope = rise / run
                rad_angle = math.atan(slope)

                # The distance of the coordinate is saved with the coordinate

                if run > 0 and rise > 0:
                    # quadrant 1
                    key = (math.degrees(rad_angle))
                    self.save_distance_from_pivot(angle_set, key, pivot, asteroid)
                elif run < 0 and rise > 0:
                    # quadrant 2
                    key = (math.degrees(rad_angle + math.pi))
                    self.save_distance_from_pivot(angle_set, key, pivot, asteroid)
                elif run < 0 and rise < 0:
                    # quadrant 3
                    key = (math.degrees(rad_angle + 2 * math.pi))
                    self.save_distance_from_pivot(angle_set, key, pivot, asteroid)
                elif run > 0 and rise < 0:
                    # quadrant 4
                    key = (math.degrees(rad_angle + 3 * math.pi))
                    self.save_distance_from_pivot(angle_set, key, pivot, asteroid)
                elif str(rad_angle) == "0.0":
                    # pointing directly to right
                    key = (math.degrees(0.0))
                    self.save_distance_from_pivot(angle_set, key, pivot, asteroid)
                elif str(rad_angle) == "-0.0":
                    # pointing directly to right
                    key = (math.degrees(math.pi))
                    self.save_distance_from_pivot(angle_set, key, pivot, asteroid)
            else:
                if rise > 0:
                    # pointing directly up
                    key = (math.degrees(math.pi / 2))
                    self.save_distance_from_pivot(angle_set, key, pivot, asteroid)
                else:
                    # pointing directly down
                    key = (math.degrees(-math.pi / 2))
                    self.save_distance_from_pivot(angle_set, key, pivot, asteroid)

        # sort the internal angle lists by distance
        for key in angle_set:
            new_list = sorted(angle_set[key], key=itemgetter(1))
            angle_set[key] = new_list

        angle_list = list(angle_set.items())
        sorted_angle_list = sorted(angle_list, key=itemgetter(0))
        # print(sorted_angle_list)

        key_idx = {}
        for key in angle_set.keys():
            key_idx[key] = 0
        # print(key_idx)

        idx = 0
        # identify order of output
        output_list = []
        while len(sorted_angle_list) > 0:
            current_pairing = sorted_angle_list[idx]
            # print(current_pairing)

            key = current_pairing[0]
            key_list = current_pairing[1]

            current_key_idx = key_idx[key]
            output_list.append(key_list[current_key_idx][0])
            # print(key_list[current_key_idx])

            key_idx[key] += 1
            # if idx key is greater than list at that angle then remove it
            if key_idx[key] >= len(key_list):
                sorted_angle_list.remove(current_pairing)

            # if there are no more elements, exit
            if len(sorted_angle_list) == 0:
                break

            idx += 1
            idx %= len(sorted_angle_list)

        return output_list


def tests():
    grid = [
        '#.',
        '.#',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((0, 0), 1)

    grid = [
        '.#',
        '#.',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((1, 0), 1)

    grid = [
        '.#',
        '..',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((1, 0), 0)

    grid = [
        '.#',
        '.#',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((1, 0), 1)

    grid = [
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((0, 0), 1)

    grid = [
        '#.',
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((0, 1), 2)

    grid = [
        '#.',
        '#.',
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((0, 1), 2)

    grid = [
        '.#..#',
        '.....',
        '..#..',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((1, 0), 2)

    grid = [
        '#.#',
        '.#.',
        '#..',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((0, 0), 3)

    grid = [
        '#.#',
        '.#.',
        '#.#',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((1, 1), 4)

    grid = [
        '####',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((1, 0), 2)

    grid = [
        '.#..#',
        '.....',
        '#####',
        '....#',
        '...##'
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((3, 4), 8)

    grid = [
        '......#.#.',
        '#..#.#....',
        '..#######.',
        '.#.#.###..',
        '.#..#.....',
        '..#....#.#',
        '#..#....#.',
        '.##.#..###',
        '##...#..#.',
        '.#....####'
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((5, 8), 33)

    grid = [
        '#.#...#.#.',
        '.###....#.',
        '.#....#...',
        '##.#.#.#.#',
        '....#.#.#.',
        '.##..###.#',
        '..#...##..',
        '..##....##',
        '......#...',
        '.####.###.'
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((1, 2), 35)

    grid = [
        '.#..#..###',
        '####.###.#',
        '....###.#.',
        '..###.##.#',
        '##.##.#.#.',
        '....###..#',
        '..#.#..#.#',
        '#..#.#.###',
        '.##...##.#',
        '.....#.#..'
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((6, 3), 41)

    grid = [
        '.#..##.###...#######',
        '##.############..##.',
        '.#.######.########.#',
        '.###.#######.####.#.',
        '#####.##.#.##.###.##',
        '..#####..#.#########',
        '####################',
        '#.####....###.#.#.##',
        '##.#################',
        '#####.##.###..####..',
        '..######..##.#######',
        '####.##.####...##..#',
        '.#####..#.######.###',
        '##...#.##########...',
        '#.##########.#######',
        '.####.#.###.###.#.##',
        '....##.##.###..#####',
        '.#.#.###########.###',
        '#.#.#.#####.####.###',
        '###.##.####.##.#..##'
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((11, 13), 210)

    grid = []
    with open("input.txt") as data:
        for line in data:
            grid.append(line.rstrip())

    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    assert best_asteroid == ((13, 17), 269)

if __name__ == "__main__":

    tests()

    grid = [
        '#...#',
        '.#.#.',
        '..#..',
        '.#.#.',
        '#...#',
    ]
    sol = MonitoringStation(grid)
    result = sol.vaporize((2, 2))
    print(result)

    result = sol.distance_between((-2, 1), (1, 5))
    assert result == 5.0

    result = sol.distance_between((-2, -3), (-4, 4))
    result = round(result, 2)
    assert result == 7.28

