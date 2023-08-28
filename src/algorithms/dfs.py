
class DFSAlgorithm:
    
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and not self.visited[row][col] and self.maze[row][col] != 1

    def dfs(self, row, col, path):
        if not self.is_valid(row, col):
            return False
        
        path.append((row, col))
        self.visited[row][col] = True

        if self.maze[row][col] == 3:  # Si es la meta
            return True

        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Abajo, Derecha, Arriba, Izquierda
        for dr, dc in directions:
            if self.dfs(row + dr, col + dc, path):
                return True

        path.pop()
        return False

    def find_path(self, start_row, start_col, end_row, end_col):
        path = []
        self.dfs(start_row, start_col, path)
        return path
        