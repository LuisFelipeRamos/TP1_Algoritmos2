from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point
from src.segment.segment import Segment
from src.classifier import Classifier

def check_newthyroid(file):

    col_names_newthyroid = [
        "T3resin", "Thyroxin", "Triiodothyronine", "Thyroidstimulating", "TSH_value", "Class"]
    newthyroid = pd.read_csv(file, names=col_names_newthyroid)

    newthyroidclass1 = newthyroid[newthyroid["Class"] == 2]
    newthyroidclass2 = newthyroid[newthyroid["Class"] == 3]
    newthyroidclass1 = newthyroidclass1[["Thyroxin", "TSH_value"]]
    newthyroidclass2 = newthyroidclass2[["Thyroxin", "TSH_value"]]

    newthyroidclass1_train = newthyroidclass1.sample(frac=0.7)
    newthyroidclass1_test = newthyroidclass1.drop(newthyroidclass1_train.index)
    newthyroidclass1_train.reset_index(drop=True, inplace=True)
    newthyroidclass1_test.reset_index(drop=True, inplace=True)

    newthyroidclass2_train = newthyroidclass2.sample(frac=0.7)
    newthyroidclass2_test = newthyroidclass2.drop(newthyroidclass2_train.index)
    newthyroidclass2_train.reset_index(drop=True, inplace=True)
    newthyroidclass2_test.reset_index(drop=True, inplace=True)

    list_newthyroidclass1_train = []
    for x in range(newthyroidclass1_train["Thyroxin"].size):
        temp_point = Point(
            newthyroidclass1_train["Thyroxin"][x], newthyroidclass1_train["TSH_value"][x]
        )
        list_newthyroidclass1_train.insert(1, temp_point)

    list_newthyroidclass1_test = []
    for x in range(newthyroidclass1_test["Thyroxin"].size):
        temp_point = Point(
            newthyroidclass1_test["Thyroxin"][x], newthyroidclass1_test["TSH_value"][x]
        )
        list_newthyroidclass1_test.insert(1, temp_point)

    list_newthyroidclass2_train = []
    for x in range(newthyroidclass2_train["Thyroxin"].size):
        temp_point = Point(
            newthyroidclass2_train["Thyroxin"][x], newthyroidclass2_train["TSH_value"][x]
        )
        list_newthyroidclass2_train.insert(1, temp_point)

    list_newthyroidclass2_test = []
    for x in range(newthyroidclass2_test["Thyroxin"].size):
        temp_point = Point(
            newthyroidclass2_test["Thyroxin"][x], newthyroidclass2_test["TSH_value"][x]
        )
        list_newthyroidclass2_test.insert(1, temp_point)

    sop1 = list_newthyroidclass1_train
    sop2 = list_newthyroidclass2_train

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
        label="Class 2",
    )
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
    for edge in ch1.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "red", linewidth=0.5)

    ax.scatter(
        [point.x for point in ch2.set_of_points],
        [point.y for point in ch2.set_of_points],
        c=["blue"],
        s=2,
        label="Class 3",
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
    x = np.linspace(0, 10, 100)
    y = slope * x + b
    plt.title("Newthyroid", fontsize=20)
    plt.xlabel("Thyroxin", fontsize=20)
    plt.xticks(fontsize=10)
    plt.ylabel("TSH_value", fontsize=20)
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


    
