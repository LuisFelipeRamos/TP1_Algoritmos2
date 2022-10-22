from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_banana(file):

    col_names_banana = ["At1", "At2", "Class"]
    banana = pd.read_csv(file, names=col_names_banana)

    bananaclass1 = banana[banana["Class"] == "1.0"]
    bananaclass2 = banana[banana["Class"] == "-1.0"]

    bananaclass1_train = bananaclass1.sample(frac=0.7)
    bananaclass1_test = bananaclass1.drop(bananaclass1_train.index)
    bananaclass1_train.reset_index(drop=True, inplace=True)
    bananaclass1_test.reset_index(drop=True, inplace=True)

    bananaclass2_train = bananaclass2.sample(frac=0.7)
    bananaclass2_test = bananaclass2.drop(bananaclass2_train.index)
    bananaclass2_train.reset_index(drop=True, inplace=True)
    bananaclass2_test.reset_index(drop=True, inplace=True)

    list_bananaclass1_train = []
    for x in range(bananaclass1_train["At1"].size):
        temp_point = Point(bananaclass1_train["At1"][x], bananaclass1_train["At2"][x])
        list_bananaclass1_train.insert(1, temp_point)

    list_bananaclass1_test = []
    for x in range(bananaclass1_test["At1"].size):
        temp_point = Point(bananaclass1_test["At1"][x], bananaclass1_test["At2"][x])
        list_bananaclass1_test.insert(1, temp_point)

    list_bananaclass2_train = []
    for x in range(bananaclass2_train["At1"].size):
        temp_point = Point(bananaclass2_train["At1"][x], bananaclass2_train["At2"][x])
        list_bananaclass2_train.insert(1, temp_point)

    list_bananaclass2_test = []
    for x in range(bananaclass2_test["At1"].size):
        temp_point = Point(bananaclass2_test["At1"][x], bananaclass2_test["At2"][x])
        list_bananaclass2_test.insert(1, temp_point)

    sop1 = list_bananaclass1_train
    sop2 = list_bananaclass2_train
    ch1: ConvexHull = ConvexHull(sop1, alg="graham_scan")
    ch2: ConvexHull = ConvexHull(sop2, alg="graham_scan")
    min_dist_segment = ch1.min_dist(ch2)

    _, ax = plt.subplots(figsize=(100, 100))
    ax = cast(plt.Axes, ax)

    ax.scatter(
        [point.x for point in ch1.set_of_points],
        [point.y for point in ch1.set_of_points],
        c=["red"],
        s=2,
        label="Class 1",
    )
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
    for edge in ch1.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "red", linewidth=0.5)

    ax.scatter(
        [point.x for point in ch2.set_of_points],
        [point.y for point in ch2.set_of_points],
        c=["blue"],
        s=2,
        label="Class 2",
    )
    for edge in ch2.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "blue", linewidth=0.5)

    plt.plot(
        [min_dist_segment.p0.x, min_dist_segment.p1.x],
        [min_dist_segment.p0.y, min_dist_segment.p1.y],
        "black",
        linewidth=0.8,
    )

    slope, b, _ = min_dist_segment.get_perpendicular_segment()
    x = np.linspace(-2, 2, 100)
    y = slope * x + b
    plt.title("Banana", fontsize=20)
    plt.xlabel("At1", fontsize=20)
    plt.xticks(fontsize=10)
    plt.ylabel("At2", fontsize=20)
    plt.yticks(fontsize=10)
    plt.plot(x, y, color="green", label=f"y = {round(slope, 2)}x + {round(b, 2)}")
    plt.legend(loc="upper left", fontsize=15)
    plt.show()

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    intersect = line_sweep.do_polygons_intersect(ch1.convex_hull, ch2.convex_hull)

    linear_separable = False
    if not intersect:
        linear_separable = not (ch1.is_inside(ch2) or ch2.is_inside(ch1))
    if not linear_separable:
        print("Os dados não são linearmente separáveis")
