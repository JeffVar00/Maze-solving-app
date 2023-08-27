import random

def generate_labyrinth(n, m, difficulty):
    labyrinth = [[0 for _ in range(m)] for _ in range(n)]

    dictionary = {"easy": 0.25, "normal": 0.5 , "difficult": 0.75}
    obstacle_density = dictionary[difficulty]
    
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