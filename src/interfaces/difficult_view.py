from tkinter import ttk, Label, Toplevel, Entry, Button
from src.interfaces.components.window import DynamicWindowSize

class InputDialog:
    def __init__(self, parent):

        #self.window.title("Maze Solver Difficult Selector")
        #self.window.configure(bg="#F0F0F0")  

        self.dialog = Toplevel(parent)
        self.dialog.title("Maze Difficult Creator")
        self.dialog.geometry("300x250")  # Set the width and height of the window
        self.dialog.resizable(False, False)  # Disable window resizing

        self.center_dialog()
        
        Label(self.dialog, text="Número de filas:").pack(pady=5)
        self.rows_entry = Entry(self.dialog)
        self.rows_entry.pack(pady=5)
        self.rows_entry.config(validate="key", validatecommand=(self.rows_entry.register(self.validate_number), "%P"))
        self.rows_entry.insert(0, "5")
        
        Label(self.dialog, text="Número de columnas:").pack(pady=5)
        self.columns_entry = Entry(self.dialog)
        self.columns_entry.pack(pady=5)
        self.columns_entry.config(validate="key", validatecommand=(self.columns_entry.register(self.validate_number), "%P"))
        self.columns_entry.insert(0, "5")
        
        Label(self.dialog, text="Dificultad:").pack(pady=5)
        self.difficulty_combobox = ttk.Combobox(self.dialog, values=["easy", "normal", "difficult"])
        self.difficulty_combobox.set("Seleccione una dificultad")
        self.difficulty_combobox.pack(pady=5)
        self.difficulty_combobox.state(["readonly"])
        self.difficulty_combobox.current(1)
        
        self.submit_button = Button(self.dialog, text="Crear", command=self.submit)
        self.submit_button.pack(pady=10)
        
        self.rows = None
        self.columns = None
        self.difficulty = None
    

    def center_dialog(self):
        self.dialog.update_idletasks() 
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.dialog.geometry(f"+{x}+{y}") 

    def validate_number(self, value):
        if value == "":
            return False
        try:
            int(value)
            return True
        except ValueError:
            return False
        
    def submit(self):
        self.rows = int(self.rows_entry.get())
        self.columns = int(self.columns_entry.get())
        self.difficulty = self.difficulty_combobox.get()
        self.dialog.destroy()