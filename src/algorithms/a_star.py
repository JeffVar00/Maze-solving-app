import heapq

class AStarAlgorithm:

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def heuristic(self, current, goal):
        # Calculate the Manhattan distance heuristic
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def find_path(self, start_row, start_col, end_row, end_col):
        # Open set using a priority queue (heap)
        open_set = [(0, start_row, start_col)]
        came_from = {}  # Store the parent nodes for constructing the path

        g_scores = {(row, col): float('inf') for row in range(self.rows) for col in range(self.cols)}
        g_scores[(start_row, start_col)] = 0

        f_scores = {(row, col): float('inf') for row in range(self.rows) for col in range(self.cols)}
        f_scores[(start_row, start_col)] = self.heuristic((start_row, start_col), (end_row, end_col))

        while open_set:
            _, current_row, current_col = heapq.heappop(open_set)

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

                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols and self.maze[neighbor_row][neighbor_col] != 1:
                    tentative_g_score = g_scores[(current_row, current_col)] + 1
                    if tentative_g_score < g_scores[(neighbor_row, neighbor_col)]:
                        came_from[(neighbor_row, neighbor_col)] = (current_row, current_col)
                        g_scores[(neighbor_row, neighbor_col)] = tentative_g_score
                        f_scores[(neighbor_row, neighbor_col)] = tentative_g_score + self.heuristic((neighbor_row, neighbor_col), (end_row, end_col))
                        heapq.heappush(open_set, (f_scores[(neighbor_row, neighbor_col)], neighbor_row, neighbor_col))

        return None  # No path found