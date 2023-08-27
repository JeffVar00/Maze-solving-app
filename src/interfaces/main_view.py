
from tkinter import filedialog, messagebox, Label, Frame

from src.interfaces.components.button import StyledButton
from src.interfaces.components.window import DynamicWindowSize
from src.interfaces.components.list import AlgorithmSelector

from utils.csv_modules import load_maze_from_csv

class MazeSolverApp:

    def __init__(self, root):

        self.root = root

        # Configuration of the main window
        self.root.title("Maze Solver App")
        self.root.configure(bg="#F0F0F0")  

        window_size_config = DynamicWindowSize(root)
        window_size_config.center_window()

        # Algorithm List
        algorithms = ["Algoritmo 1", "Algoritmo 2", "Algoritmo 3"]
        default_algorithm = algorithms[0]
        self.algorithm_selector = AlgorithmSelector(root, algorithms, default_algorithm)
        
        # Buttons
        buttons_frame = Frame(root)
        buttons_frame.pack(pady=10)

        StyledButton(buttons_frame, "Cargar Laberinto", self.load_maze, "#3498DB", "white")
        StyledButton(buttons_frame, "Resolver Laberinto", self.solve_maze, "#E74C3C", "white")

        # Maze Solving Area
        maze_label = Label(root, text="Maze Area")
        maze_label.pack(pady=10)  

        self.maze = None

    def load_maze(self):

        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.maze = load_maze_from_csv(file_path)
        messagebox.showinfo("Laberinto Cargado", "Laberinto cargado con éxito!")

    def solve_maze(self):

        selected_algorithm = self.algorithm_selector.get_selected_algorithm()
        print(f"Selected Algorithm: {selected_algorithm}")

        if self.maze is None:
            messagebox.showerror("Error", "Carga un laberinto primero.")
            return

        # Lógica para resolver el laberinto usando el algoritmo de búsqueda en profundidad (DFS)
        # Implementa el algoritmo aquí y obtén la lista de tuplas que representa el camino

        # Mostrar el resultado en una matriz en la interfaz gráfica
        # Actualiza la interfaz gráfica con el resultado