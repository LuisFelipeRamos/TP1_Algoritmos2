import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_segment(file):

    col_names_segment = [
        "Region-centroid-col",
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
        "Class",
    ]
    segment = pd.read_csv(file, names=col_names_segment)

    segmentclass1 = segment[segment["Class"] == 1]
    segmentclass2 = segment[segment["Class"] == 2]
    segmentclass1 = segmentclass1[["Region-centroid-col", "Rawblue-mean"]]
    segmentclass2 = segmentclass2[["Region-centroid-col", "Rawblue-mean"]]

    segmentclass1_train = segmentclass1.sample(frac=0.7)
    segmentclass1_test = segmentclass1.drop(segmentclass1_train.index)
    segmentclass1_train.reset_index(drop=True, inplace=True)
    segmentclass1_test.reset_index(drop=True, inplace=True)

    segmentclass2_train = segmentclass2.sample(frac=0.7)
    segmentclass2_test = segmentclass2.drop(segmentclass2_train.index)
    segmentclass2_train.reset_index(drop=True, inplace=True)
    segmentclass2_test.reset_index(drop=True, inplace=True)

    list_segmentclass1_train = []
    for x in range(segmentclass1_train["Region-centroid-col"].size):
        temp_point = Point(
            segmentclass1_train["Region-centroid-col"][x],
            segmentclass1_train["Rawblue-mean"][x],
        )
        list_segmentclass1_train.insert(1, temp_point)

    list_segmentclass1_test = []
    for x in range(segmentclass1_test["Region-centroid-col"].size):
        temp_point = Point(
            segmentclass1_test["Region-centroid-col"][x],
            segmentclass1_test["Rawblue-mean"][x],
        )
        list_segmentclass1_test.insert(1, temp_point)

    list_segmentclass2_train = []
    for x in range(segmentclass2_train["Region-centroid-col"].size):
        temp_point = Point(
            segmentclass2_train["Region-centroid-col"][x],
            segmentclass2_train["Rawblue-mean"][x],
        )
        list_segmentclass2_train.insert(1, temp_point)

    list_segmentclass2_test = []
    for x in range(segmentclass2_test["Region-centroid-col"].size):
        temp_point = Point(
            segmentclass2_test["Region-centroid-col"][x],
            segmentclass2_test["Rawblue-mean"][x],
        )
        list_segmentclass2_test.insert(1, temp_point)

    sop1 = list_segmentclass1_train
    sop2 = list_segmentclass2_train
    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")

    D: DataProcessor = DataProcessor(
        ("1", "2"), "Segment", ("Region-centroid-col", "Rawblue-mean")
    )

    D.plot(ch1, ch2, (10, 300))
    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
