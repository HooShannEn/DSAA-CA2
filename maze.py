class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.start_pos = self.find_position('s')
        self.end_pos = self.find_position('e')

    def find_position(self, char):
        # Find the position of a given character in the maze.
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == char:
                    return (x, y)
        return None

    def is_within_bounds(self, x, y):
        # Check if a given position is within the maze bounds.
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

    def is_passable(self, x, y):
        # Check if a given position is passable (not a wall).
        return self.is_within_bounds(x, y) and self.grid[y][x] != 'X'

    def display_maze(self):
        # Print the maze layout to the console (for debugging).
        for row in self.grid:
            print(''.join(row))

    def get_start_position(self):
        # Get the start position of the maze.
        return self.start_pos

    def get_end_position(self):
        # Get the end position of the maze.
        return self.end_pos
