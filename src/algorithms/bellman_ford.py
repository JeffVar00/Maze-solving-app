class BellmanFordAlgorithm:

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def find_path(self, start_row, start_col, end_row, end_col):
        distances = {(row, col): float('inf') for row in range(self.rows) for col in range(self.cols)}
        distances[(start_row, start_col)] = 0
        predecessors = {}
        no_update = True  # Flag for early exit

        # Number of iterations is usually (V - 1) where V is the number of vertices
        for _ in range(self.rows * self.cols - 1):
            no_update = True
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.maze[row][col] != 1:
                        for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                            neighbor_row, neighbor_col = row + dr, col + dc

                            if (
                                    0 <= neighbor_row < self.rows
                                    and 0 <= neighbor_col < self.cols
                                    and self.maze[neighbor_row][neighbor_col] != 1
                            ):
                                current_distance = distances[(row, col)] + 1

                                # Check if the new distance is less than the current distance
                                if current_distance < distances[(neighbor_row, neighbor_col)]:
                                    distances[(neighbor_row, neighbor_col)] = current_distance
                                    predecessors[(neighbor_row, neighbor_col)] = (row, col)
                                    no_update = False  # A distance was updated

            if no_update:
                break

        path = []

        # Check if a path exists
        if (end_row, end_col) not in predecessors:
            return None

        current_row, current_col = end_row, end_col
        while (current_row, current_col) != (start_row, start_col):
            path.append((current_row, current_col))
            current_row, current_col = predecessors[(current_row, current_col)]
        path.append((start_row, start_col))
        path.reverse()

        return path