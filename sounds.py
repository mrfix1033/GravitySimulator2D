import pygame


class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.wall_collision = pygame.mixer.Sound("wall_collision.mp3")
        self.body_collision = pygame.mixer.Sound("body_collision.mp3")
