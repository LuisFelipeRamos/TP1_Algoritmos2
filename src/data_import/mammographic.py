import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_mammographic(file):

    col_names_mammographic = [
        "BI-RADS",
        "Age",
        "Shape",
        "Margin",
        "Density",
        "Severity",
    ]
    mammographic = pd.read_csv(file, names=col_names_mammographic)

    mammographicclass1 = mammographic[mammographic["Severity"] == 0]
    mammographicclass2 = mammographic[mammographic["Severity"] == 1]
    mammographicclass1 = mammographicclass1[["Age", "Density"]]
    mammographicclass2 = mammographicclass2[["Age", "Density"]]

    mammographicclass1_train = mammographicclass1.sample(frac=0.7)
    mammographicclass1_test = mammographicclass1.drop(mammographicclass1_train.index)
    mammographicclass1_train.reset_index(drop=True, inplace=True)
    mammographicclass1_test.reset_index(drop=True, inplace=True)

    mammographicclass2_train = mammographicclass2.sample(frac=0.7)
    mammographicclass2_test = mammographicclass2.drop(mammographicclass2_train.index)
    mammographicclass2_train.reset_index(drop=True, inplace=True)
    mammographicclass2_test.reset_index(drop=True, inplace=True)

    list_mammographicclass1_train = []
    for x in range(mammographicclass1_train["Age"].size):
        temp_point = Point(
            mammographicclass1_train["Age"][x], mammographicclass1_train["Density"][x]
        )
        list_mammographicclass1_train.insert(1, temp_point)

    list_mammographicclass1_test = []
    for x in range(mammographicclass1_test["Age"].size):
        temp_point = Point(
            mammographicclass1_test["Age"][x], mammographicclass1_test["Density"][x]
        )
        list_mammographicclass1_test.insert(1, temp_point)

    list_mammographicclass2_train = []
    for x in range(mammographicclass2_train["Age"].size):
        temp_point = Point(
            mammographicclass2_train["Age"][x], mammographicclass2_train["Density"][x]
        )
        list_mammographicclass2_train.insert(1, temp_point)

    list_mammographicclass2_test = []
    for x in range(mammographicclass2_test["Age"].size):
        temp_point = Point(
            mammographicclass2_test["Age"][x], mammographicclass2_test["Density"][x]
        )
        list_mammographicclass2_test.insert(1, temp_point)

    sop1 = list_mammographicclass1_train
    sop2 = list_mammographicclass2_train
    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")

    D: DataProcessor = DataProcessor(("1", "2"), "Mammographic", ("Age", "Density"))

    D.plot(ch1, ch2, (11, 15))

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
