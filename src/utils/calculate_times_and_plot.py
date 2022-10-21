import random
import time

import matplotlib.pyplot as plt

from src.convex_hull.convex_hull import ConvexHull
from src.point.point import Point


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
    l: list[list[float]] = []
    SCREEN_MARGIN: int = 0
    WIDTH: int = 600
    HEIGHT: int = 600
    for number_of_points in range(3, 100):
        times: list[float] = [0.0, 0.0, 0.0]
        algorithms: list[str] = ["graham_scan", "gift_wrapping", "incremental"]
        for _ in range(100):
            for j in range(3):
                set_of_points: list[Point] = generate_random_set_of_points(
                    number_of_points,
                    SCREEN_MARGIN,
                    WIDTH - SCREEN_MARGIN,
                    SCREEN_MARGIN,
                    HEIGHT - SCREEN_MARGIN,
                )
                a_1: float = time.time()
                convex_hull: ConvexHull = ConvexHull(set_of_points, alg=algorithms[j])
                a_2: float = time.time()
                times[j] += a_2 - a_1

        for k in times:
            k /= 100
        l.append(times)

    plt.plot(
        list(range(3, 100)),
        [t[0] for t in l],
        color="red",
        label="Varredura de Graham",
    )
    plt.plot(
        list(range(3, 100)),
        [t[1] for t in l],
        color="blue",
        label="Embrulho de Presente",
    )
    plt.plot(
        list(range(3, 100)),
        [t[2] for t in l],
        color="green",
        label="Incremental",
    )
    plt.legend()
    plt.xlabel("Número de pontos do conjunto")
    plt.ylabel("Tempo de execução do algoritmo")
    plt.title("Comparação de tempo para cada algoritmo de envoltória convexa")
    plt.savefig("filename.png", dpi=1000)
    plt.grid(True)
    plt.show()