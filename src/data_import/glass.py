import pandas as pd

from src.convex_hull.convex_hull import ConvexHull
from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep
from src.point.point import Point


def check_glass(file):

    col_names_glass = ["RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "TypeGlass"]
    glass = pd.read_csv(file, names=col_names_glass)

    glassclass1 = glass[glass["TypeGlass"] == 1]
    glassclass2 = glass[glass["TypeGlass"] == 6]
    glassclass1 = glassclass1[["Na", "Mg"]]
    glassclass2 = glassclass2[["Na", "Mg"]]

    glassclass1_train = glassclass1.sample(frac=0.7)
    glassclass1_test = glassclass1.drop(glassclass1_train.index)
    glassclass1_train.reset_index(drop=True, inplace=True)
    glassclass1_test.reset_index(drop=True, inplace=True)

    glassclass2_train = glassclass2.sample(frac=0.7)
    glassclass2_test = glassclass2.drop(glassclass2_train.index)
    glassclass2_train.reset_index(drop=True, inplace=True)
    glassclass2_test.reset_index(drop=True, inplace=True)

    list_glassclass1_train = []
    for x in range(glassclass1_train["Na"].size):
        temp_point = Point(glassclass1_train["Na"][x], glassclass1_train["Mg"][x])
        list_glassclass1_train.insert(1, temp_point)

    list_glassclass1_test = []
    for x in range(glassclass1_test["Na"].size):
        temp_point = Point(glassclass1_test["Na"][x], glassclass1_test["Mg"][x])
        list_glassclass1_test.insert(1, temp_point)

    list_glassclass2_train = []
    for x in range(glassclass2_train["Na"].size):
        temp_point = Point(glassclass2_train["Na"][x], glassclass2_train["Mg"][x])
        list_glassclass2_train.insert(1, temp_point)

    list_glassclass2_test = []
    for x in range(glassclass2_test["Na"].size):
        temp_point = Point(glassclass2_test["Na"][x], glassclass2_test["Mg"][x])
        list_glassclass2_test.insert(1, temp_point)

    sop1 = list_glassclass1_train
    sop2 = list_glassclass2_train

    ch1 = ConvexHull(sop1, alg="graham_scan")
    ch2 = ConvexHull(sop2, alg="graham_scan")

    D: DataProcessor = DataProcessor(("1", "6"), "Glass", ("Na", "Mg"))

    D.plot(ch1, ch2, (11, 15))

    # checa se os polígonos se intersectam
    line_sweep = LineSweep()

    linear_separable = not line_sweep.do_polygons_intersect(
        ch1.convex_hull, ch2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
