import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_titanic(file):
    """Checa se o dataset `titanic` é separável."""

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

    D: DataProcessor = DataProcessor(
        ("Survived", "Didn't Survive"), "Titanic", ("Class", "Age")
    )

    hull_1, hull_2 = D.process(titanicclass1, titanicclass2)

    D.plot(hull_1, hull_2, (-2, 2))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull_1.convex_hull, hull_2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
