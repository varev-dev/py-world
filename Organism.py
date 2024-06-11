from __future__ import annotations

import random
import tkinter as tk
from tkinter import Canvas
from abc import ABC, abstractmethod
from Direction import Direction as Dire

from World import World
from Position import Position


class Organism:
    DELAY = 5

    def __init__(self, world: World, position: Position, power, initiative, move_size, color):
        self.world = world
        self.position = position
        self.power = power
        self.initiative = initiative
        self.move_size = move_size
        self.last_action = world.turn
        self.color = color

    def print(self, canvas: tk.Canvas):
        size_x = canvas.winfo_width() / self.world.width
        size_y = canvas.winfo_height() / self.world.height

        x0 = size_x * self.position.x
        y0 = size_y * self.position.y
        x1 = size_x * (self.position.x + 1)
        y1 = size_y * (self.position.y + 1)

        canvas.create_rectangle(x0, y0, x1, y1, fill=self.color)

    @staticmethod
    def is_every_direction_checked(checked):
        for direction in Dire:
            if not checked[direction.value]:
                return False

        return True

    def is_move_possible(self, direction: Dire):
        if direction == Dire.NORTH or direction == Dire.NORTHEAST or direction == Dire.NORTHWEST:
            if self.position.y - self.move_size < 0:
                return False
        elif direction == Dire.SOUTH or direction == Dire.SOUTHEAST or direction == Dire.SOUTHWEST:
            if self.position.y + self.move_size >= self.world.height:
                return False

        if direction == Dire.WEST or direction == Dire.NORTHWEST or direction == Dire.SOUTHWEST:
            if self.position.x - self.move_size < 0:
                return False
        elif direction == Dire.EAST or direction == Dire.NORTHEAST or direction == Dire.SOUTHEAST:
            if self.position.x + self.move_size >= self.world.width:
                return False

        return True

    def get_random_possible_direction(self):
        checked = [False] * len(Dire)

        while not self.is_every_direction_checked(checked):
            random_direction = random.choice(list(Dire))

            if checked[random_direction.value]:
                continue
            checked[random_direction.value] = True

            if not self.is_move_possible(random_direction):
                continue

            return random_direction

        return None

    def get_adjacent_empty_field(self):
        checked = [False] * len(Dire)

        while not self.is_every_direction_checked(checked):
            random_direction = random.choice(list(Dire))

            if checked[random_direction.value]:
                continue
            checked[random_direction.value] = True

            if not self.is_move_possible(random_direction):
                continue

            return self.position.updated_position(random_direction, self.world, self.move_size)

        return None

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, other: Organism):
        pass
