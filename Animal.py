import random

from Position import Position
from Organism import Organism
from World import World


class Animal(Organism):
    def __init__(self, world: World, position: Position, power=1, initiative=1, move_size=1, color='black'):
        super().__init__(world, position, power, initiative, move_size, color)

    def action(self):
        direction = super().get_random_possible_direction(isinstance(self, Fox))
        self.world.messages.append(self.__class__.__name__ + " on move")
        if direction is not None:
            pos = self.position.updated_position(direction, self.world, self.move_size)

            if self.world.fields[pos.y][pos.x] == 0:
                self.world.fields[self.position.y][self.position.x] = 0
                self.position.update(direction, self.world, self.move_size)
                self.world.fields[self.position.y][self.position.x] = self
            else:
                self.world.fields[pos.y][pos.x].collision(self)

    def collision(self, other: Organism):
        if type(self) is type(other):
            pos = self.get_adjacent_empty_field()
            if pos is None:
                return
            org = type(self)(self.world, pos)
            self.world.organisms.append(org)
            self.world.fields[pos.y][pos.x] = org
            self.world.messages.append(type(self).__name__ + " was born (x:" + str(pos.x) + "; y:" + str(pos.y) + ")")
            return

        message = ""

        self.world.fields[other.position.y][other.position.x] = 0
        if self.power >= other.power:
            message += type(self).__name__ + " killed " + type(other).__name__
            self.world.organisms.remove(other)
        else:
            message += type(other).__name__ + " killed " + type(self).__name__
            self.world.fields[self.position.y][self.position.x] = other
            other.position = self.position
            self.world.organisms.remove(self)
        self.world.messages.append(message)


class Fox(Animal):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 3, 7, 1, 'orange')


class Sheep(Animal):
    def __init__(self, world: World, position: Position, power=1, initiative=1, move_size=1, color='black'):
        super().__init__(world, position, 4, 4, 1, 'lightgray')


class Wolf(Animal):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 9, 5, 1, 'gray')


class Turtle(Animal):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 2, 1, 1, 'darkgreen')

    def collision(self, other: Organism):
        if other.power < 5:
            self.world.messages.append(self.__class__.__name__ + " reflects attack")
            return

        super().collision(other)


class Antelope(Animal):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 4, 4, 2, 'brown4')

    def collision(self, other: Organism):
        if random.random() < 0.5:
            pos = super().get_adjacent_empty_field()
            if pos is not None:
                self.world.fields[self.position.y][self.position.x] = other
                self.world.fields[pos.y][pos.x] = self
                self.world.messages.append(self.__class__.__name__ + " runs away from the fight")
                return

        super().collision(other)


class CyberSheep(Sheep):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 11, 4, 1, 'pink')

    def action(self):
        closest_org = None
        closest_dist = None
        for org in self.world.organisms:
            if type(org) is not Fox:
                continue

            dist = self.position.get_distance_between(org)

            if closest_org is None or dist < closest_dist:
                closest_org = org
                closest_dist = dist

        if closest_org is None:
            super().action()
            return

        pos = self.position.follow_position(closest_org, self.move_size)
        if self.world.fields[pos.y][pos.x] == 0:
            self.world.fields[self.position.y][self.position.x] = 0
            self.position = pos
            self.world.fields[self.position.y][self.position.x] = self
        else:
            self.world.fields[pos.y][pos.x].collision(self)
