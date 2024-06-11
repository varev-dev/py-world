import tkinter as tk
from tkinter import simpledialog, Text

from Organism import Organism
from Plant import *
from Animal import *
from Position import Position
from World import World


class Game:
    def __init__(self):
        self.world = None
        self.root = tk.Tk()
        self.root.title("Py World")
        self.text = Text(self.root, height=45, width=45)
        self.canvas = tk.Canvas(self.root, width=800, height=800, bg="white")
        self.button_frame = tk.Frame(self.root)
        self.btn_next = None
        self.btn_save = None
        self.btn_skill = None
        self.btn_load = None
        self.btn_new = None

    def setup(self):
        # Configure grid weights for proper stretching
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.canvas.grid(row=0, column=0, rowspan=10, padx=10, pady=10)
        self.button_frame.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

        # Configure frame grid weights
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        # Set up the buttons inside the frame
        self.btn_new = tk.Button(self.button_frame, text="new game", command=self.create_new_world)
        self.btn_save = tk.Button(self.button_frame, text="save game")
        self.btn_load = tk.Button(self.button_frame, text="load game")
        self.btn_skill = tk.Button(self.button_frame, text="use skill", command=self.skill_activate)
        self.btn_next = tk.Button(self.button_frame, text="next round", command=lambda: self.next_turn())

        # Set up the text area
        self.text.grid(row=1, column=1, columnspan=3, rowspan=19, padx=10, pady=10, sticky="nsew")

        # Arrange the buttons in a grid within the frame
        self.btn_new.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.btn_save.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.btn_load.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        self.btn_skill.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.btn_next.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.canvas.focus_set()
        self.root.bind('<Key>', self.read_pressed)

    def run(self):
        self.canvas.focus_set()
        # Start the Tkinter event loop
        self.root.mainloop()

    def skill_activate(self):
        if self.world is None or self.world.human is None:
            return
        self.world.human.use_ability()

    def read_pressed(self, event):
        key = event.char.lower()
        if self.world is None or self.world.human is None:
            return

        if key in ('q', 'w', 'e', 'a', 'd', 'z', 'x', 'c'):
            self.world.human.update_direction(key)
            self.next_turn()

    def next_turn(self):
        if self.world is None:
            return
        self.world.make_turn()
        self.world.print(self.canvas, self.text)
        self.canvas.focus_set()

    def create_new_world(self):
        width = simpledialog.askinteger("Width", "Enter the width of the world:", parent=self.root)
        height = simpledialog.askinteger("Height", "Enter the height of the world:", parent=self.root)

        plants = simpledialog.askfloat("Plant rate", "Enter in range 0-1:", parent=self.root, minvalue=0, maxvalue=1)
        animals = simpledialog.askfloat("Animal rate", "Enter in range 0-1:", parent=self.root, minvalue=0, maxvalue=1)

        if width is None or height is None or plants is None or animals is None:
            return None

        self.world = World(width, height, 0)
        self.world.generate(float(animals), float(plants))
        self.canvas.delete('all')
        self.text.delete('1.0', tk.END)
        self.world.print(self.canvas, self.text)


if __name__ == '__main__':
    game = Game()
    game.setup()
    game.run()
