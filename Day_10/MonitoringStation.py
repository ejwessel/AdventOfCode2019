
class MonitoringStation:

    def __init__(self, grid):
        self.grid = grid
        self.max_x = len(grid[0])
        self.max_y = len(grid)
        self.asteroids = {}
        self.locate_asteroids()

    def locate_asteroids(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if self.grid[row][col] is not '#':
                    continue
                self.asteroids[(row, col)] = 0

# go through rows and columns
# save all asteroid spots in set
#   (x, y) = 0
#   set will be used to keep count seen
# compute the max numerator for slope
# compute the max denominator for slope
# Go through all asteroids
#   compute all possible slopes (+ / -)
#   starting at asteroid coordinate walk in direction until end of see asteroid
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


