from tkinter import filedialog, messagebox, Label, Frame, Canvas, CENTER

import os
import subprocess

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

        # Variables
        self.completed_maze = False
        self.maze = None
        self.laberinth_file_path = None

        # Configuration of the main window
        self.root.title("Maze Solver Application")
        self.root.config(bg="white")

        window_size_config = DynamicWindowSize(root)
        window_size_config.center_window()

        # Algorithm List
        algorithms = ["Algoritmo 1", "Algoritmo 2", "Algoritmo 3"]
        default_algorithm = algorithms[0]
        self.algorithm_selector = AlgorithmSelector(self.root, algorithms, default_algorithm)
        
        # Head Buttons
        buttons_frame = Frame(root, bg="white")
        buttons_frame.pack(pady=10)

        StyledButton(buttons_frame, "Generar nuevo Laberinto", self.create_maze, "#3498DB", "white")
        StyledButton(buttons_frame, "Resolver Laberinto", self.solve_maze, "#E74C3C", "white")

        # Show the Maze in the Solving Area
        canvas_frame = Frame(root)
        canvas_frame.pack(expand=True, fill="both")

        # Create the canvas and place it in the center of the frame
        self.maze_canvas = Canvas(canvas_frame, bg="white")
        self.maze_canvas.pack(expand=True, fill="both")

        # Results
        self.results_label = Label(self.root, bg="white")
        self.results_label.pack()

        # Bottom Buttons
        save_frame = Frame(root, bg="white")
        save_frame.pack(pady=10)

        StyledButton(save_frame, "Guardar Laberinto", self.save_maze, "#2ECC71", "white")

        # Options frame
        options_frame = Frame(root, bg="white")
        options_frame.pack(pady=10)

        StyledButton(options_frame, "Limpiar Laberinto", self.clean_maze, "#E74C3C", "white")
        StyledButton(options_frame, "Resultados", self.open_results_folder, "#F39C12", "white")

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

        if self.maze is None:
            messagebox.showerror("Error", "Seleccione un laberinto primero.")
            return
        print(self.maze)

        if not isinstance(self.maze, list):
            messagebox.showerror("Error", "El archivo seleccionado no es un laberinto.")
            return

        # Get the algortihm from the list
        selected_algorithm = self.algorithm_selector.get_selected_algorithm()
        print(f"Selected Algorithm: {selected_algorithm}")

        result_handler = ResultHandler()
        result_handler.start_timer_memory()
        
        # Run the maze solving algorithm selected
        # This should be a loop showing every step (updated the maze and call self.update_maze_display()) (perfect result) or the final step (in the end updated the maze with the same method)
        # ...
        self.update_maze_display()

        result_handler.stop_timer_memory()

        result_text = result_handler.record_result()
        self.results_label.config(text=result_text)
        result_handler.save_result(selected_algorithm, self.laberinth_file_path, self.maze)
        
        messagebox.showinfo("Laberinto Cargado", "Laberinto resuelto :D")

        # Save the solved maze into a csv file
        # self.save_maze()

    def save_maze(self):

        ## ver que hacer si guardar apenas termina o dar la opcion para guardar el laberinto, los resultados si se guardan automaticamente

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

    def update_maze_display(self):
        
        self.color_map = {
            0: "white",
            1: "black",
            2: "green",
            3: "red",
            4: "yellow",
            5: "blue"
        }

        self.maze_canvas.delete("all")  # Clear the canvas

        if self.maze:

            if 50 <= len(self.maze) < 75:
                cell_size = 5
            elif 75 <= len(self.maze) <= 150:
                cell_size = 3
            elif len(self.maze) > 150:
                cell_size = 2
            else:
                cell_size = 20
            
            canvas_width = self.maze_canvas.winfo_width()  
            canvas_height = self.maze_canvas.winfo_height()  

            rows = len(self.maze)
            cols = len(self.maze[0])

            maze_width = cols * cell_size
            maze_height = rows * cell_size

            # Center the maze on the screen
            x_offset = (canvas_width - maze_width) / 2
            y_offset = (canvas_height - maze_height) / 2

            for row in range(rows):
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
        self.update_maze_display()
        self.results_label.config(text="")

    def open_results_folder(self):
        results_folder = os.path.abspath("data/results")
        
        if os.path.exists(results_folder):
            subprocess.Popen(['explorer', results_folder])
        else:
            messagebox.showinfo("Carpeta de Resultados", "La carpeta de resultados no existe.")