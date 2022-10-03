from src.convex_hull.convex_hull import ConvexHull
from src.point.point import Point
import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from typing import cast

from src.animation import AlgorithmVisualization

def generate_random_set_of_points(number_of_points: int, min_x: int, max_x: int, min_y: int, max_y: int) -> list[Point]:
    set_of_points: list[Point] = []
    for _ in range(number_of_points):
        x: int
        y: int
        x, y = random.uniform(min_x, max_x)*random.uniform(min_x, max_x), random.uniform(min_y, max_y)*random.uniform(min_y, max_y)
        set_of_points.append(Point(math.sqrt(x), math.sqrt(y)))
    return set_of_points

def calculate_times_and_plot():
    l = []
    FPS: int = 60
    SCREEN_MARGIN: int = 0
    WIDTH: int = 600
    HEIGHT: int = 600
    for i in range(3, 100):
        times = [0, 0, 0]
        number_of_points = i
        for _ in range(100):
            set_of_points = generate_random_set_of_points(
            number_of_points, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
        )
            a1 = time.time()
            convex_hull = ConvexHull(set_of_points, alg='graham_scan')
            a2 = time.time()
            times[0] += a2 - a1
        
        for _ in range(100):
            set_of_points = generate_random_set_of_points(
            number_of_points, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
        )
            a1 = time.time()
            convex_hull = ConvexHull(set_of_points, alg='gift_wrapping')
            a2 = time.time()
            times[1] += a2 - a1
        for _ in range(100):
            set_of_points = generate_random_set_of_points(
            number_of_points, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
        )
            a1 = time.time()
            convex_hull = ConvexHull(set_of_points, alg='incremental')
            a2 = time.time()
            times[2] += a2 - a1
        for e in times:
            e/=100
        l.append(times)
    
    plt.plot([i for i in range(3, 100)], [t[0] for t in l], color="red")
    plt.plot([i for i in range(3, 100)], [t[1] for t in l], color="blue")
    plt.plot([i for i in range(3, 100)], [t[2] for t in l], color="green")
    plt.legend(["Algoritmo da varredura de Graham", "Algoritmo do embrulho de presente", "Algoritmo incremental"])
    plt.xlabel("Número de pontos do conjunto")
    plt.ylabel("Tempo de execução do algoritmo")
    plt.title("Comparação de tempo para cada algoritmo de envoltória convexa")
    plt.grid(True)
    plt.show()


def run():
    FPS: int = 60
    SCREEN_MARGIN: int = 100
    WIDTH: int = 600
    HEIGHT: int = 600
    number_of_points = 25

    set_of_points = generate_random_set_of_points(
            number_of_points, SCREEN_MARGIN, WIDTH - SCREEN_MARGIN, SCREEN_MARGIN, HEIGHT - SCREEN_MARGIN
        )
    algo_vis = AlgorithmVisualization(WIDTH, HEIGHT, SCREEN_MARGIN, FPS)
    algo_vis.animate_convex_hull("incremental", set_of_points)

    
   
  

