import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_haberman(file):

    col_names_haberman = ["Age", "Year", "Positive", "Survival"]
    haberman = pd.read_csv(file, names=col_names_haberman)

    habermanclass1 = haberman[haberman["Survival"] == " positive"]
    habermanclass2 = haberman[haberman["Survival"] == " negative"]
    habermanclass1 = habermanclass1[["Age", "Positive"]]
    habermanclass2 = habermanclass2[["Age", "Positive"]]

    habermanclass1_train = habermanclass1.sample(frac=0.7)
    habermanclass1_test = habermanclass1.drop(habermanclass1_train.index)
    habermanclass1_train.reset_index(drop=True, inplace=True)
    habermanclass1_test.reset_index(drop=True, inplace=True)

    habermanclass2_train = habermanclass2.sample(frac=0.7)
    habermanclass2_test = habermanclass2.drop(habermanclass2_train.index)
    habermanclass2_train.reset_index(drop=True, inplace=True)
    habermanclass2_test.reset_index(drop=True, inplace=True)

    list_habermanclass1_train = []
    for x in range(habermanclass1_train["Age"].size):
        temp_point = Point(
            habermanclass1_train["Age"][x], habermanclass1_train["Positive"][x]
        )
        list_habermanclass1_train.insert(1, temp_point)

    list_habermanclass1_test = []
    for x in range(habermanclass1_test["Age"].size):
        temp_point = Point(
            habermanclass1_test["Age"][x], habermanclass1_test["Positive"][x]
        )
        list_habermanclass1_test.insert(1, temp_point)

    list_habermanclass2_train = []
    for x in range(habermanclass2_train["Age"].size):
        temp_point = Point(
            habermanclass2_train["Age"][x], habermanclass2_train["Positive"][x]
        )
        list_habermanclass2_train.insert(1, temp_point)

    list_habermanclass2_test = []
    for x in range(habermanclass2_test["Age"].size):
        temp_point = Point(
            habermanclass2_test["Age"][x], habermanclass2_test["Positive"][x]
        )
        list_habermanclass2_test.insert(1, temp_point)

    sop1 = list_habermanclass1_train
    sop2 = list_habermanclass2_train
    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")

    D: DataProcessor = DataProcessor(
        ("Positive", "Negative"), "Haberman", ("Age", "Positive")
    )

    D.plot(ch1, ch2, (30, 90))

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
