import random

from Direction import Direction
from Organism import Organism
from Position import Position
from World import World


class Plant(Organism):
    def __init__(self, world: World, position: Position, power=1, color='black'):
        super().__init__(world, position, power, 0, 1, color)

    def action(self):
        if random.random() < 0.75:
            return

        pos = super().get_adjacent_empty_field()
        if pos is None:
            return

        org = type(self)(self.world, pos)
        self.world.fields[pos.y][pos.x] = org
        self.world.organisms.append(org)
        self.world.messages.append(type(self).__name__ + " has grown")

    def collision(self, other: Organism):
        self.world.fields[other.position.y][other.position.x] = 0
        self.world.organisms.remove(self)
        other.position = self.position
        self.world.fields[other.position.y][other.position.x] = other
        self.world.messages.append(type(other).__name__ + " ate " + type(self).__name__)


class Grass(Plant):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 0, 'lightgreen')


class Sonchus(Plant):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 0, 'yellow')

    def action(self):
        for i in range(0, 3):
            super().action()


class Guarana(Plant):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 0, 'firebrick1')

    def collision(self, other: Organism):
        other.power += 3
        super().collision(other)


class Belladonna(Plant):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 99, 'blue')

    def collision(self, other: Organism):
        self.world.fields[other.position.y][other.position.x] = 0
        self.world.organisms.remove(other)
        self.world.messages.append(type(other).__name__ + " ate " + type(self).__name__ + " and died")


class Hogweed(Plant):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 10, 'orchid')

    def action(self):
        from Animal import CyberSheep

        for direction in Direction:
            pos = self.position.updated_position(direction, self.world, self.move_size)

            if pos.x == self.position.x and pos.y == self.position.y:
                continue

            org = self.world.fields[pos.y][pos.x]

            if org == 0 or isinstance(org, (CyberSheep, Hogweed)):
                continue

            self.world.messages.append(self.__class__.__name__ + " killed " + org.__class__.__name__)
            self.world.fields[pos.y][pos.x] = 0
            self.world.organisms.remove(org)

    def collision(self, other: Organism):
        self.world.messages.append(self.__class__.__name__ + " killed " + other.__class__.__name__)
        self.world.fields[other.position.y][other.position.x] = 0
