from src.point.point import Point
from src.segment.segment import Segment
from src.convex_hull import ConvexHull, convex_hull

from pygame_animation import AlgorithmVisualization

# libs
import math
import random
import time
import pygame


def generate_random_set_of_points(number_of_points, min_x, max_x, min_y, max_y):
    set_of_points = []
    for _ in range(number_of_points):
        x, y = random.randint(min_x, max_x), random.randint(min_x, max_y)
        set_of_points.append(Point(x, y))

    return set_of_points

def main():
    
    """ alg_times = [0, 0]
    
    set_of_points = []
    typer = 0
    for i in range(1000):
        type=1
        set_of_points = generate_random_set_of_points(10, 1, 100, 1, 100)
        t0 = time.time()
        convex_hull = ConvexHull(set_of_points, alg='gift_wrapping')
        t1 = time.time()
        alg_times[0] += t1 - t0
    alg_times[0] /= 100

    for i in range(1000):
        typer=2
        set_of_points = generate_random_set_of_points(10, 1, 100, 1, 100)
        t0 = time.time()
        convex_hull = ConvexHull(set_of_points, alg='graham_scan')
        t1 = time.time()
        alg_times[1] += t1 - t0
    alg_times[1]/=100
    
    print(alg_times) """

    FPS = 60
    SCREEN_MARGIN = 100
    WIDTH, HEIGHT = 600, 600         
    set_of_points = generate_random_set_of_points(50, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN)

    """ alg_visualization = AlgorithmVisualization(WIDTH, HEIGHT,SCREEN_MARGIN, FPS)
    alg_visualization.animate_convex_hull("gift_wrapping", set_of_points) """

    convex_hull = ConvexHull(set_of_points, "gift_wrapping")
    convex_hull.plot(WIDTH)

if __name__ == "__main__":
    main()