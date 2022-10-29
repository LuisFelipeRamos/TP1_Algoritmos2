import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_mammographic(file):
    """Checa se o dataset `mammographic` é separável."""

    col_names_mammographic = [
        "BI-RADS",
        "Age",
        "Shape",
        "Margin",
        "Density",
        "Severity",
    ]
    mammographic = pd.read_csv(file, names=col_names_mammographic)

    mammographicclass1 = mammographic[mammographic["Severity"] == 0]
    mammographicclass2 = mammographic[mammographic["Severity"] == 1]
    mammographicclass1 = mammographicclass1[["Age", "Density"]]
    mammographicclass2 = mammographicclass2[["Age", "Density"]]

    D: DataProcessor = DataProcessor(("1", "2"), "Mammographic", ("Age", "Density"))

    hull_1, hull_2 = D.process(mammographicclass1, mammographicclass2)

    D.plot(hull_1, hull_2, (11, 15))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull_1.convex_hull, hull_2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
