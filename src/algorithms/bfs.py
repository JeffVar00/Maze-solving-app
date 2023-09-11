from collections import deque

class BFSAlgorithm:

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def find_path(self, start_row, start_col, end_row, end_col):
        # Initialize a queue for BFS
        queue = deque([(start_row, start_col)])
        visited = set([(start_row, start_col)])
        came_from = {}

        while queue:
            current_row, current_col = queue.popleft()

            if (current_row, current_col) == (end_row, end_col):
                # Reconstruct the path
                path = []
                while (current_row, current_col) in came_from:
                    path.append((current_row, current_col))
                    current_row, current_col = came_from[(current_row, current_col)]
                path.reverse()
                return path

            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                neighbor_row, neighbor_col = current_row + dr, current_col + dc

                if (
                    0 <= neighbor_row < self.rows
                    and 0 <= neighbor_col < self.cols
                    and self.maze[neighbor_row][neighbor_col] != 1
                    and (neighbor_row, neighbor_col) not in visited
                ):
                    queue.append((neighbor_row, neighbor_col))
                    visited.add((neighbor_row, neighbor_col))
                    came_from[(neighbor_row, neighbor_col)] = (current_row, current_col)

        # No solution
        return None