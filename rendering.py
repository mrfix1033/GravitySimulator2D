import numpy as np
import pygame

WIDTH, HEIGHT, FPS = 960, 540, 144


class Renderer:
    def __init__(self, surface, physics_engine):
        self.surface = surface
        self.physics_engine = physics_engine
        self.font = pygame.font.SysFont("Calibri", 14)

    def render(self):
        for body in self.physics_engine.bodies:
            pygame.draw.line(self.surface, (165, 0, 0), body.coords, body.coords + body.vel)
            self._render_text(body)
            self.render_circle(body)

    def _render_text(self, body):
        Ek = round(np.sqrt(sum(x ** 2 for x in body.vel)) * body.mass, 1)
        Ek_text = self.font.render(str(Ek), False, (165, 165, 165))
        Ek_coords = body.coords.copy()
        Ek_coords[0] -= np.asarray(Ek_text.get_width()) / 2
        Ek_coords[1] -= body.radius * 1.2 + Ek_text.get_height()
        self.surface.blit(Ek_text, Ek_coords)

    def render_circle(self, circle):
        pygame.draw.circle(self.surface, (255, 255, 255), circle.coords, circle.radius)
