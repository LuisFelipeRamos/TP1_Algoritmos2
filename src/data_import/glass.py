import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_glass(file):
    """Checa se o dataset `glass` é separável."""

    col_names_glass = ["RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "TypeGlass"]
    glass = pd.read_csv(file, names=col_names_glass)

    glassclass1 = glass[glass["TypeGlass"] == 1]
    glassclass2 = glass[glass["TypeGlass"] == 6]
    glassclass1 = glassclass1[["Na", "Mg"]]
    glassclass2 = glassclass2[["Na", "Mg"]]

    D: DataProcessor = DataProcessor(("1", "6"), "Glass", ("Na", "Mg"))

    hull_1, hull_2 = D.process(glassclass1, glassclass2)

    D.plot(hull_1, hull_2, (11, 15))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull_1.convex_hull, hull_2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
