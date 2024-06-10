import Organism
import tkinter as tk
from tkinter import Text


class World:
    def __init__(self, width, height, turn):
        self.width = width
        self.height = height
        self.turn = turn
        self.fields = [[0 for _ in range(height)] for _ in range(width)]
        self.organisms = []
        self.messages = []

    def print(self, canvas: tk.Canvas, text_area: Text):
        text_area.delete('1.0', tk.END)
        for text in self.messages:
            text_area.insert(tk.END, str(text) + "\n")

        self.messages = []
        canvas.delete('all')
        for org in self.organisms:
            org.print(canvas)

    def add_organism(self, organism):
        self.organisms.append(organism)
        self.fields[organism.position.y][organism.position.x] = organism

    def remove_organism(self, organism):
        self.fields[organism.position.y][organism.position.x] = None
        self.organisms.remove(organism)

    def make_turn(self):
        org_copy = self.organisms.copy()

        for org in self.organisms:
            org.action()
