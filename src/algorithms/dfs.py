
class DFSAlgorithm:
    
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.maze[row][col] != 1

    def find_path(self, start_row, start_col, end_row, end_col):
        stack = [((start_row, start_col), [(start_row, start_col)])]
        visited = set()

        while stack:
            current, path = stack.pop()

            if current == (end_row, end_col):
                return path

            visited.add(current)
            row, col = current

            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                new_position = (new_row, new_col)

                if self.is_valid(new_row, new_col) and new_position not in visited:
                    new_path = path + [new_position]
                    stack.append((new_position, new_path))
                    visited.add(new_position)

        return None  