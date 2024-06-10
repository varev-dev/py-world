from Position import Position
from Organism import Organism
from World import World


class Animal(Organism):
    def __init__(self, world: World, position: Position, power, initiative, move_size, color):
        super().__init__(world, position, power, initiative, move_size, color)

    def action(self):
        direction = super().get_random_possible_direction()

        if direction is not None:
            self.world.fields[self.position.y][self.position.x] = None
            self.position.update(direction, self.world, self.move_size)
            self.world.messages.append(str(self.position.x) + " " + str(self.position.y))
            self.world.fields[self.position.y][self.position.x] = self

    def collision(self, other: Organism):
        if self.power >= other.power:
            self.world.organisms.remove(other)
        else:
            self.world.organisms.remove(self)
