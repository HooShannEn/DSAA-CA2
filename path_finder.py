from collections import deque

class _PathFinder:
    def __init__(self, maze):
        self._maze = maze

    def is_passable(self, x, y):
        # Check if a position in the maze is passable (not a wall).
        return 0 <= x < len(self._maze.grid[0]) and 0 <= y < len(self._maze.grid) and self._maze.grid[y][x] != 'X'

    # def bfs_shortest_path(self, start_pos, end_pos=None):
    #     # Use Breadth-First Search (BFS) to find the shortest path from start_pos to the endpoint 'e'.
    #     start_x, start_y = start_pos
    #     queue = deque([(start_x, start_y)])
    #     visited = set([(start_x, start_y)])
    #     parent = {}

    #     while queue:
    #         x, y = queue.popleft()

    #         if self._maze.grid[y][x] == 'e':  # If we've reached the endpoint
    #             path = []
    #             while (x, y) != (start_x, start_y):
    #                 path.append((x, y))
    #                 x, y = parent[(x, y)]
    #             path.append((start_x, start_y))
    #             path.reverse()
    #             return path

    #         for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # Explore neighbors
    #             nx, ny = x + dx, y + dy
    #             if (nx, ny) not in visited and self.is_passable(nx, ny):
    #                 visited.add((nx, ny))
    #                 queue.append((nx, ny))
    #                 parent[(nx, ny)] = (x, y)

    #     return None  # No path found

    def bfs_shortest_path(self, start_pos, end_pos=None):
        # Use Breadth-First Search (BFS) to find the shortest path from start_pos to the specified end_pos.
        start_x, start_y = start_pos
        queue = deque([(start_x, start_y)])
        visited = set([(start_x, start_y)])
        parent = {}

        while queue:
            x, y = queue.popleft()

            # Check if we've reached the specified endpoint or the default endpoint 'e'
            if (end_pos and (x, y) == end_pos) or (end_pos is None and self._maze.grid[y][x] == 'e'):
                path = []
                while (x, y) != (start_x, start_y):
                    path.append((x, y))
                    x, y = parent[(x, y)]
                path.append((start_x, start_y))
                path.reverse()
                return path

            # Explore neighbors
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and self.is_passable(nx, ny):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
                    parent[(nx, ny)] = (x, y)

        return None  # No path found
