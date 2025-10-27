from events.events_abstract import Event


class CircleCollideWall(Event):
    WALL_UP = 0
    WALL_RIGHT = 1
    WALL_DOWN = 2
    WALL_LEFT = 3

    def __init__(self, wall):
        self.wall = wall


class CircleCollideCircle(Event):
    def __init__(self, first, second):
        self.first = first
        self.second = second
