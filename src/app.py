from src.convex_hull.convex_hull import ConvexHull
from src.point.point import Point
import random
import math
import time

from src.animation import AlgorithmVisualization


def generate_random_set_of_points(number_of_points: int, min_x: int, max_x: int, min_y: int, max_y: int) -> list[Point]:
    set_of_points: list[Point] = []
    for _ in range(number_of_points):
        x: int
        y: int
        x, y = random.uniform(min_x, max_x)*random.uniform(min_x, max_x)*random.uniform(min_x, max_x), random.uniform(min_y, max_y)*random.uniform(min_y, max_y)*random.uniform(min_y, max_y)
        set_of_points.append(Point(math.sqrt(x), math.sqrt(y)))

    return set_of_points


def run():
    FPS: int = 60
    SCREEN_MARGIN: int = 0
    WIDTH: int = 600
    HEIGHT: int = 600
    number_of_points = 145
    set_of_points = generate_random_set_of_points(
        number_of_points, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
    )

    """time_dict = {"graham_scan": 0, "gift_wrapping": 0, "incremental": 0}
    for _ in range(100):
        set_of_points = generate_random_set_of_points(
        number_of_points, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
    )
        a1 = time.time()
        convex_hull = ConvexHull(set_of_points, alg='graham_scan')
        a2 = time.time()
        time_dict["graham_scan"] += a2 - a1
      
    for _ in range(100):
        set_of_points = generate_random_set_of_points(
        number_of_points, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
    )
        a1 = time.time()
        convex_hull = ConvexHull(set_of_points, alg='gift_wrapping')
        a2 = time.time()
        time_dict["gift_wrapping"] += a2 - a1
    for _ in range(100):
        set_of_points = generate_random_set_of_points(
        number_of_points, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
    )
        a1 = time.time()
        convex_hull = ConvexHull(set_of_points, alg='incremental')
        a2 = time.time()
        time_dict["incremental"] += a2 - a1
    for e in time_dict.keys():
        time_dict[e]/=100
    print(time_dict) """
   

    convex_hull = ConvexHull(set_of_points, alg='incremental')
    convex_hull.plot(100)
  


if __name__ == "__main__":
    run()
