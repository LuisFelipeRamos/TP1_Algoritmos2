import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_newthyroid(file):

    col_names_newthyroid = [
        "T3resin",
        "Thyroxin",
        "Triiodothyronine",
        "Thyroidstimulating",
        "TSH_value",
        "Class",
    ]
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
            newthyroidclass1_train["Thyroxin"][x],
            newthyroidclass1_train["TSH_value"][x],
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
            newthyroidclass2_train["Thyroxin"][x],
            newthyroidclass2_train["TSH_value"][x],
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

    D: DataProcessor = DataProcessor(
        ("2", "3"), "Newthyroid", ("Thyroxin", "TSH_value")
    )

    D.plot(ch1, ch2, (0, 10))

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
