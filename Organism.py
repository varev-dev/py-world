from __future__ import annotations

import random
import tkinter as tk
from tkinter import Canvas
from abc import ABC, abstractmethod
from Direction import Direction as Dire

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

    def is_every_direction_checked(self, checked: []):
        for direction in Dire:
            if not checked[direction]:
                return False

        return True

    def is_move_possible(self, direction: Dire):
        if direction == Dire.NORTH or direction == Dire.NORTHEAST or direction == Dire.NORTHWEST:
            if self.position.y - self.move_size < 0:
                return False
        if direction == Dire.SOUTH or direction == Dire.SOUTHEAST or direction == Dire.SOUTHWEST:
            if self.position.y + self.move_size >= self.world.height:
                return False

        if direction == Dire.EAST or direction == Dire.NORTHEAST or direction == Dire.SOUTHEAST:
            if self.position.x - self.move_size < 0:
                return False
        if direction == Dire.WEST or direction == Dire.NORTHWEST or direction == Dire.SOUTHWEST:
            if self.position.x + self.move_size >= self.world.width:
                return False

    def get_random_possible_direction(self):
        checked = []

        while self.is_every_direction_checked(checked):
            random_direction = random.choice(list(Dire))

            if checked[random_direction]:
                continue

            if not self.is_move_possible(random_direction):
                continue

            return random_direction

        return None

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, other: Organism):
        pass
