import random

def generate_labyrinth(n, m, obstacle_density):
    labyrinth = [[0 for _ in range(m)] for _ in range(n)]
    
    start = (random.randint(0, n - 1), random.randint(0, m - 1))
    end = (random.randint(0, n - 1), random.randint(0, m - 1))

    for row in range(n):
        for col in range(m):
            if (row, col) == start:
                labyrinth[row][col] = 2  # Start
            elif (row, col) == end:
                labyrinth[row][col] = 3  # End
            else:
                if random.random() < obstacle_density:
                    labyrinth[row][col] = 1  # Wall
                else:
                    labyrinth[row][col] = 0  # Road

    return labyrinth

## Example usage
# n = 5
# m = 5

# obstacle_density = 0.3  # Difficulty 0-1 -- 0-Easier-0.5-harder-1

# labyrinth_matrix = generate_labyrinth(n, m, obstacle_density)

## Print the generated labyrinth
# for row in labyrinth_matrix:
#     print(" ".join(map(str, row)))