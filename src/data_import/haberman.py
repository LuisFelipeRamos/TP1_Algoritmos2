import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_haberman(file):
    """Checa se o dataset `haberman` é separável."""

    col_names_haberman = ["Age", "Year", "Positive", "Survival"]
    haberman = pd.read_csv(file, names=col_names_haberman)

    habermanclass1 = haberman[haberman["Survival"] == " positive"]
    habermanclass2 = haberman[haberman["Survival"] == " negative"]
    habermanclass1 = habermanclass1[["Age", "Positive"]]
    habermanclass2 = habermanclass2[["Age", "Positive"]]

    D: DataProcessor = DataProcessor(
        ("Positive", "Negative"), "Haberman", ("Age", "Positive")
    )

    hull_1, hull_2 = D.process(habermanclass1, habermanclass2)

    D.plot(hull_1, hull_2, (30, 90))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull_1.convex_hull, hull_2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
