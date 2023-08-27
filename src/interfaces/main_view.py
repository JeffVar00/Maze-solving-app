import tracemalloc
import time
import os

from tkinter import filedialog, messagebox, Label, Frame

from src.interfaces.components.button import StyledButton
from src.interfaces.components.window import DynamicWindowSize
from src.interfaces.components.list import AlgorithmSelector
from src.interfaces.difficult_view import InputDialog
from src.models.time_tracker import ResultHandler

from utils.csv_modules import load_maze_from_csv, save_maze_to_csv
from utils.maze_gen import generate_labyrinth


class MazeSolverApp:

    def __init__(self, root):

        self.root = root

        # Configuration of the main window
        self.root.title("Maze Solver Application")
        self.root.configure(bg="#F0F0F0")  

        window_size_config = DynamicWindowSize(root)
        window_size_config.center_window()

        # Algorithm List
        algorithms = ["Algoritmo 1", "Algoritmo 2", "Algoritmo 3"]
        default_algorithm = algorithms[0]
        self.algorithm_selector = AlgorithmSelector(self.root, algorithms, default_algorithm)
        
        # Head Buttons
        buttons_frame = Frame(root)
        buttons_frame.pack(pady=10)

        StyledButton(buttons_frame, "Generar nuevo Laberinto", self.create_maze, "#3498DB", "white")
        StyledButton(buttons_frame, "Resolver Laberinto", self.solve_maze, "#E74C3C", "white")

        # Maze Solving Area
        maze_label = Label(root, text="Maze Area")
        maze_label.pack(pady=10) 

        # Bottom Buttons
        save_frame = Frame(root)
        save_frame.pack(pady=10)

        StyledButton(save_frame, "Guardar Laberinto", self.save_maze, "#2ECC71", "white")
        
        # Variables
        self.completed_maze = False
        self.maze = None
        self.laberinth_file_path = None

    def create_maze(self):

        input_dialog = InputDialog(self.root)
        self.root.wait_window(input_dialog.dialog)
        
        rows = input_dialog.rows
        columns = input_dialog.columns
        difficulty = input_dialog.difficulty

        if rows is not None and columns is not None and difficulty:
            new_maze = generate_labyrinth(rows, columns, difficulty)  # Generate maze based on input
            self.generate_maze_csv(new_maze)  

    def solve_maze(self):

        # Ask for CSV file
        self.laberinth_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.maze = load_maze_from_csv(self.laberinth_file_path)

        if self.laberinth_file_path == "":
            return
            
        print(self.maze)

        if self.maze is None:
            messagebox.showerror("Error", "Seleccione un laberinto primero.")
            return
        if not isinstance(self.maze, list):
            messagebox.showerror("Error", "El archivo seleccionado no es un laberinto.")
            return

        # Get the algortihm from the list
        selected_algorithm = self.algorithm_selector.get_selected_algorithm()
        print(f"Selected Algorithm: {selected_algorithm}")

        result_handler = ResultHandler(selected_algorithm, self.laberinth_file_path)
        result_handler.start_timer_memory()
        
        # Run your maze solving algorithm
        # This should be a loop showing every step (perfect result) or the final step
        # ...

        result_handler.stop_timer_memory()

        result_text = result_handler.record_result()
        result_handler.save_result()

        result_label = Label(self.root, text=result_text)
        result_label.pack()
        messagebox.showinfo("Laberinto Cargado", "Laberinto resuelto :D")

        # Save the solved maze into a csv file
        # self.save_maze()

    def save_maze(self):

        if self.maze is None and self.completed_maze is False:
            messagebox.showerror("Error", "No hay resultados para guardar.")
            return
        self.generate_maze_csv(self.maze)  

    def generate_maze_csv(self, maze):
        
        file_path = filedialog.asksaveasfilename(filetypes=[("CSV Files", "*.csv")])

        if file_path == "":
            return

        if not file_path.endswith(".csv"):
            file_path += ".csv"
            
        save_maze_to_csv(file_path, maze)
        messagebox.showinfo("Laberinto Guardado", "Laberinto guardado con éxito!")