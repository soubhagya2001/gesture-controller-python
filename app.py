import tkinter as tk
from tkinter import Label, PhotoImage
from subprocess import Popen

class GameLauncher(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("AirPlay")
        self.pack(fill=tk.BOTH, expand=True)

       
        self.games_frame = tk.Frame(self, bg="grey")
        self.controller_frame = tk.Frame(self, bg="black")

        self.games_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.controller_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Add a separator line
        separator = tk.Frame(self, width=2, bg="black")
        separator.pack(side=tk.LEFT, fill=tk.Y)

        
        self.create_game_section()

        
        self.create_controller_section()

    def create_game_section(self):
        
        games_heading = tk.Label(self.games_frame, text="GAMES", font=("Helvetica", 16), bg="white")
        games_heading.pack(pady=10)

        # Game images and names
        games_info = [
            {"name": "Wolf Runner", "image_path": "./images/wolfGame.png", "command": "python ./pygame/fourth.py"},

        ]

        for info in games_info:
            image = PhotoImage(file=info["image_path"]).subsample(2, 2)  # Adjust subsample as needed
            # Resize the image to a specific size
            image = image.zoom(2)  # Adjust the zoom factor as needed
            image = image.subsample(2)
            button = tk.Button(self.games_frame, image=image, text=info["name"], compound=tk.TOP, command=lambda c=info["command"]: self.run_command(c))
            button.image = image
            button.pack(pady=10)

    def create_controller_section(self):
       
        controller_heading = tk.Label(self.controller_frame, text="CONTROLLER", font=("Helvetica", 16), bg="white")
        controller_heading.pack(pady=10)

        
        controller_info = [
            {"name": "Runner", "image_path": "./images/hand.png", "command": "python ./controller/dino.py"},
            {"name": "Steering", "image_path": "./images/steering.png", "command": "python ./controller/carController.py"},
            {"name": "Head Mouse", "image_path": "./images/head.png", "command": "python ./controller/head.py"},
            {"name": "Hand Mouse", "image_path": "./images/hand.png", "command": "python ./controller/handMouse1.py"},
        ]

        for info in controller_info:
            image = PhotoImage(file=info["image_path"]).subsample(2, 2)  # Adjust subsample as needed
            # Resize the image to a specific size
            image = image.zoom(2)  # Adjust the zoom factor as needed
            image = image.subsample(2)
            button = tk.Button(self.controller_frame, image=image, text=info["name"], compound=tk.TOP, command=lambda c=info["command"]: self.run_command(c))
            button.image = image
            button.pack(side=tk.LEFT, padx=10)  # Arrange buttons side by side with padding

        # Information about closing in the 4% area
        #info_label = Label(self.controller_frame, text="To close, press 'q' or 'esc'", font=("Helvetica", 10), bg="white")
        #info_label.pack(side=tk.BOTTOM, fill=tk.X, pady=20, padx=10)  # Place at the bottom with padding
        #info_label.pack(side=tk.BOTTOM, anchor=tk.SW, fill=tk.X, pady=20, padx=10)


    def run_command(self, command):
        Popen(command, shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(master=root)
    root.geometry("600x250")
    root.resizable(False,False)
    app.mainloop()
