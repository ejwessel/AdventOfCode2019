
class MonitoringStation:

    def __init__(self, grid):
        self.grid = grid
        self.max_x = len(grid[0]) - 1
        self.max_y = len(grid) - 1
        self.asteroids = {}
        self.locate_asteroids()

    def locate_asteroids(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if self.grid[row][col] is not '#':
                    continue
                self.asteroids[(row, col)] = 0

    def identify_visibility(self):
        for asteroid in self.asteroids:
            for run in range(0, self.max_x + 1):
                for rise in range(0, self.max_y + 1):
                    if rise == 0 and run == 0:
                        continue

                    # quadrant 1
                    seen = self.walk(asteroid[0] + run, asteroid[1] + rise, rise, run)
                    self.asteroids[asteroid] += seen

                    # quadrant 2
                    seen = self.walk(asteroid[0] - run, asteroid[1] + rise, rise, -run)
                    self.asteroids[asteroid] += seen

                    # quadrant 3
                    seen = self.walk(asteroid[0] - run, asteroid[1] - rise, -rise, -run)
                    self.asteroids[asteroid] += seen

                    # quadrant 4
                    seen = self.walk(asteroid[0] + run, asteroid[1] - rise, -rise, run)
                    self.asteroids[asteroid] += seen

    def walk(self, x, y, rise, run):
        if x > self.max_x or x < 0:
            # handle bounds
            return 0
        elif y > self.max_y or y < 0:
            # handle bounds
            return 0
        elif self.grid[x][y] is '#':
            return 1
        else:
            return self.walk(x + run, y + rise, rise, run)

# Go through all asteroids an identify the one that can see the most

if __name__ == "__main__":

    grid = [
        '.#..#',
        '.....',
        '#####',
        '....#',
        '...##'
    ]
    sol = MonitoringStation(grid)
    sol.identify_visibility()
    print(sol.asteroids)



