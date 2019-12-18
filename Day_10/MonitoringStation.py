
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

                # compute the slope
                rise = asteroid_start[1] - asteroid_end[1]
                run = asteroid_start[0] - asteroid_end[0]

                # turn the values into strings because we need to keep
                if run != 0:
                    slope = rise / run
                    self.asteroids[asteroid_start].add(str(slope))
                elif rise < 0:
                    self.asteroids[asteroid_start].add(str(-1.0))
                elif rise > 0:
                    self.asteroids[asteroid_start].add(str(1.0))

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
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]

    grid = [
        '.#',
        '#.',
    ]
    sol = MonitoringStation(grid)
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]

    grid = [
        '.#',
        '..',
    ]
    sol = MonitoringStation(grid)
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]

    grid = [
        '.#',
        '.#',
    ]
    sol = MonitoringStation(grid)
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]

    grid = [
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]

    grid = [
        '#.',
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print(sol.asteroids)

    grid = [
        '#.',
        '#.',
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print(sol.asteroids)

    grid = [
        '.#..#',
        '.....',
        '..#..',
    ]
    sol = MonitoringStation(grid)
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]

    grid = [
        '.#..#',
        '.....',
        '####.',
    ]
    sol = MonitoringStation(grid)
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]
    print(sol.asteroids)

    grid = [
        '.#..#',
        '.....',
        '#####',
        '....#',
        '...##'
    ]
    sol = MonitoringStation(grid)
    best_asteroid = sol.identify_visibility()
    print(best_asteroid)


if __name__ == "__main__":

    # tests()

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

