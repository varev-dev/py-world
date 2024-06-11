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
        text_area.insert(tk.END, "======== Current round " + str(self.turn) + " ========\n")

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
        fields = self.width * self.height
        animals = int(fields * animals_percent)

        if animals > fields - 1:
            animals = fields - 1

        plants = int(fields * plants_percent)

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

    def save(self, filename):
        import Animal
        with open(filename, 'w') as file:
            line = f"{self.turn} {self.width} {self.height}\n"
            file.write(line)
            for org in self.organisms:
                line = f"{org.__class__.__name__} {org.position.x} {org.position.y} {org.power}"
                if type(org) is Animal.Human:
                    line += f" {org.delay}"
                line += "\n"
                file.write(line)

    def load(self, filename):
        self.human = None
        self.organisms = []
        self.messages = []

        with open(filename, 'r') as file:
            data = file.readline().strip().split(' ')

            self.turn = int(data[0])
            self.width = int(data[1])
            self.height = int(data[2])
            self.fields = [[0 for _ in range(self.width)] for _ in range(self.height)]

            import Animal
            import Plant
            from Position import Position
            classes = [Animal.Fox, Animal.Sheep, Animal.CyberSheep, Animal.Antelope, Animal.Turtle, Animal.Wolf,
                       Animal.Human, Plant.Grass, Plant.Sonchus, Plant.Guarana, Plant.Belladonna, Plant.Hogweed]
            for line in file:
                data = line.strip().split(' ')
                for class_name in classes:
                    if data[0] == class_name.__name__:
                        pos = Position(int(data[1]), int(data[2]))
                        power = data[3]

                        org = class_name(self, pos, power)

                        if class_name is Animal.Human:
                            org.delay = int(data[4])
                            self.human = org

                        self.add_organism(org)

        self.organisms.sort(key=lambda organ: organ.initiative, reverse=True)
