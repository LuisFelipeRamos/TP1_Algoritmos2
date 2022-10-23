from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point
from src.segment.segment import Segment


def check_haberman(file):

    col_names_haberman = ["Age", "Year", "Positive", "Survival"]
    haberman = pd.read_csv(file, names=col_names_haberman)

    habermanclass1 = haberman[haberman["Survival"] == " positive"]
    habermanclass2 = haberman[haberman["Survival"] == " negative"]
    habermanclass1 = habermanclass1[["Age", "Positive"]]
    habermanclass2 = habermanclass2[["Age", "Positive"]]

    habermanclass1_train = habermanclass1.sample(frac=0.7)
    habermanclass1_test = habermanclass1.drop(habermanclass1_train.index)
    habermanclass1_train.reset_index(drop=True, inplace=True)
    habermanclass1_test.reset_index(drop=True, inplace=True)

    habermanclass2_train = habermanclass2.sample(frac=0.7)
    habermanclass2_test = habermanclass2.drop(habermanclass2_train.index)
    habermanclass2_train.reset_index(drop=True, inplace=True)
    habermanclass2_test.reset_index(drop=True, inplace=True)

    list_habermanclass1_train = []
    for x in range(habermanclass1_train["Age"].size):
        temp_point = Point(
            habermanclass1_train["Age"][x], habermanclass1_train["Positive"][x]
        )
        list_habermanclass1_train.insert(1, temp_point)

    list_habermanclass1_test = []
    for x in range(habermanclass1_test["Age"].size):
        temp_point = Point(
            habermanclass1_test["Age"][x], habermanclass1_test["Positive"][x]
        )
        list_habermanclass1_test.insert(1, temp_point)

    list_habermanclass2_train = []
    for x in range(habermanclass2_train["Age"].size):
        temp_point = Point(
            habermanclass2_train["Age"][x], habermanclass2_train["Positive"][x]
        )
        list_habermanclass2_train.insert(1, temp_point)

    list_habermanclass2_test = []
    for x in range(habermanclass2_test["Age"].size):
        temp_point = Point(
            habermanclass2_test["Age"][x], habermanclass2_test["Positive"][x]
        )
        list_habermanclass2_test.insert(1, temp_point)

    sop1 = list_habermanclass1_train
    sop2 = list_habermanclass2_train
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
    plt.plot(x, y, color="green", label=f"y = {round(slope, 2)}x + {round(b, 2)}")
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

    class_1_seg = Segment(midpoint, list_habermanclass1_train[0])

    class_1_side = class_1_seg.is_counter_clockwise(aux_segment)
    class_2_side = not class_1_side

    c = 0
    for point in list_habermanclass2_test:
        new_seg = Segment(midpoint, point)
        if new_seg.is_counter_clockwise(aux_segment) == class_2_side:
            c += 1
        else:
            continue
