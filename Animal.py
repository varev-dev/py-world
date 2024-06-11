from Position import Position
from Organism import Organism
from World import World


class Animal(Organism):
    def __init__(self, world: World, position: Position, power=1, initiative=1, move_size=1, color='black'):
        super().__init__(world, position, power, initiative, move_size, color)

    def action(self):
        direction = super().get_random_possible_direction()

        if direction is not None:
            pos = self.position.updated_position(direction, self.world, self.move_size)

            if self.world.fields[pos.y][pos.x] == 0:
                self.world.fields[self.position.y][self.position.x] = 0
                self.position.update(direction, self.world, self.move_size)
                self.world.messages.append(str(self.position.x) + " " + str(self.position.y))
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
            return

        if self.power >= other.power:
            self.world.organisms.remove(other)
        else:
            self.world.organisms.remove(self)


class Sheep(Animal):
    def __init__(self, world: World, position: Position):
        super().__init__(world, position, 4, 4, 1, 'lightgray')
