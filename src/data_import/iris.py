import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_iris(file):

    col_names_iris = ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth", "Class"]
    iris = pd.read_csv(file, names=col_names_iris)

    irisclass1 = iris[iris["Class"] != " Iris-setosa"]
    irisclass2 = iris[iris["Class"] == " Iris-setosa"]
    irisclass1 = irisclass1[["PetalLength", "PetalWidth"]]
    irisclass2 = irisclass2[["PetalLength", "PetalWidth"]]

    irisclass1_train = irisclass1.sample(frac=0.7)
    irisclass1_test = irisclass1.drop(irisclass1_train.index)
    irisclass1_train.reset_index(drop=True, inplace=True)
    irisclass1_test.reset_index(drop=True, inplace=True)

    irisclass2_train = irisclass2.sample(frac=0.7)
    irisclass2_test = irisclass2.drop(irisclass2_train.index)
    irisclass2_train.reset_index(drop=True, inplace=True)
    irisclass2_test.reset_index(drop=True, inplace=True)

    list_irisclass1_train = []
    for x in range(irisclass1_train["PetalLength"].size):
        temp_point = Point(
            irisclass1_train["PetalLength"][x], irisclass1_train["PetalWidth"][x]
        )
        list_irisclass1_train.insert(1, temp_point)

    list_irisclass1_test = []
    for x in range(irisclass1_test["PetalLength"].size):
        temp_point = Point(
            irisclass1_test["PetalLength"][x], irisclass1_test["PetalWidth"][x]
        )
        list_irisclass1_test.insert(1, temp_point)

    list_irisclass2_train = []
    for x in range(irisclass2_train["PetalLength"].size):
        temp_point = Point(
            irisclass2_train["PetalLength"][x], irisclass2_train["PetalWidth"][x]
        )
        list_irisclass2_train.insert(1, temp_point)

    list_irisclass2_test = []
    for x in range(irisclass2_test["PetalLength"].size):
        temp_point = Point(
            irisclass2_test["PetalLength"][x], irisclass2_test["PetalWidth"][x]
        )
        list_irisclass2_test.insert(1, temp_point)

    sop1 = list_irisclass1_train
    sop2 = list_irisclass2_train
    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")

    D: DataProcessor = DataProcessor(
        ("Iris-setosa", "not Iris-setosa"), "Iris", ("PetalLength", "PetalWidth")
    )

    D.plot(ch1, ch2, (1, 4))

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
