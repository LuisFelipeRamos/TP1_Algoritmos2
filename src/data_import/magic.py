import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_magic(file):

    col_names_magic = [
        "FLength",
        "FWidth",
        "FSize",
        "FConc",
        "FConc1",
        "FAsym",
        "FM3Long",
        "FM3Trans",
        "FAlpha",
        "FDist",
        "Class",
    ]
    magic = pd.read_csv(file, names=col_names_magic)

    magicclass1 = magic[magic["Class"] == "g"]
    magicclass2 = magic[magic["Class"] == "h"]
    magicclass1 = magicclass1[["FLength", "FWidth"]]
    magicclass2 = magicclass2[["FLength", "FWidth"]]

    magicclass1_train = magicclass1.sample(frac=0.7)
    magicclass1_test = magicclass1.drop(magicclass1_train.index)
    magicclass1_train.reset_index(drop=True, inplace=True)
    magicclass1_test.reset_index(drop=True, inplace=True)

    magicclass2_train = magicclass2.sample(frac=0.7)
    magicclass2_test = magicclass2.drop(magicclass2_train.index)
    magicclass2_train.reset_index(drop=True, inplace=True)
    magicclass2_test.reset_index(drop=True, inplace=True)

    list_magicclass1_train = []
    for x in range(magicclass1_train["FLength"].size):
        temp_point = Point(
            magicclass1_train["FLength"][x], magicclass1_train["FWidth"][x]
        )
        list_magicclass1_train.insert(1, temp_point)

    list_magicclass1_test = []
    for x in range(magicclass1_test["FLength"].size):
        temp_point = Point(
            magicclass1_test["FLength"][x], magicclass1_test["FWidth"][x]
        )
        list_magicclass1_test.insert(1, temp_point)

    list_magicclass2_train = []
    for x in range(magicclass2_train["FLength"].size):
        temp_point = Point(
            magicclass2_train["FLength"][x], magicclass2_train["FWidth"][x]
        )
        list_magicclass2_train.insert(1, temp_point)

    list_magicclass2_test = []
    for x in range(magicclass2_test["FLength"].size):
        temp_point = Point(
            magicclass2_test["FLength"][x], magicclass2_test["FWidth"][x]
        )
        list_magicclass2_test.insert(1, temp_point)

    sop1 = list_magicclass1_train
    sop2 = list_magicclass2_train
    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")

    D: DataProcessor = DataProcessor(("g", "h"), "Magic", ("FLength", "FWidth"))

    D.plot(ch1, ch2, (0, 300))

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
