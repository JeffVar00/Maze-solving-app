from tkinter import Label, OptionMenu, StringVar, Label, ttk

class AlgorithmSelector:
    def __init__(self, root, algorithms, default_algorithm):
        self.algorithms = algorithms
        self.selected_algorithm = StringVar(value=default_algorithm)

        self.label = Label(root, text="Seleccione un algoritmo:")
        self.label.pack()

        style = ttk.Style()
        style.theme_create("custom_style", parent="alt", settings={
            "TCombobox": {
                "configure": {
                    "fieldbackground": "#F0F0F0",
                    "background": "white",
                    "foreground": "black",
                    "padding": 5,
                    "font": ("Helvetica", 14),
                    "arrowcolor": "black",
                    "arrowpadding": 10,
                    "selectbackground": "#F0F0F0", 
                    "selectforeground": "black",
                },
            }
        })
        style.theme_use("custom_style")

        self.menu = ttk.Combobox(
            root,
            textvariable=self.selected_algorithm,
            values=algorithms,
            state="readonly",
        )

        self.menu.pack()

    def get_selected_algorithm(self):
        return self.selected_algorithm.get()