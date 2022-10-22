from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point
from src.segment.segment import Segment


def check_wine(file):

    col_names_wine = [
        "Alcohol",
        "MalicAcid",
        "Ash",
        "AlcalinityOfAsh",
        "Magnesium",
        "TotalPhenols",
        "flavanoids",
        "NonflavanoidsPhenols",
        "Proanthocyanins",
        "ColorIntensity",
        "Hue",
        "OD280/OD315",
        "Proline",
        "Class",
    ]
    wine = pd.read_csv(file, names=col_names_wine)

    wineclass1 = wine[wine["Class"] == 1]
    wineclass2 = wine[wine["Class"] == 3]
    wineclass1 = wineclass1[["Magnesium", "flavanoids"]]
    wineclass2 = wineclass2[["Magnesium", "flavanoids"]]

    wineclass1_train = wineclass1.sample(frac=0.7)
    wineclass1_test = wineclass1.drop(wineclass1_train.index)
    wineclass1_train.reset_index(drop=True, inplace=True)
    wineclass1_test.reset_index(drop=True, inplace=True)

    wineclass2_train = wineclass2.sample(frac=0.7)
    wineclass2_test = wineclass2.drop(wineclass2_train.index)
    wineclass2_train.reset_index(drop=True, inplace=True)
    wineclass2_test.reset_index(drop=True, inplace=True)

    list_wineclass1_train = []
    for x in range(wineclass1_train["Magnesium"].size):
        temp_point = Point(
            wineclass1_train["Magnesium"][x], wineclass1_train["flavanoids"][x]
        )
        list_wineclass1_train.insert(1, temp_point)

    list_wineclass1_test = []
    for x in range(wineclass1_test["Magnesium"].size):
        temp_point = Point(
            wineclass1_test["Magnesium"][x], wineclass1_test["flavanoids"][x]
        )
        list_wineclass1_test.insert(1, temp_point)

    list_wineclass2_train = []
    for x in range(wineclass2_train["Magnesium"].size):
        temp_point = Point(
            wineclass2_train["Magnesium"][x], wineclass2_train["flavanoids"][x]
        )
        list_wineclass2_train.insert(1, temp_point)

    list_wineclass2_test = []
    for x in range(wineclass2_test["Magnesium"].size):
        temp_point = Point(
            wineclass2_test["Magnesium"][x], wineclass2_test["flavanoids"][x]
        )
        list_wineclass2_test.insert(1, temp_point)

    sop1 = list_wineclass1_train
    sop2 = list_wineclass2_train
    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")
    min_dist_segment = ch1.min_dist(ch2)

    _, ax = plt.subplots(figsize=(100, 100))
    ax = cast(plt.Axes, ax)

    ax.scatter(
        [point.x for point in ch1.set_of_points],
        [point.y for point in ch1.set_of_points],
        c=["red"],
        s=2,
        label="Class positive",
    )
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
    for edge in ch1.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "red", linewidth=0.5)

    ax.scatter(
        [point.x for point in ch2.set_of_points],
        [point.y for point in ch2.set_of_points],
        c=["blue"],
        s=2,
        label="Class negative",
    )
    for edge in ch2.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "blue", linewidth=0.5)

    plt.plot(
        [min_dist_segment.p0.x, min_dist_segment.p1.x],
        [min_dist_segment.p0.y, min_dist_segment.p1.y],
        "black",
        linewidth=0.8,
    )

    slope, b, midpoint = min_dist_segment.get_perpendicular_segment()
    x = np.linspace(30, 90, 100)
    y = slope * x + b
    plt.title("Haberman", fontsize=20)
    plt.xlabel("Petal Length", fontsize=20)
    plt.xticks(fontsize=10)
    plt.ylabel("Petal Width", fontsize=20)
    plt.yticks(fontsize=10)
    plt.plot(x, y, color="green", label=f"y = {round(slope, 2)}x + {b}")
    plt.legend(loc="upper right", fontsize=15)
    plt.show()

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
        return

    aux_segment = Segment(midpoint, Point(midpoint.x + 1, (midpoint.x + 1) * slope + b))

    class_1_seg = Segment(midpoint, list_wineclass1_train[0])

    class_1_side = class_1_seg.is_counter_clockwise(aux_segment)
    class_2_side = not class_1_side

    c = 0
    for point in list_wineclass2_test:
        new_seg = Segment(midpoint, point)
        if new_seg.is_counter_clockwise(aux_segment) == class_2_side:
            c += 1
        else:
            continue
