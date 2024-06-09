import Position
import Organism
import World


class Animal(Organism.Organism):
    def __init__(self, world: World.World, position: Position.Position, power, initiative, move_size, color):
        super().__init__(world, position, power, initiative, move_size, color)

    def action(self):
        pass

    def collision(self, other: Organism):
        if self.power >= other.power:
            self.world.organisms.remove(other)
        else:
            self.world.organisms.remove(self)
