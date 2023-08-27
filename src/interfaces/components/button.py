from tkinter import Button, LEFT

class StyledButton:
    def __init__(self, root, text, command, bg_color, fg_color):

        self.button = Button(
            root,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=("Helvetica", 11),
        )

        self.button.pack(side=LEFT, padx=10)