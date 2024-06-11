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

    def updated_position(self, dire: Direction, world: World, move_size):
        position = Position(0, 0)

        if dire == Direction.NORTH or dire == Direction.NORTHWEST or dire == Direction.NORTHEAST:
            position.y = self.y - move_size if self.y - move_size >= 0 else 0
        elif dire == Direction.SOUTH or dire == Direction.SOUTHWEST or dire == Direction.SOUTHEAST:
            position.y = self.y + move_size if self.y + move_size < world.height else world.height - 1

        if dire == Direction.WEST or dire == Direction.NORTHWEST or dire == Direction.SOUTHWEST:
            position.x = self.x - move_size if self.x - move_size >= 0 else 0
        elif dire == Direction.EAST or dire == Direction.NORTHEAST or dire == Direction.SOUTHEAST:
            position.x = self.x + move_size if self.x + move_size < world.width else world.width - 1

        return position

    def get_distance_between(self, compare):
        dist_x = abs(self.x - compare.position.x)
        dist_y = abs(self.y - compare.position.y)

        return min(dist_x, dist_y)

    def follow_position(self, org, move_size):
        if org.position.x > self.x and org.position.y > self.y:
            return Position(min(self.x + move_size, org.world.width - 1), min(self.y + move_size, org.world.height - 1))
        elif org.position.x > self.x and org.position.y < self.y:
            return Position(min(self.x + move_size, org.world.width - 1), max(self.y - move_size, 0))
        elif org.position.x < self.x and org.position.y < self.y:
            return Position(max(self.x - move_size, 0), max(self.y - move_size, 0))
        elif org.position.x < self.x and org.position.y > self.y:
            return Position(max(self.x - move_size, 0), min(self.y + move_size, org.world.height - 1))
        elif org.position.x < self.x:
            return Position(max(self.x - move_size, 0), self.y)
        elif org.position.x > self.x:
            return Position(min(self.x + move_size, org.world.width - 1), self.y)
        elif org.position.y < self.y:
            return Position(self.x, min(self.y - move_size, org.world.height - 1))
        elif org.position.y > self.y:
            return Position(self.x, max(self.y - move_size, 0))
        else:
            return self
