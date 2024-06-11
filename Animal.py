import random

from Position import Position
from Organism import Organism
from World import World


class Animal(Organism):
    def __init__(self, world: World, position: Position, power=1, initiative=1, move_size=1, color='black'):
        super().__init__(world, position, power, initiative, move_size, color)

    def action(self):
        direction = super().get_random_possible_direction(not isinstance(self, Fox))
        # self.world.messages.append(self.__class__.__name__ + " on move")
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
            if self in self.world.organisms:
                self.world.organisms.remove(self)
        self.world.messages.append(message)


class Fox(Animal):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 3, 7, 1, 'orange')


class Sheep(Animal):
    def __init__(self, world: World, position: Position, power=4, initiative=4, move_size=1, color='lightgray'):
        super().__init__(world, position, power, initiative, move_size, color)

    def collision(self, other: Organism):
        if isinstance(other, (CyberSheep, Sheep)):
            pos = self.get_adjacent_empty_field()
            if pos is None:
                return
            org = Sheep(self.world, pos)
            self.world.organisms.append(org)
            self.world.fields[pos.y][pos.x] = org
            self.world.messages.append(Sheep.__name__ + " was born (x:" + str(pos.x) + "; y:" + str(pos.y) + ")")
            return

        super().collision(other)


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
        from Plant import Hogweed

        for org in self.world.organisms:
            if type(org) is not Hogweed:
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


class Human(Animal):
    DELAY = 5

    def __init__(self, world: World, position: Position, delay=0):
        super().__init__(world, position, 5, 4, 1, 'black')
        self.direction = None
        self.delay = delay

    def action(self):
        self.delay = max(self.delay - 1, 0)
        if self.direction is None:
            return

        self.world.messages.append(self.__class__.__name__ + " on move")
        pos = self.position.updated_position(self.direction, self.world, self.move_size)

        if pos.x == self.position.x and pos.y == self.position.y:
            return

        if self.world.fields[pos.y][pos.x] == 0:
            self.world.fields[self.position.y][self.position.x] = 0
            self.position = pos
            self.world.fields[self.position.y][self.position.x] = self
        else:
            self.world.fields[pos.y][pos.x].collision(self)

    def collision(self, other: Organism):
        if type(other) is Human:
            self.world.fields[other.position.y][other.position.x] = 0
            return

        if self.delay > Human.DELAY and other.power > self.power:
            pos = super().get_adjacent_empty_field()
            self.world.messages.append(self.__class__.__name__ + " survived because of ability")

            if pos is None or pos is self.position:
                return

            self.world.fields[other.position.y][other.position.x] = 0
            self.world.fields[self.position.y][self.position.x] = other
            other.position = self.position
            self.world.fields[pos.y][pos.x] = self
            self.position = pos
            return
        else:
            super().collision(other)

    def update_direction(self, key):
        from Direction import Direction

        key_to_direction = {
            'a': Direction.WEST,
            'q': Direction.NORTHWEST,
            'w': Direction.NORTH,
            'e': Direction.NORTHEAST,
            'd': Direction.EAST,
            'c': Direction.SOUTHEAST,
            'x': Direction.SOUTH,
            'z': Direction.SOUTHWEST
        }

        if key in key_to_direction:
            self.direction = key_to_direction[key]
        else:
            self.direction = None

    def use_ability(self):
        if self.delay == 0:
            self.delay = Human.DELAY * 2
            self.world.messages.append("Used ability!")
        elif self.delay > Human.DELAY:
            self.world.messages.append("Ability is already active")
        else:
            self.world.messages.append("Available in " + str(self.delay) + " rounds")
