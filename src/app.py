from ast import arg
import math
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import argparse
from typing import cast

from src.convex_hull.convex_hull import ConvexHull
from src.point.point import Point
from src.utils import min_dist_between_convex_hulls_segment, get_perpendicular_segment


def generate_random_set_of_points(
    number_of_points: int, min_x: int, max_x: int, min_y: int, max_y: int
) -> list[Point]:
    set_of_points: list[Point] = []
    for _ in range(number_of_points):
        x: float
        y: float
        x, y = random.uniform(min_x, max_x), random.uniform(min_y, max_y)
        set_of_points.append(Point(x, y))
    return set_of_points


def calculate_times_and_plot():
    l = []
    SCREEN_MARGIN: int = 0
    WIDTH: int = 600
    HEIGHT: int = 600
    for i in range(3, 100):
        times = [0.0, 0.0, 0.0]
        number_of_points = i
        for _ in range(100):
            set_of_points = generate_random_set_of_points(
                number_of_points,
                SCREEN_MARGIN,
                WIDTH - SCREEN_MARGIN,
                SCREEN_MARGIN,
                HEIGHT - SCREEN_MARGIN,
            )
            a1 = time.time()
            convex_hull = ConvexHull(set_of_points, alg="graham_scan")
            a2 = time.time()
            times[0] += a2 - a1

        for _ in range(100):
            set_of_points = generate_random_set_of_points(
                number_of_points,
                SCREEN_MARGIN,
                WIDTH - SCREEN_MARGIN,
                SCREEN_MARGIN,
                HEIGHT - SCREEN_MARGIN,
            )
            a1 = time.time()
            convex_hull = ConvexHull(set_of_points, alg="gift_wrapping")
            a2 = time.time()
            times[1] += a2 - a1
        for _ in range(100):
            set_of_points = generate_random_set_of_points(
                number_of_points,
                SCREEN_MARGIN,
                WIDTH - SCREEN_MARGIN,
                SCREEN_MARGIN,
                HEIGHT - SCREEN_MARGIN,
            )
            a1 = time.time()
            convex_hull = ConvexHull(set_of_points, alg="incremental")
            a2 = time.time()
            times[2] += a2 - a1
        for e in times:
            e /= 100
        l.append(times)

    plt.plot([i for i in range(3, 100)], [t[0] for t in l], color="red")
    plt.plot([i for i in range(3, 100)], [t[1] for t in l], color="blue")
    plt.plot([i for i in range(3, 100)], [t[2] for t in l], color="green")
    plt.legend(
        [
            "Algoritmo da varredura de Graham",
            "Algoritmo do embrulho de presente",
            "Algoritmo incremental",
        ]
    )
    plt.savefig('filename.png', dpi=1000)
    plt.xlabel("Número de pontos do conjunto")
    plt.ylabel("Tempo de execução do algoritmo")
    plt.title("Comparação de tempo para cada algoritmo de envoltória convexa")
    plt.grid(True)
    plt.show()


def run():
    
    parser = argparse.ArgumentParser(description="Recebe arquivos .dat para checar se são linearmente separáveis")
    parser.add_argument("--file", dest="file", required=False, type=str, help="arquivo .dat que contêm dados a serem treinados")
    args = parser.parse_args()

    sop1 = generate_random_set_of_points(20, 5, 10, 5, 10)
    sop2 = generate_random_set_of_points(20, 15, 20, 15, 20)
    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")

    min_dist_segment = min_dist_between_convex_hulls_segment(ch1, ch2)

    _, ax = plt.subplots(figsize=(100, 100))
    ax = cast(plt.Axes, ax)

    ax.scatter(
        [point.x for point in ch1.set_of_points],
        [point.y for point in ch1.set_of_points],
        c=["red"],
        s=2,
    )
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
    for edge in ch1.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "k", linewidth=0.5)
    
    ax.scatter(
        [point.x for point in ch2.set_of_points],
        [point.y for point in ch2.set_of_points],
        c=["green"],
        s=2,
    )
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
    for edge in ch2.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "k", linewidth=0.5)
    
    plt.plot([min_dist_segment.p0.x, min_dist_segment.p1.x], [min_dist_segment.p0.y, min_dist_segment.p1.y], "yellow", linewidth=.8)

    slope, b = get_perpendicular_segment(min_dist_segment)
    x = np.linspace(5, 20, 100)
    y = slope*x + b
    plt.plot(x, y, "-r")

    plt.show()

    
    
    
    

    

