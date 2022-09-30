import random

from pygame_animation import AlgorithmVisualization
from src.point.point import Point


def generate_random_set_of_points(number_of_points, min_x, max_x, min_y, max_y):
    set_of_points: list[Point] = []
    for _ in range(number_of_points):
        x: int
        y: int
        x, y = random.randint(min_x, max_x), random.randint(min_y, max_y)
        set_of_points.append(Point(x, y))

    return set_of_points


def main():
    FPS: int = 60
    SCREEN_MARGIN: int = 100
    WIDTH: int = 600
    HEIGHT: int = 600
    set_of_points = generate_random_set_of_points(
        50, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
    )

    alg_visualization = AlgorithmVisualization(WIDTH, HEIGHT, SCREEN_MARGIN, FPS)
    alg_visualization.animate_convex_hull("gift_wrapping", set_of_points)


if __name__ == "__main__":
    main()
