from tkinter import filedialog, messagebox, Label, Frame, Canvas, CENTER

import os
import subprocess

from src.algorithms.bellman_ford import BellmanFordAlgorithm
from src.algorithms.bfs import BFSAlgorithm
from src.interfaces.components.button import StyledButton
from src.interfaces.components.window import DynamicWindowSize
from src.interfaces.components.list import AlgorithmSelector
from src.interfaces.difficult_view import InputDialog
from src.models.time_tracker import ResultHandler

from src.algorithms.dfs import DFSAlgorithm
from src.algorithms.a_star import AStarAlgorithm
from src.algorithms.dijkstra import DijkstraAlgorithm

from utils.csv_modules import load_maze_from_csv, save_maze_to_csv
from utils.maze_gen import generate_labyrinth


class MazeSolverApp:

    def __init__(self, root):

        self.root = root

        # Variables
        self.completed_maze = False
        self.maze = None
        self.laberinth_file_path = None

        self.algorithms = {
            "Dijkstra": self.solve_with_dijkstra,
            "Depth First Search (DFS)": self.solve_with_dfs,
            "Breadth First Search (BFS)": self.solve_with_bfs,
            "Bellman Ford": self.solve_with_bellman_ford,
            "A Search": self.solve_with_a_star
        }

        self.init_window()

    def init_window(self):

        # Configuration of the main window
        self.root.title("Maze Solver Application")
        self.root.config(bg="white")

        window_size_config = DynamicWindowSize(self.root)
        window_size_config.center_window()

        # Algorithm List
        algorithms = ["Dijkstra", "Bellman Ford", "Depth First Search (DFS)", "Breadth First Search (BFS)", "A Search"]
        default_algorithm = algorithms[0]
        self.algorithm_selector = AlgorithmSelector(self.root, algorithms, default_algorithm)
        
        # Head Buttons
        buttons_frame = Frame(self.root, bg="white")
        buttons_frame.pack(pady=10)

        StyledButton(buttons_frame, "Generar nuevo Laberinto", self.create_maze, "#3498DB", "white")
        StyledButton(buttons_frame, "Resolver Laberinto", self.solve_maze, "#E74C3C", "white")

        # Show the Maze in the Solving Area
        canvas_frame = Frame(self.root)
        canvas_frame.pack(expand=True, fill="both")

        # Create the canvas and place it in the center of the frame
        self.maze_canvas = Canvas(canvas_frame, bg="white")
        self.maze_canvas.pack(expand=True, fill="both")

        # Results
        self.results_label = Label(self.root, bg="white")
        self.results_label.pack()

        # Options frame
        options_frame = Frame(self.root, bg="white")
        options_frame.pack(pady=10)

        StyledButton(options_frame, "Limpiar Laberinto", self.clean_maze, "#E74C3C", "white")
        StyledButton(options_frame, "Resultados", self.open_results_folder, "#F39C12", "white")

    ###### MAZE SOLVER METHODS ######

    def solve_maze(self):
        
        self.clean_maze()

        # Ask for the laberinth
        self.laberinth_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if self.laberinth_file_path == "":
            return
        
        self.maze = load_maze_from_csv(self.laberinth_file_path)

        if self.maze is None:
            messagebox.showerror("Error", "Seleccione un laberinto primero.")
            return
        
        # I mean this is kind of cursed
        if not isinstance(self.maze, list):
            messagebox.showerror("Error", "El archivo seleccionado no es un laberinto.")
            return

        # Get the algortihm from the list
        selected_algorithm = self.algorithm_selector.get_selected_algorithm()
        print(f"Selected Algorithm: {selected_algorithm}")

        solving_function = self.algorithms.get(selected_algorithm)

        # Get the values for starting the algorithm first, before keeping tracking to dont add any more complexity, only the algorithm
        start_row, start_col = self.find_start_position(self.maze)
        end_row, end_col = self.find_end_position(self.maze)

        # Starts the tracking
        result_handler = ResultHandler()
        result_handler.start_timer_memory()

        # Get the algorithm function and solve the maze
        if solving_function:
            
            # Get the path from the algorithm selected
            path = solving_function(start_row, start_col, end_row, end_col)

            if path:
                self.completed_maze = True
                self.write_maze(path)
            else:
                messagebox.showinfo("Sin Solución", "No se encontró una solución para el laberinto.")

        else:
            messagebox.showerror("Error", "Algorithm not found!")

        # Stop the tracking
        result_handler.stop_timer_memory()
        
        if self.completed_maze is True:
            
            # Get the tracking results and send them to the interface and a txt
            result_text = result_handler.record_result()
            self.results_label.config(text=result_text)
            result_handler.save_result(selected_algorithm, self.laberinth_file_path, self.maze)

            # Save the solved maze into a csv file
            self.save_maze()

    def find_start_position(self, maze):
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == 2:
                    return row, col
        return -1, -1

    def find_end_position(self, maze):
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == 3:
                    return row, col
        return -1, -1

    # Change the path we got into a route for writing the maze in the canvas and the solution csv
    def show_solution_on_interface(self, path):
        for row, col in path:
            if self.maze[row][col] != 2 and self.maze[row][col] != 3: 
                self.maze[row][col] = 5 

    ###### MAZE SOLVER METHODS ######

    ###### MAZE GEN METHODS ######

    def create_maze(self):

        input_dialog = InputDialog(self.root)
        self.root.wait_window(input_dialog.dialog)
        
        rows = input_dialog.rows
        columns = input_dialog.columns
        difficulty = input_dialog.difficulty

        if rows is not None and columns is not None and difficulty:
            # Maze generator method
            new_maze = generate_labyrinth(rows, columns, difficulty) 
            self.generate_maze_csv(new_maze)  

    def generate_maze_csv(self, maze):
        
        file_path = filedialog.asksaveasfilename(filetypes=[("CSV Files", "*.csv")])

        if file_path == "":
            return

        if not file_path.endswith(".csv"):
            file_path += ".csv"
            
        save_maze_to_csv(file_path, maze)
        messagebox.showinfo("Laberinto Guardado", "Laberinto guardado con éxito!")

    def save_maze(self):
        
        solved_mazes_folder = "data/results/solved_mazes"
        os.makedirs(solved_mazes_folder, exist_ok=True)

        selected_algorithm = self.algorithm_selector.get_selected_algorithm()
        laberinth_name = self.laberinth_file_path.split("/")[-1].split(".")[0]

        file_path = f"{solved_mazes_folder}/{selected_algorithm.lower().replace(' ', '_')}{laberinth_name}.txt"

        save_maze_to_csv(file_path, self.maze) 

    ###### MAZE GEN METHODS ######

    ###### MAZE DISPLAY METHODS ######

    def write_maze(self, path=None):
        
        self.color_map = {
            0: "white",
            1: "black",
            2: "green",
            3: "red",
            4: "yellow",
            5: "blue"
        }

        # Clear the canvas
        self.maze_canvas.delete("all")  

        if self.maze and path:

            self.show_solution_on_interface(path)
            
            # Decides the maze size based on how large is the maze
            if 50 <= len(self.maze) < 75:
                cell_size = 5
            elif 75 <= len(self.maze) <= 150:
                cell_size = 3
            elif len(self.maze) > 150:
                cell_size = 2
            else:
                cell_size = 20
            
            # Get the size of the canvas
            canvas_width = self.maze_canvas.winfo_width()  
            canvas_height = self.maze_canvas.winfo_height()  

            rows = len(self.maze)
            cols = len(self.maze[0])

            # Get the size of the maze
            maze_width = cols * cell_size
            maze_height = rows * cell_size

            # Based on the canvas and the maze size look for the center of the canvas 
            x_offset = (canvas_width - maze_width) / 2
            y_offset = (canvas_height - maze_height) / 2

            for row in range(rows):
                
                # Write each cell based on the current sizes
                for col in range(cols):
                    x1 = x_offset + col * cell_size
                    y1 = y_offset + row * cell_size
                    x2 = x1 + cell_size
                    y2 = y1 + cell_size

                    value = self.maze[row][col]
                    color = self.color_map.get(value, "blue")  

                    self.maze_canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        else:

            self.maze_canvas.config(width=1, height=1)  

    def clean_maze(self):

        self.maze = None
        self.completed_maze = False
        self.write_maze()
        self.results_label.config(text="")

    ###### MAZE DISPLAY METHODS ######

    ###### OPTIONS METHODS ######

    def open_results_folder(self):
        results_folder = os.path.abspath("data/results")
        
        if os.path.exists(results_folder):
            subprocess.Popen(['explorer', results_folder])
        else:
            messagebox.showinfo("Carpeta de Resultados", "La carpeta de resultados no existe.")

    ###### OPTIONS METHODS ######

    ###### ALGORITHMS METHODS ######

    def solve_with_bfs(self, start_row, start_col, end_row, end_col):
        solver = BFSAlgorithm(self.maze)
        return solver.find_path(start_row, start_col, end_row, end_col)

    def solve_with_bellman_ford(self, start_row, start_col, end_row, end_col):
        solver = BellmanFordAlgorithm(self.maze)
        return solver.find_path(start_row, start_col, end_row, end_col)

    def solve_with_dijkstra(self, start_row, start_col, end_row, end_col):
        solver = DijkstraAlgorithm(self.maze)
        return solver.find_path(start_row, start_col, end_row, end_col)

    def solve_with_dfs(self, start_row, start_col, end_row, end_col):
        solver = DFSAlgorithm(self.maze)
        return solver.find_path(start_row, start_col, end_row, end_col)
    
    def solve_with_a_star(self, start_row, start_col, end_row, end_col):
        solver = AStarAlgorithm(self.maze)
        return solver.find_path(start_row, start_col, end_row, end_col) 
    
    ###### ALGORITHMS METHODS ######
