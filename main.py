import tkinter as tk
from tkinter import Text

from Organism import Organism
from Animal import Animal
from Position import Position
from World import World


def next_turn(wrd: World, rt: tk.Tk, cnv: tk.Canvas, text: tk.Text):
    wrd.make_turn()
    wrd.print(cnv, text)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Py World")

    world = World(10, 10, 2)
    organism = Animal(world, Position(2, 2), 2, 2, 1, 'blue')
    world.add_organism(organism)

    # Configure grid weights for proper stretching
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # Set up the canvas
    canvas = tk.Canvas(root, width=800, height=800, bg="white")
    canvas.grid(row=0, column=0, rowspan=10, padx=10, pady=10)

    # Create a frame for the buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

    # Configure frame grid weights
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)

    # Set up the buttons inside the frame
    btn_new = tk.Button(button_frame, text="new game")
    btn_save = tk.Button(button_frame, text="save game")
    btn_load = tk.Button(button_frame, text="load game")
    btn_skill = tk.Button(button_frame, text="use skill")
    btn_next = tk.Button(button_frame, text="next round")

    # Set up the text area
    text_area = Text(root, height=45, width=45)
    text_area.grid(row=1, column=1, columnspan=3, rowspan=19, padx=10, pady=10, sticky="nsew")

    # Arrange the buttons in a grid within the frame
    btn_new.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    btn_save.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    btn_load.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    btn_skill.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    canvas.delete('all')
    btn_next.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    btn_next.config(command=lambda: next_turn(world, root, canvas, text_area))

    # Start the Tkinter event loop
    root.mainloop()
