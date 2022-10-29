from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point
from src.segment.segment import Segment


def check_mammographic(file):

    col_names_mammographic = ["BI-RADS", "Age", "Shape", "Margin", "Density", "Severity"]
    mammographic = pd.read_csv(file, names=col_names_mammographic)

    mammographicclass1=mammographic[mammographic["Severity"]==0]
    mammographicclass2=mammographic[mammographic["Severity"]==1]
    mammographicclass1=mammographicclass1[["Age","Density"]]
    mammographicclass2=mammographicclass2[["Age","Density"]]

    mammographicclass1_train=mammographicclass1.sample(frac=0.7)
    mammographicclass1_test=mammographicclass1.drop(mammographicclass1_train.index)
    mammographicclass1_train.reset_index(drop=True,inplace=True)
    mammographicclass1_test.reset_index(drop=True,inplace=True)

    mammographicclass2_train=mammographicclass2.sample(frac=0.7)
    mammographicclass2_test=mammographicclass2.drop(mammographicclass2_train.index)
    mammographicclass2_train.reset_index(drop=True,inplace=True)
    mammographicclass2_test.reset_index(drop=True,inplace=True)

    list_mammographicclass1_train=[]
    for x in range(mammographicclass1_train["Age"].size):
        temp_point=Point(mammographicclass1_train["Age"][x],mammographicclass1_train["Density"][x])
        list_mammographicclass1_train.insert(1,temp_point)

    list_mammographicclass1_test=[]
    for x in range(mammographicclass1_test["Age"].size):
        temp_point=Point(mammographicclass1_test["Age"][x],mammographicclass1_test["Density"][x])
        list_mammographicclass1_test.insert(1,temp_point)
    
    list_mammographicclass2_train=[]
    for x in range(mammographicclass2_train["Age"].size):
        temp_point=Point(mammographicclass2_train["Age"][x],mammographicclass2_train["Density"][x])
        list_mammographicclass2_train.insert(1,temp_point)

    list_mammographicclass2_test=[]
    for x in range(mammographicclass2_test["Age"].size):
        temp_point=Point(mammographicclass2_test["Age"][x],mammographicclass2_test["Density"][x])
        list_mammographicclass2_test.insert(1,temp_point)

    sop1 = list_mammographicclass1_train
    sop2 = list_mammographicclass2_train
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
        label="Class 0",
    )
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
    for edge in ch1.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "red", linewidth=0.5)

    ax.scatter(
        [point.x for point in ch2.set_of_points],
        [point.y for point in ch2.set_of_points],
        c=["blue"],
        s=2,
        label="Class 1",
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
    x = np.linspace(11, 15, 100)
    y = slope * x + b
    plt.title("Mammographic", fontsize=20)
    plt.xlabel("Age", fontsize=20)
    plt.xticks(fontsize=10)
    plt.ylabel("Density", fontsize=20)
    plt.yticks(fontsize=10)
    plt.plot(x, y, color="green", label=f"y = {round(slope, 2)}x + {round(b, 2)}")
    plt.legend(loc="upper left", fontsize=15)
    plt.show()

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
        return
