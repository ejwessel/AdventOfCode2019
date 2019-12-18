import math

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
                        self.asteroids[asteroid_start].add(math.degrees(rad_angle))
                    elif run < 0 and rise > 0:
                        self.asteroids[asteroid_start].add(math.degrees(rad_angle + math.pi))
                    elif run < 0 and rise < 0:
                        self.asteroids[asteroid_start].add(math.degrees(rad_angle + 2 * math.pi))
                    elif run > 0 and rise < 0:
                        self.asteroids[asteroid_start].add(math.degrees(rad_angle + 3 * math.pi))
                    else:
                        self.asteroids[asteroid_start].add(math.degrees(rad_angle))
                else:
                    if rise > 0:
                        self.asteroids[asteroid_start].add(math.degrees(math.pi))
                    else:
                        self.asteroids[asteroid_start].add(math.degrees(-math.pi))

        max_key = None
        for key, value in self.asteroids.items():
            if max_key is None:
                max_key = key
            if len(value) > len(self.asteroids[max_key]):
                max_key = key

        return max_key, len(self.asteroids[max_key])


def tests():
    grid = [
        '#.',
        '.#',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()

    grid = [
        '.#',
        '#.',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()

    grid = [
        '.#',
        '..',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()

    grid = [
        '.#',
        '.#',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()

    grid = [
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()

    grid = [
        '#.',
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()

    grid = [
        '#.',
        '#.',
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()

    grid = [
        '.#..#',
        '.....',
        '..#..',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()

    grid = [
        '#.#',
        '.#.',
        '#..',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()

    grid = [
        '#.#',
        '.#.',
        '#.#',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]


if __name__ == "__main__":

    # tests()

    grid = [
        '####',
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)
    print(sol.asteroids)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print()


    grid = [
        '.#..#',
        '.....',
        '#####',
        '....#',
        '...##'
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(sol.asteroids)
    print(best_asteroid)
    [print(key, len(value)) for key, value in sol.asteroids.items()]
