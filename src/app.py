from src.convex_hull.convex_hull import ConvexHull
from src.point.point import Point
import random
import math

from src.animation import AlgorithmVisualization


def generate_random_set_of_points(number_of_points: int, min_x: int, max_x: int, min_y: int, max_y: int) -> list[Point]:
    set_of_points: list[Point] = []
    for _ in range(number_of_points):
        x: int
        y: int
        x, y = random.uniform(min_x, max_x)*random.uniform(min_x, max_x), random.uniform(min_y, max_y)*random.uniform(min_x, max_x)
        set_of_points.append(Point(int(math.sqrt(x)), int(math.sqrt(y))))

    return set_of_points


def run():
    FPS: int = 60
    SCREEN_MARGIN: int = 0
    WIDTH: int = 100
    HEIGHT: int = 100
    set_of_points = generate_random_set_of_points(
        146, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
    )

    """ alg_visualization = AlgorithmVisualization(WIDTH, HEIGHT, SCREEN_MARGIN, FPS)
    alg_visualization.animate_convex_hull("incremental_alg", set_of_points) """

    convex_hull = ConvexHull(set_of_points, alg='incremental_alg')
    convex_hull.plot(100)

if __name__ == "__main__":
    run()
