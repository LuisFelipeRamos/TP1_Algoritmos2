import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_banana(file):

    col_names_banana = ["At1", "At2", "Class"]
    banana = pd.read_csv(file, names=col_names_banana)

    bananaclass1 = banana[banana["Class"] == 1.0]
    bananaclass2 = banana[banana["Class"] == -1.0]

    bananaclass1_train = bananaclass1.sample(frac=0.7)
    bananaclass1_test = bananaclass1.drop(bananaclass1_train.index)
    bananaclass1_train.reset_index(drop=True, inplace=True)
    bananaclass1_test.reset_index(drop=True, inplace=True)

    bananaclass2_train = bananaclass2.sample(frac=0.7)
    bananaclass2_test = bananaclass2.drop(bananaclass2_train.index)
    bananaclass2_train.reset_index(drop=True, inplace=True)
    bananaclass2_test.reset_index(drop=True, inplace=True)

    list_bananaclass1_train = []
    for x in range(bananaclass1_train["At1"].size):
        temp_point = Point(bananaclass1_train["At1"][x], bananaclass1_train["At2"][x])
        list_bananaclass1_train.insert(1, temp_point)

    list_bananaclass1_test = []
    for x in range(bananaclass1_test["At1"].size):
        temp_point = Point(bananaclass1_test["At1"][x], bananaclass1_test["At2"][x])
        list_bananaclass1_test.insert(1, temp_point)

    list_bananaclass2_train = []
    for x in range(bananaclass2_train["At1"].size):
        temp_point = Point(bananaclass2_train["At1"][x], bananaclass2_train["At2"][x])
        list_bananaclass2_train.insert(1, temp_point)

    list_bananaclass2_test = []
    for x in range(bananaclass2_test["At1"].size):
        temp_point = Point(bananaclass2_test["At1"][x], bananaclass2_test["At2"][x])
        list_bananaclass2_test.insert(1, temp_point)

    sop1 = list_bananaclass1_train
    sop2 = list_bananaclass2_train
    ch1: ConvexHull = ConvexHull(sop1, alg="graham_scan")
    ch2: ConvexHull = ConvexHull(sop2, alg="graham_scan")

    D: DataProcessor = DataProcessor(("1", "2"), "Banana", ("At1", "At2"))

    D.plot(ch1, ch2, (-3, 3))

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    intersect = line_sweep.do_polygons_intersect(ch1.convex_hull, ch2.convex_hull)

    linear_separable = False
    if not intersect:
        linear_separable = not (ch1.is_inside(ch2) or ch2.is_inside(ch1))
    if not linear_separable:
        print("Os dados não são linearmente separáveis")
