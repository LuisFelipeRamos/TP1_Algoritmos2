from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point
from src.segment.segment import Segment
from src.utils import get_perpendicular_segment, min_dist_between_convex_hulls_segment

def check_magic(file):

    col_names_magic = ["FLength", "FWidth", "FSize", "FConc", "FConc1", "FAsym", "FM3Long", "FM3Trans", "FAlpha", "FDist", "Class"]
    magic = pd.read_csv(file, names=col_names_magic)

    magicclass1=magic[magic['Class']=='g']
    magicclass2=magic[magic['Class']=='h']
    magicclass1=magicclass1[['FLength','FWidth']]
    magicclass2=magicclass2[['FLength','FWidth']]

    magicclass1_train=magicclass1.sample(frac=0.7)
    magicclass1_test=magicclass1.drop(magicclass1_train.index)
    magicclass1_train.reset_index(drop=True,inplace=True)
    magicclass1_test.reset_index(drop=True,inplace=True)

    magicclass2_train=magicclass2.sample(frac=0.7)
    magicclass2_test=magicclass2.drop(magicclass2_train.index)
    magicclass2_train.reset_index(drop=True,inplace=True)
    magicclass2_test.reset_index(drop=True,inplace=True)

    list_magicclass1_train=[]
    for x in range(magicclass1_train['FLength'].size):
        temp_point=Point(magicclass1_train['FLength'][x],magicclass1_train['FWidth'][x])
        list_magicclass1_train.insert(1,temp_point)

    list_magicclass1_test=[]
    for x in range(magicclass1_test['FLength'].size):
        temp_point=Point(magicclass1_test['FLength'][x],magicclass1_test['FWidth'][x])
        list_magicclass1_test.insert(1,temp_point)

    list_magicclass2_train=[]
    for x in range(magicclass2_train['FLength'].size):
        temp_point=Point(magicclass2_train['FLength'][x],magicclass2_train['FWidth'][x])
        list_magicclass2_train.insert(1,temp_point)

    list_magicclass2_test=[]
    for x in range(magicclass2_test['FLength'].size):
        temp_point=Point(magicclass2_test['FLength'][x],magicclass2_test['FWidth'][x])
        list_magicclass2_test.insert(1,temp_point)


    sop1 = list_magicclass1_train
    sop2 = list_magicclass2_train
    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")
    min_dist_segment = min_dist_between_convex_hulls_segment(ch1, ch2)

    _, ax = plt.subplots(figsize=(100, 100))
    ax = cast(plt.Axes, ax)

    ax.scatter(
        [point.x for point in ch1.set_of_points],
        [point.y for point in ch1.set_of_points],
        c=["red"],
        s=4,
        label="Class g"
    )
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)

    for edge in ch1.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "red", linewidth=0.5)

    ax.scatter(
        [point.x for point in ch2.set_of_points],
        [point.y for point in ch2.set_of_points],
        c=["blue"],
        s=4,
        label="Class h"
    )
    for edge in ch2.convex_hull:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "blue", linewidth=0.5)

    plt.plot(
        [min_dist_segment.p0.x, min_dist_segment.p1.x],
        [min_dist_segment.p0.y, min_dist_segment.p1.y],
        "black",
        linewidth=0.8
    )

    slope, b, midpoint = get_perpendicular_segment(min_dist_segment)
    x = np.linspace(0, 300, 100)
    y = slope * x + b
    plt.title("Magic", fontsize=20)
    plt.xlabel("FLength", fontsize=20)
    plt.xticks(fontsize=10)
    plt.ylabel("FWidth", fontsize=20)
    plt.yticks(fontsize=10)
    plt.plot(x, y, color="green", label=f"y = {round(slope, 2)}x + {round(b)}")
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

    aux_segment = Segment(midpoint, Point(midpoint.x + 1, (midpoint.x + 1) * slope + b))

    class_1_seg = Segment(midpoint, list_magicclass1_train[0])

    class_1_side = class_1_seg.is_counter_clockwise(aux_segment)
    class_2_side = not class_1_side

    c = 0
    for point in list_magicclass2_test:
        new_seg = Segment(midpoint, point)
        if new_seg.is_counter_clockwise(aux_segment) == class_2_side:
            c += 1
        else:
            continue
