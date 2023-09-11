import heapq


class AStarAlgorithm:
    # Iterative Solution

    # Inspired on the code provieded by the professor, https://www.geeksforgeeks.org/a-search-algorithm/ and https://www.simplilearn.com/tutorials/artificial-intelligence-tutorial/a-star-algorithm

    def __init__(self, maze):
        # Variables
        self.maze = maze
        self.rows = len(maze)  # Rows
        self.cols = len(maze[0])  # Cols

    def heuristic(self, current, goal):
        # Calculate the Manhattan Distance Heuristic
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def find_path(self, start_row, start_col, end_row, end_col):
        # For solving this algorithm I will be using a priority queue (heap) starting at the first position of the maze, using a set of tuples
        open_set = [(0, start_row, start_col)]

        # And to keep track of the parent nodes for constructing the path
        came_from = {}

        # g_score: distance from start to current node
        g_scores = {
            (row, col): float("inf")
            for row in range(self.rows)
            for col in range(self.cols)
        }
        g_scores[(start_row, start_col)] = 0

        # f_score: g_score + heuristic
        f_scores = {
            (row, col): float("inf")
            for row in range(self.rows)
            for col in range(self.cols)
        }
        f_scores[(start_row, start_col)] = self.heuristic(
            (start_row, start_col), (end_row, end_col)
        )

        # While I have a solution/starting poing
        while open_set:
            # Get the current position and the path at this moment taken to reach it, the path always starts at the first position
            _, current_row, current_col = heapq.heappop(open_set)

            # When match with the end tuple sent by the function at first
            if (current_row, current_col) == (end_row, end_col):
                # Reconstruct the path
                path = []
                while (current_row, current_col) in came_from:
                    path.append((current_row, current_col))
                    current_row, current_col = came_from[(current_row, current_col)]
                path.reverse()
                return path

            # Possible movements: Right, Up, Left, Down
            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                neighbor_row, neighbor_col = current_row + dr, current_col + dc

                # Check if the new position is valid and not visited
                if (
                    0 <= neighbor_row < self.rows
                    and 0 <= neighbor_col < self.cols
                    and self.maze[neighbor_row][neighbor_col] != 1
                ):
                    # Calculate the tentative g score which is the distance from start to current node
                    tentative_g_score = g_scores[(current_row, current_col)] + 1

                    # If the tentative g score is less than the current g score, update the parent node and the g score
                    if tentative_g_score < g_scores[(neighbor_row, neighbor_col)]:
                        came_from[(neighbor_row, neighbor_col)] = (
                            current_row,
                            current_col,
                        )
                        g_scores[(neighbor_row, neighbor_col)] = tentative_g_score
                        f_scores[
                            (neighbor_row, neighbor_col)
                        ] = tentative_g_score + self.heuristic(
                            (neighbor_row, neighbor_col), (end_row, end_col)
                        )
                        heapq.heappush(
                            open_set,
                            (
                                f_scores[(neighbor_row, neighbor_col)],
                                neighbor_row,
                                neighbor_col,
                            ),
                        )
        # No solution
        return None
