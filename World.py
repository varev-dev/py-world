import random

import Organism
import tkinter as tk
from tkinter import Text


class World:
    def __init__(self, width, height, turn):
        self.width = width
        self.height = height
        self.turn = turn
        self.human = None
        self.fields = [[0 for _ in range(width)] for _ in range(height)]
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

    def create_organisms(self, counter, classes):
        while counter != 0:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)

            if self.fields[y][x] != 0:
                continue

            counter -= 1
            selected = random.choice(classes)
            from Position import Position
            org = selected(self, Position(x, y))
            self.organisms.append(org)
            self.fields[y][x] = org

    def generate(self, animals_percent, plants_percent):
        fields = int(self.width * self.height)
        animals = int(fields * animals_percent)

        if animals > fields - 1:
            animals = fields - 1

        plants = fields * plants_percent

        if plants + animals > fields - 1:
            plants = fields - animals - 1

        import Animal
        import Plant
        from Position import Position

        av_animals = [Animal.Fox, Animal.Sheep, Animal.CyberSheep, Animal.Antelope, Animal.Turtle, Animal.Wolf]
        av_plants = [Plant.Grass, Plant.Sonchus, Plant.Guarana, Plant.Belladonna, Plant.Hogweed]

        self.human = Animal.Human(self, Position(int(self.width/2), int(self.height/2)))
        self.add_organism(self.human)
        self.create_organisms(animals, av_animals)
        self.create_organisms(plants, av_plants)

    def add_organism(self, organism):
        self.organisms.append(organism)
        self.fields[organism.position.y][organism.position.x] = organism

    def remove_organism(self, organism):
        self.fields[organism.position.y][organism.position.x] = 0
        self.organisms.remove(organism)

    def make_turn(self):
        self.organisms.sort(key=lambda organ: organ.initiative, reverse=True)
        org_copy = self.organisms.copy()
        self.turn += 1

        for org in org_copy:
            if org in self.organisms:
                org.action()

        if self.human not in self.organisms:
            self.human = None
