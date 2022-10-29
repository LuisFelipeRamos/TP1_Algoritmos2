from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point
from src.segment.segment import Segment
from src.classifier import Classifier

def check_titanic(file):

    col_names_titanic = [
        "Class",
        "Age",
        "Sex",
        "Survived",
    ]
    wine = pd.read_csv(file, names=col_names_titanic)

    titanicclass1 = wine[wine["Survived"] == 1]
    titanicclass2 = wine[wine["Survived"] == -1]
    titanicclass1 = titanicclass1[["Class", "Age"]]
    titanicclass2 = titanicclass2[["Class", "Age"]]

    titanicclass1_train = titanicclass1.sample(frac=0.7)
    titanicclass1_test = titanicclass1.drop(titanicclass1_train.index)
    titanicclass1_train.reset_index(drop=True, inplace=True)
    titanicclass1_test.reset_index(drop=True, inplace=True)

    titanicclass2_train = titanicclass2.sample(frac=0.7)
    titanicclass2_test = titanicclass2.drop(titanicclass2_train.index)
    titanicclass2_train.reset_index(drop=True, inplace=True)
    titanicclass2_test.reset_index(drop=True, inplace=True)

    list_titanicclass1_train = []
    for x in range(titanicclass1_train["Class"].size):
        temp_point = Point(
            titanicclass1_train["Class"][x], titanicclass1_train["Age"][x]
        )
        list_titanicclass1_train.insert(1, temp_point)

    list_titanicclass1_test = []
    for x in range(titanicclass1_test["Class"].size):
        temp_point = Point(
            titanicclass1_test["Class"][x], titanicclass1_test["Age"][x]
        )
        list_titanicclass1_test.insert(1, temp_point)

    list_titanicclass2_train = []
    for x in range(titanicclass2_train["Class"].size):
        temp_point = Point(
            titanicclass2_train["Class"][x], titanicclass2_train["Age"][x]
        )
        list_titanicclass2_train.insert(1, temp_point)

    list_titanicclass2_test = []
    for x in range(titanicclass2_test["Class"].size):
        temp_point = Point(
            titanicclass2_test["Class"][x], titanicclass2_test["Age"][x]
        )
        list_titanicclass2_test.insert(1, temp_point)

    sop1 = list_titanicclass1_train
    sop2 = list_titanicclass2_train

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
        label="Class 1 (survived)",
    )
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
    for edge in ch1.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "red", linewidth=0.5)

    ax.scatter(
        [point.x for point in ch2.set_of_points],
        [point.y for point in ch2.set_of_points],
        c=["blue"],
        s=2,
        label="Class  -1 (didn't survived)",
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
    x = np.linspace(-2, 2, 100)
    y = slope * x + b
    plt.title("Titanic", fontsize=20)
    plt.xlabel("Class", fontsize=20)
    plt.xticks(fontsize=10)
    plt.ylabel("Age", fontsize=20)
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


    
