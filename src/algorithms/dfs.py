class DFSAlgorithm:

    # Iterative Solution algorithm
    # Inspired on https://medium.com/swlh/solving-mazes-with-depth-first-search-e315771317ae, https://www.geeksforgeeks.org/depth-first-traversal-dfs-on-a-2d-array/, https://www.algosome.com/articles/maze-generation-depth-first.html

    def __init__(self, maze):
        # Variables
        self.maze = maze
        self.rows = len(maze) # Rows
        self.cols = len(maze[0]) # Cols

    def find_path(self, start_row, start_col, end_row, end_col):
        # For solving this algorithm I will be using a stack starting at the first position of the maze
        stack = [((start_row, start_col), [(start_row, start_col)])] 

        # And to keep track of visited columns I will be using a visited set of tuples
        visited = set()  

        # While I have a solution/starting poing
        while stack:

            # Get the current position and the path at this moment taken to reach it, the path always starts at the first position
            current, path = stack.pop()  

            # When match with the tuple sent by the function at first
            if current == (end_row, end_col):
                return path  

            # Add tuple
            visited.add(current)

            # Change current
            row, col = current

            # Possible movements: Right, Up, Left, Down
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)] 

            # dr: direction for row, dc: direction for column 
            # (dr, dc)
            for dr, dc in directions: 

                new_row, new_col = row + dr, col + dc
                new_position = (new_row, new_col)

                # For every possible direction, check if the new position is valid and not visited

                if self.is_valid(new_row, new_col) and new_position not in visited:

                    # Extend the current path to include the new tuple position
                    new_path = path + [new_position]  
                    
                    # Add the new position to the stack (new current) and updated path in the stack
                    stack.append((new_position, new_path))  
                    visited.add(new_position)

        # No solution
        return None 
    
    # Check if the given position (row, col) is within the maze boundaries and not a wall (1)
    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols and self.maze[row][col] != 1