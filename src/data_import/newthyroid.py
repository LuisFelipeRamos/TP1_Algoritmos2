import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_newthyroid(file):
    """Checa se o dataset `newthyroid` é separável."""

    col_names_newthyroid = [
        "T3resin",
        "Thyroxin",
        "Triiodothyronine",
        "Thyroidstimulating",
        "TSH_value",
        "Class",
    ]
    newthyroid = pd.read_csv(file, names=col_names_newthyroid)

    newthyroidclass1 = newthyroid[newthyroid["Class"] == 2]
    newthyroidclass2 = newthyroid[newthyroid["Class"] == 3]
    newthyroidclass1 = newthyroidclass1[["Thyroxin", "TSH_value"]]
    newthyroidclass2 = newthyroidclass2[["Thyroxin", "TSH_value"]]

    D: DataProcessor = DataProcessor(
        ("2", "3"), "Newthyroid", ("Thyroxin", "TSH_value")
    )

    hull_1, hull_2 = D.process(newthyroidclass1, newthyroidclass2)

    D.plot(hull_1, hull_2, (0, 10))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull_1.convex_hull, hull_2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
