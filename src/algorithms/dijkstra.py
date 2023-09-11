import heapq

class DijkstraAlgorithm:

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def find_path(self, start_row, start_col, end_row, end_col):
        # Initialize the open set as a priority queue with the starting node
        open_set = [(0, start_row, start_col)]
        # Initialize a dictionary to keep track of the parent nodes
        came_from = {}
        # Initialize distances to keep track of minimum distances
        distances = {(row, col): float('inf') for row in range(self.rows) for col in range(self.cols)}
        # Distance to the start node is 0
        distances[(start_row, start_col)] = 0

        # Main loop: continue until there are nodes to explore
        while open_set:
            # Get the node with the lowest f_score from the open set
            _, current_row, current_col = heapq.heappop(open_set)

            # Check if we've reached the goal node
            if (current_row, current_col) == (end_row, end_col):
                path = []
                while (current_row, current_col) in came_from:
                    path.append((current_row, current_col))
                    current_row, current_col = came_from[(current_row, current_col)]
                path.reverse()
                return path

            # Define possible movements: Right, Up, Left, Down
            for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                neighbor_row, neighbor_col = current_row + dr, current_col + dc

                # Check if the new position is valid and not visited
                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols and self.maze[neighbor_row][neighbor_col] != 1:
                    # Calculate the distance from start to current node
                    tentative_distance = distances[(current_row, current_col)] + 1

                    if tentative_distance < distances[(neighbor_row, neighbor_col)]:
                        came_from[(neighbor_row, neighbor_col)] = (current_row, current_col)
                        distances[(neighbor_row, neighbor_col)] = tentative_distance
                        heapq.heappush(open_set, (tentative_distance, neighbor_row, neighbor_col))

        return None