from rendering import *


class PygameClass:
    def __init__(self, physics_engine, statistic):
        self.physics_engine = physics_engine
        self.statistic = statistic
        self._init_pygame()

    def _init_pygame(self):
        pygame.init()
        self._surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self._clock = pygame.time.Clock()
        self.renderer = Renderer(self._surface, self.physics_engine)
        self.running = True

    def start(self):
        while self.running:
            self._tick()

    def _tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self._render()
        pygame.display.flip()
        self.statistic.rendered_frames += 1
        self._clock.tick(FPS)

    def _render(self):
        self._surface.fill((0, 0, 0))
        self.renderer.render()