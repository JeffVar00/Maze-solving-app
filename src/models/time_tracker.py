from tkinter import messagebox, Label
import tracemalloc
import time
import os

class ResultHandler:
    def __init__(self):

        self.memory_before = None
        self.start_time = None
        self.end_time = None
        self.memory_used = None
        self.elapsed_time = None


    def start_timer_memory(self):
        self.memory_before = tracemalloc.get_traced_memory()[0]
        self.start_time = time.time()

    def stop_timer_memory(self):
        self.end_time = time.time()
        tracemalloc.stop()
        self.memory_used = tracemalloc.get_traced_memory()[0] - self.memory_before
        self.elapsed_time = self.end_time - self.start_time

    def record_result(self):
        return f"Tiempo: {self.elapsed_time:.6f} segundos\t Memoria usada: {self.memory_used / 1024:.2f} KB"

    def save_result(self, algorithm_name, file_path, maze):

        # get maze rows and columns
        rows = len(maze)
        columns = len(maze[0])

        results_folder = "data/results"
        os.makedirs(results_folder, exist_ok=True)

        # Get the laberinth name from filepath
        laberinth_name = file_path.split("/")[-1].split(".")[0]

        # Save the results to a text file
        file_name = f"{results_folder}/{algorithm_name.lower().replace(' ', '_')}_{laberinth_name}.txt"
        with open(file_name, 'w') as file:
            file.write(f"Tamaño del Laberinto: \n")
            file.write(f"Filas: {rows}\n")
            file.write(f"Columnas: {columns}\n\n")
            file.write(f"Algoritmo: {algorithm_name}\n")
            file.write(f"Tiempo: {self.elapsed_time:.6f} segundos\n")
            file.write(f"Memoria usada: {self.memory_used / 1024:.2f} KB\n")
            

        