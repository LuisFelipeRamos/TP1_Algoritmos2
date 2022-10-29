import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_wine(file):

    col_names_wine = [
        "Alcohol",
        "MalicAcid",
        "Ash",
        "AlcalinityOfAsh",
        "Magnesium",
        "TotalPhenols",
        "flavanoids",
        "NonflavanoidsPhenols",
        "Proanthocyanins",
        "ColorIntensity",
        "Hue",
        "OD280/OD315",
        "Proline",
        "Class",
    ]
    wine = pd.read_csv(file, names=col_names_wine)

    wineclass1 = wine[wine["Class"] == 1]
    wineclass2 = wine[wine["Class"] == 3]
    wineclass1 = wineclass1[["TotalPhenols", "flavanoids"]]
    wineclass2 = wineclass2[["TotalPhenols", "flavanoids"]]

    wineclass1_train = wineclass1.sample(frac=0.7)
    wineclass1_test = wineclass1.drop(wineclass1_train.index)
    wineclass1_train.reset_index(drop=True, inplace=True)
    wineclass1_test.reset_index(drop=True, inplace=True)

    wineclass2_train = wineclass2.sample(frac=0.7)
    wineclass2_test = wineclass2.drop(wineclass2_train.index)
    wineclass2_train.reset_index(drop=True, inplace=True)
    wineclass2_test.reset_index(drop=True, inplace=True)

    list_wineclass1_train = []
    for x in range(wineclass1_train["TotalPhenols"].size):
        temp_point = Point(
            wineclass1_train["TotalPhenols"][x], wineclass1_train["flavanoids"][x]
        )
        list_wineclass1_train.insert(1, temp_point)

    list_wineclass1_test = []
    for x in range(wineclass1_test["TotalPhenols"].size):
        temp_point = Point(
            wineclass1_test["TotalPhenols"][x], wineclass1_test["flavanoids"][x]
        )
        list_wineclass1_test.insert(1, temp_point)

    list_wineclass2_train = []
    for x in range(wineclass2_train["TotalPhenols"].size):
        temp_point = Point(
            wineclass2_train["TotalPhenols"][x], wineclass2_train["flavanoids"][x]
        )
        list_wineclass2_train.insert(1, temp_point)

    list_wineclass2_test = []
    for x in range(wineclass2_test["TotalPhenols"].size):
        temp_point = Point(
            wineclass2_test["TotalPhenols"][x], wineclass2_test["flavanoids"][x]
        )
        list_wineclass2_test.insert(1, temp_point)

    sop1 = list_wineclass1_train
    sop2 = list_wineclass2_train

    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")

    D: DataProcessor = DataProcessor(("1", "3"), "Wine", ("TotalPhenols", "flavanoids"))

    D.plot(ch1, ch2, (0, 4))

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
