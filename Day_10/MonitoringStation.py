
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
                self.asteroids[(x, y)] = set()

    def identify_visibility(self):
        for asteroid in self.asteroids:
            for run in range(0, self.max_x + 1):
                for rise in range(0, self.max_y + 1):
                    if rise == 0 and run == 0:
                        continue

                    # quadrant 1
                    seen = self.walk(asteroid[0] + run, asteroid[1] + rise, rise, run)
                    if seen is not None:
                        self.asteroids[asteroid].add(seen)

                    # quadrant 2
                    seen = self.walk(asteroid[0] - run, asteroid[1] + rise, rise, -run)
                    if seen is not None:
                        self.asteroids[asteroid].add(seen)

                    # quadrant 3
                    seen = self.walk(asteroid[0] - run, asteroid[1] - rise, -rise, -run)
                    if seen is not None:
                        self.asteroids[asteroid].add(seen)

                    # quadrant 4
                    seen = self.walk(asteroid[0] + run, asteroid[1] - rise, -rise, run)
                    if seen is not None:
                        self.asteroids[asteroid].add(seen)

    def walk(self, x, y, rise, run):
        if x > self.max_x or x < 0:
            # handle bounds
            return None
        elif y > self.max_y or y < 0:
            # handle bounds
            return None
        elif self.grid[y][x] is '#':
            return x, y
        else:
            return self.walk(x + run, y + rise, rise, run)

# Go through all asteroids an identify the one that can see the most


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


if __name__ == "__main__":

    # tests()

    grid = [
        '#.',
        '#.',
        '#.',
    ]
    sol = MonitoringStation(grid)
    print(sol.asteroids)
    sol.identify_visibility()
    [print(key, len(value)) for key, value in sol.asteroids.items()]

    # grid = [
    #     '.#..#',
    #     '.....',
    #     '#####',
    #     '....#',
    #     '...##'
    # ]
    # sol = MonitoringStation(grid)
    # print(sol.asteroids)
    # sol.identify_visibility()
    # [print(key, len(value)) for key, value in sol.asteroids.items()]
