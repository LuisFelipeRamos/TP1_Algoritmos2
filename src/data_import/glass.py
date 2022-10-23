from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point
from src.segment.segment import Segment


def check_glass(file):

    col_names_glass = ["RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "TypeGlass"]
    glass = pd.read_csv(file, names=col_names_glass)

    glassclass1=glass[glass['TypeGlass']==1]
    glassclass2=glass[glass['TypeGlass']==6]
    glassclass1=glassclass1[['K','Si']]
    glassclass2=glassclass2[['K','Si']]

    glassclass1_train=glassclass1.sample(frac=0.7)
    glassclass1_test=glassclass1.drop(glassclass1_train.index)
    glassclass1_train.reset_index(drop=True,inplace=True)
    glassclass1_test.reset_index(drop=True,inplace=True)

    glassclass2_train=glassclass2.sample(frac=0.7)
    glassclass2_test=glassclass2.drop(glassclass2_train.index)
    glassclass2_train.reset_index(drop=True,inplace=True)
    glassclass2_test.reset_index(drop=True,inplace=True)

    list_glassclass1_train=[]
    for x in range(glassclass1_train['K'].size):
        temp_point=Point(glassclass1_train['K'][x],glassclass1_train['Si'][x])
        list_glassclass1_train.insert(1,temp_point)

    list_glassclass1_test=[]
    for x in range(glassclass1_test['K'].size):
        temp_point=Point(glassclass1_test['K'][x],glassclass1_test['Si'][x])
        list_glassclass1_test.insert(1,temp_point)
    
    list_glassclass2_train=[]
    for x in range(glassclass2_train['K'].size):
        temp_point=Point(glassclass2_train['K'][x],glassclass2_train['Si'][x])
        list_glassclass2_train.insert(1,temp_point)

    list_glassclass2_test=[]
    for x in range(glassclass2_test['K'].size):
        temp_point=Point(glassclass2_test['K'][x],glassclass2_test['Si'][x])
        list_glassclass2_test.insert(1,temp_point)

    sop1 = list_glassclass1_train
    sop2 = list_glassclass2_train
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
        label="Class 6",
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
    x = np.linspace(0, 3, 100)
    y = slope * x + b
    plt.title("Glass", fontsize=20)
    plt.xlabel("K", fontsize=20)
    plt.xticks(fontsize=10)
    plt.ylabel("Si", fontsize=20)
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

    class_1_seg = Segment(midpoint, list_glassclass1_train[0])

    class_1_side = class_1_seg.is_counter_clockwise(aux_segment)
    class_2_side = not class_1_side

    c = 0
    for point in list_glassclass2_test:
        new_seg = Segment(midpoint, point)
        if new_seg.is_counter_clockwise(aux_segment) == class_2_side:
            c += 1
        else:
            continue