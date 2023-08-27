import csv

def load_maze_from_csv(filename):
    maze = []
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            maze.append([int(cell) for cell in row])
    return maze

def save_maze_to_csv(filename, maze):
    with open(filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in maze:
            csv_writer.writerow(row)