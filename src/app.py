# import random

# from src.animation import AlgorithmVisualization
from src.line_sweep.line_sweep import LineSweep
from src.point import Point
from src.segment import Segment


# def generate_random_set_of_points(number_of_points: int, min_x: int, max_x: int, min_y: int, max_y: int) -> list[Point]:
#     set_of_points: list[Point] = []
#     for _ in range(number_of_points):
#         x: int
#         y: int
#         x, y = random.randint(min_x, max_x)*random.randint(min_x, max_x), random.randint(min_y, max_y)*random.randint(min_x, max_x)
#         set_of_points.append(Point(x/max_x, y/max_y))
#
#     return set_of_points


def run() -> None:
    # FPS: int = 60
    # SCREEN_MARGIN: int = 100
    # WIDTH: int = 600
    # HEIGHT: int = 600
    # set_of_points = generate_random_set_of_points(
    #     25, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
    # )
    #
    # alg_visualization = AlgorithmVisualization(WIDTH, HEIGHT, SCREEN_MARGIN, FPS)
    # alg_visualization.animate_convex_hull("gift_wrapping", set_of_points)
    x: list[Segment] = [
        Segment(Point(1, 1), Point(4, 4)),
        Segment(Point(2, 3), Point(3, 2)),
    ]
    L: LineSweep = LineSweep()
    y: bool = L.any_segments_intersect(x)
    print(y)


if __name__ == "__main__":
    run()
