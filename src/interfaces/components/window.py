class DynamicWindowSize:
    def __init__(self, root, width_ratio=0.6, height_ratio=0.6):
        self.root = root
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        initial_width = int(screen_width * self.width_ratio)
        initial_height = int(screen_height * self.height_ratio)

        x_position = (screen_width - initial_width) // 2
        y_position = (screen_height - initial_height) // 2

        self.root.geometry(f"{initial_width}x{initial_height}+{x_position}+{y_position}")