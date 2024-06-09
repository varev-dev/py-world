from __future__ import annotations

import tkinter as tk
from tkinter import Canvas
from abc import ABC, abstractmethod

import World
import Position


class Organism:
    DELAY = 5

    def __init__(self, world: World.World, position: Position.Position, power, initiative, move_size, color):
        self.world = world
        self.position = position
        self.power = power
        self.initiative = initiative
        self.move_size = move_size
        self.last_action = world.turn
        self.color = color

    def print(self, canvas: tk.Canvas):
        size_x = self.world.width / canvas.winfo_width()
        size_y = self.world.height / canvas.winfo_height()

        x0 = size_x * self.position.x
        y0 = size_y * self.position.y
        x1 = size_x * (self.position.x + 1)
        y1 = size_x * (self.position.x + 1)

        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color)

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, other: Organism):
        pass
