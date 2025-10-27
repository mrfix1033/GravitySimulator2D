from threading import Thread

from events.events_physics import *
from events_handler import EventsHandler
from physics import PhysicsEngine, get_physics_handler_target
from pygame_class import PygameClass
from sounds import Sounds


class Game:
    def __init__(self):
        from statistic import Statistic

        self.events_handler = EventsHandler()
        self.register_events()
        self.add_listeners()

        self.physics_engine = PhysicsEngine(self.events_handler)
        self.sounds = Sounds()
        self.statistic = Statistic(self)
        self.pygame_class = PygameClass(self.physics_engine, self.statistic)

        self.running = True

    def register_events(self):
        self.events_handler.register(CircleCollideWall)
        self.events_handler.register(CircleCollideCircle)

    def add_listeners(self):
        self.events_handler.add_listener(CircleCollideWall, lambda _: self.sounds.wall_collision.play())
        self.events_handler.add_listener(CircleCollideCircle, lambda _: self.sounds.body_collision.play())

    def start(self):
        from statistic import get_statistic_print_target
        Thread(target=get_physics_handler_target(self.physics_engine, lambda: self.running)).start()
        Thread(target=get_statistic_print_target(lambda: self.statistic, lambda: self.running)).start()
        self.pygame_class.start()
        self.running = False


if __name__ == "__main__":
    game = Game()
    game.start()
