import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


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
        temp_point = Point(titanicclass1_test["Class"][x], titanicclass1_test["Age"][x])
        list_titanicclass1_test.insert(1, temp_point)

    list_titanicclass2_train = []
    for x in range(titanicclass2_train["Class"].size):
        temp_point = Point(
            titanicclass2_train["Class"][x], titanicclass2_train["Age"][x]
        )
        list_titanicclass2_train.insert(1, temp_point)

    list_titanicclass2_test = []
    for x in range(titanicclass2_test["Class"].size):
        temp_point = Point(titanicclass2_test["Class"][x], titanicclass2_test["Age"][x])
        list_titanicclass2_test.insert(1, temp_point)

    sop1 = list_titanicclass1_train
    sop2 = list_titanicclass2_train

    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")

    D: DataProcessor = DataProcessor(
        ("Survived", "Didn't Survive"), "Titanic", ("Class", "Age")
    )

    D.plot(ch1, ch2, (-2, 2))

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
