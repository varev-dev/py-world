from World import World
from Direction import Direction


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, dire: Direction, world: World, move_size):
        if dire == Direction.NORTH or dire == Direction.NORTHWEST or dire == Direction.NORTHEAST:
            if self.y - move_size >= 0:
                self.y -= move_size
        elif dire == Direction.SOUTH or dire == Direction.SOUTHWEST or dire == Direction.SOUTHEAST:
            if self.y + move_size < world.height:
                self.y += move_size

        if dire == Direction.WEST or dire == Direction.NORTHWEST or dire == Direction.SOUTHWEST:
            if self.x - move_size >= 0:
                self.x -= move_size
        elif dire == Direction.EAST or dire == Direction.NORTHEAST or dire == Direction.SOUTHEAST:
            if self.x + move_size < world.width:
                self.x += move_size
