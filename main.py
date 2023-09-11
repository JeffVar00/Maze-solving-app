import tkinter as tk
from src.interfaces.main_view import MazeSolverApp

def main():
    root = tk.Tk()
    app = MazeSolverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 

