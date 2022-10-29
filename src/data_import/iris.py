import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_iris(file):
    """Checa se o dataset `iris` é separável."""

    col_names_iris = ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth", "Class"]
    iris = pd.read_csv(file, names=col_names_iris)

    irisclass1 = iris[iris["Class"] != " Iris-setosa"]
    irisclass2 = iris[iris["Class"] == " Iris-setosa"]
    irisclass1 = irisclass1[["PetalLength", "PetalWidth"]]
    irisclass2 = irisclass2[["PetalLength", "PetalWidth"]]

    D: DataProcessor = DataProcessor(
        ("Iris-setosa", "not Iris-setosa"), "Iris", ("PetalLength", "PetalWidth")
    )

    hull_1, hull_2 = D.process(irisclass1, irisclass2)

    D.plot(hull_1, hull_2, (1, 4))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull_1.convex_hull, hull_2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
