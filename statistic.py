import time
import typing


class Statistic:
    from main import Game
    def __init__(self, game: Game):
        self.game = game
        self.rendered_frames = 0  # todo deque (time of rendered frame)
        self.start_time = time.time_ns() / 1e9


def get_statistic_print_target(get_statistic: typing.Callable[[], Statistic], running: typing.Callable[[], bool]):
    def decorated():
        while running():
            stat = get_statistic()
            print(f"\rBody count: {len(stat.game.physics_engine.bodies)}\t"
                  f"FPS: {round(stat.rendered_frames / (time.time_ns() / 1e9 - stat.start_time), 1)}", end='')
            time.sleep(0.2)

    return decorated
