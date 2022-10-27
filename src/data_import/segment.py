from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point
from src.segment.segment import Segment


def check_segment(file):

    col_names_segment = ["Region-centroid-col", 
    "Region-centroid-row", 
    "Region-pixel-count", 
    "Short-line-density-5", 
    "Short-line-density-2", 
    "Vedge-mean",
    "Vegde-sd", 
    "Hedge-mean",
    "Hedge-sd", 
    "Intensity-mean", 
    "Rawred-mean", 
    "Rawblue-mean", 
    "Rawgreen-mean", 
    "Exred-mean", 
    "Exblue-mean", 
    "Exgreen-mean",
    "Value-mean", 
    "Saturatoin-mean",
    "Hue-mean",
    "Class"]
    segment = pd.read_csv(file, names=col_names_segment)

    segmentclass1=segment[segment['Class']==1]
    segmentclass2=segment[segment['Class']==6]
    segmentclass1=segmentclass1[["Region-centroid-col","Rawblue-mean"]]
    segmentclass2=segmentclass2[["Region-centroid-col","Rawblue-mean"]]

    segmentclass1_train=segmentclass1.sample(frac=0.7)
    segmentclass1_test=segmentclass1.drop(segmentclass1_train.index)
    segmentclass1_train.reset_index(drop=True,inplace=True)
    segmentclass1_test.reset_index(drop=True,inplace=True)

    segmentclass2_train=segmentclass2.sample(frac=0.7)
    segmentclass2_test=segmentclass2.drop(segmentclass2_train.index)
    segmentclass2_train.reset_index(drop=True,inplace=True)
    segmentclass2_test.reset_index(drop=True,inplace=True)

    list_segmentclass1_train=[]
    for x in range(segmentclass1_train["Region-centroid-col"].size):
        temp_point=Point(segmentclass1_train["Region-centroid-col"][x],segmentclass1_train["Rawblue-mean"][x])
        list_segmentclass1_train.insert(1,temp_point)

    list_segmentclass1_test=[]
    for x in range(segmentclass1_test["Region-centroid-col"].size):
        temp_point=Point(segmentclass1_test["Region-centroid-col"][x],segmentclass1_test["Rawblue-mean"][x])
        list_segmentclass1_test.insert(1,temp_point)
    
    list_segmentclass2_train=[]
    for x in range(segmentclass2_train["Region-centroid-col"].size):
        temp_point=Point(segmentclass2_train["Region-centroid-col"][x],segmentclass2_train["Rawblue-mean"][x])
        list_segmentclass2_train.insert(1,temp_point)

    list_segmentclass2_test=[]
    for x in range(segmentclass2_test["Region-centroid-col"].size):
        temp_point=Point(segmentclass2_test["Region-centroid-col"][x],segmentclass2_test["Rawblue-mean"][x])
        list_segmentclass2_test.insert(1,temp_point)

    sop1 = list_segmentclass1_train
    sop2 = list_segmentclass2_train
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
    x = np.linspace(8, 10, 100)
    y = slope * x + b
    plt.title("Segment", fontsize=20)
    plt.xlabel("Region-centroid-col", fontsize=20)
    plt.xticks(fontsize=10)
    plt.ylabel("Rawblue-mean", fontsize=20)
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
