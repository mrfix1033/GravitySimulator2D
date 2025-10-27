import abc
import math
import time
import typing
from random import randint, random

import numpy as np

from events.events_physics import CircleCollideWall, CircleCollideCircle
from rendering import WIDTH, HEIGHT

MASS_MULTIPLIER = 0.5
radius_to_mass = lambda r: MASS_MULTIPLIER * r ** 2

min_vel = 10  # pixels per second
max_vel = 100
diff_vel = max_vel - min_vel
SIGNS = (-1, 1)
number_of_bodies = 7


class Body(abc.ABC):
    def __init__(self, coords=None, vel=None, mass=None):
        self.coords = np.zeros(2) if coords is None else coords
        self.vel = np.zeros(2) if vel is None else vel
        self.mass = 1.0 if mass is None else mass

    # def __getattribute__(first, item):
    #     if item == "mass":
    #         return super().__getattribute__("mass") * MASS_MULTIPLIER
    #     return super().__getattribute__(item)


class Circle(Body):
    def __init__(self, radius, coords=None, vel=None, mass=None):
        if mass is None:
            mass = radius_to_mass(radius)
        super().__init__(coords, vel, mass)
        self.radius = radius


class PhysicsEngine:
    def __init__(self, events_handler):
        self.bodies = set()
        self.events_handler = events_handler
        for i in range(number_of_bodies):
            self._add_circle()

    def _add_circle(self):
        radius = randint(5, 15)
        coords = np.asarray((random() * WIDTH, random() * HEIGHT))
        magnitudes = np.random.uniform(min_vel, max_vel, 2)
        signs = np.random.choice(SIGNS, 2)
        vel = magnitudes * signs
        self.bodies.add(Circle(radius, coords, vel))

    def tick(self, passed_time_s):
        for body in self.bodies:
            collided_wall = check_walls_collide(body)  # you can add an "if" and some action in case of a collision with the wall
            if collided_wall:
                self.events_handler.call(CircleCollideWall(collided_wall))
            for other_body in self.bodies:  # bodies-collision, you can comment on this cycle to remove collisions between the bodies
                if other_body is body:
                    continue
                dist = math.dist(body.coords, other_body.coords)
                fug = body.mass * other_body.mass / dist ** 2  # force of universal gravity
                n = (other_body.coords - body.coords) / dist  # единичный вектор нормали центров
                add_vel = n * fug / body.mass * passed_time_s  # тело притягивается к другому по нормали центров
                body.vel += add_vel
                # body.vel += ((other_body.coords - body.coords) / body.mass /
                #              math.dist(body.coords, other_body.coords) ** 2)  # body-gravity
                if check_body_collide(body, other_body):  # you can add an "if" and some action in case of a collision
                    self.events_handler.call(CircleCollideCircle(body, other_body))
                    #     n = other_body.coords - body.coords
                    # n /= np.diag(n)

        for body in self.bodies:
            body.coords += body.vel * passed_time_s
            # body.vel[1] += 0.1  # down-gravity


def check_walls_collide(first) -> int:
    was_collision = 0
    if first.coords[0] - first.radius <= 0 and first.vel[0] < 0:
        first.vel[0] *= -1
        was_collision = CircleCollideWall.WALL_LEFT
    if first.coords[1] - first.radius <= 0 and first.vel[1] < 0:
        first.vel[1] *= -1
        was_collision = CircleCollideWall.WALL_UP
    if first.coords[0] + first.radius > WIDTH and first.vel[0] > 0:
        first.vel[0] *= -1
        was_collision = CircleCollideWall.WALL_RIGHT
    if first.coords[1] + first.radius > HEIGHT and first.vel[1] > 0:
        first.vel[1] *= -1
        was_collision = CircleCollideWall.WALL_DOWN
    return was_collision


def check_body_collide(self, body) -> bool:
    return body.radius + self.radius > math.dist(self.coords, body.coords)


def get_physics_handler_target(physics_engine, running: typing.Callable[[], bool]):
    def decorated():
        prev_time = time.time()
        while running():
            time.sleep(0.001)
            now = time.time()
            passed_time_s = now - prev_time
            prev_time = now
            physics_engine.tick(passed_time_s)
    return decorated