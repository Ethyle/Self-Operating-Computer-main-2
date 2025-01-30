# gui.py
import tkinter as tk
from tkinter import *
import threading
from main import main

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatisation AI")
        self.root.geometry("400x100")
        self.root.resizable(False, False)

        # Center the window
        self.center_window(400, 100)

        # Create a text entry
        self.entry = Entry(root, width=50, font=("Arial", 14))
        self.entry.pack(pady=10)

        # Create a submit button
        self.submit_button = Button(root, text="Execute", command=self.submit_task, font=("Arial", 12))
        self.submit_button.pack()

    def center_window(self, width, height):
        """Centers the window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def submit_task(self):
        """Retrieves the entered task and runs the algorithm."""
        task_description = self.entry.get().strip()
        if task_description:
            print(f"Task submitted : {task_description}")
            self.root.withdraw()  # Hide window

            # Run the algorithm in a new thread
            threading.Thread(target=main, args=(task_description,), daemon=True).start()
        else:
            print("Please enter a valid task.")

def start_gui():
    """Initialises and starts the GUI."""
    root = Tk()
    app = TaskApp(root)
    root.mainloop()
