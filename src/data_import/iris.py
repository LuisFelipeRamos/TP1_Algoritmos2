from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point
from src.segment.segment import Segment
from src.utils import min_dist_between_convex_hulls_segment


def check_iris(file):

    col_names_iris = ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth", "Class"]
    iris = pd.read_csv(file, names=col_names_iris)

    irisclass1 = iris[iris["Class"] != " Iris-setosa"]
    irisclass2 = iris[iris["Class"] == " Iris-setosa"]
    irisclass1 = irisclass1[["PetalLength", "PetalWidth"]]
    irisclass2 = irisclass2[["PetalLength", "PetalWidth"]]

    irisclass1_train = irisclass1.sample(frac=0.7)
    irisclass1_test = irisclass1.drop(irisclass1_train.index)
    irisclass1_train.reset_index(drop=True, inplace=True)
    irisclass1_test.reset_index(drop=True, inplace=True)

    irisclass2_train = irisclass2.sample(frac=0.7)
    irisclass2_test = irisclass2.drop(irisclass2_train.index)
    irisclass2_train.reset_index(drop=True, inplace=True)
    irisclass2_test.reset_index(drop=True, inplace=True)

    list_irisclass1_train = []
    for x in range(irisclass1_train["PetalLength"].size):
        temp_point = Point(
            irisclass1_train["PetalLength"][x], irisclass1_train["PetalWidth"][x]
        )
        list_irisclass1_train.insert(1, temp_point)

    list_irisclass1_test = []
    for x in range(irisclass1_test["PetalLength"].size):
        temp_point = Point(
            irisclass1_test["PetalLength"][x], irisclass1_test["PetalWidth"][x]
        )
        list_irisclass1_test.insert(1, temp_point)

    list_irisclass2_train = []
    for x in range(irisclass2_train["PetalLength"].size):
        temp_point = Point(
            irisclass2_train["PetalLength"][x], irisclass2_train["PetalWidth"][x]
        )
        list_irisclass2_train.insert(1, temp_point)

    list_irisclass2_test = []
    for x in range(irisclass2_test["PetalLength"].size):
        temp_point = Point(
            irisclass2_test["PetalLength"][x], irisclass2_test["PetalWidth"][x]
        )
        list_irisclass2_test.insert(1, temp_point)

    sop1 = list_irisclass1_train
    sop2 = list_irisclass2_train
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
        label="Class Iris-setosa"
    )
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
    for edge in ch1.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "red", linewidth=0.5)

    ax.scatter(
        [point.x for point in ch2.set_of_points],
        [point.y for point in ch2.set_of_points],
        c=["blue"],
        s=2,
        label="Class not Iris-setosa"
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
    x = np.linspace(1, 4, 100)
    y = slope * x + b
    plt.title("Iris", fontsize=20)
    plt.xlabel("Petal Length", fontsize=20)
    plt.xticks(fontsize=10)
    plt.ylabel("Petal Width", fontsize=20)
    plt.yticks(fontsize=10)
    plt.plot(x, y, color="green", label=f"y = {round(slope, 2)}x + {b}")
    plt.legend(loc="lower right", fontsize=15)
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

    class_1_seg = Segment(midpoint, list_irisclass1_train[0])

    class_1_side = class_1_seg.is_counter_clockwise(aux_segment)
    class_2_side = not class_1_side

    c = 0
    for point in list_irisclass2_test:
        new_seg = Segment(midpoint, point)
        if new_seg.is_counter_clockwise(aux_segment) == class_2_side:
            c += 1
        else:
            continue
