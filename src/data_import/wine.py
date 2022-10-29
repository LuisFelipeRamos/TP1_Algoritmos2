import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_wine(file):
    """Checa se o dataset `wine` é separável."""

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

    D: DataProcessor = DataProcessor(("1", "3"), "Wine", ("TotalPhenols", "flavanoids"))

    hull_1, hull_2 = D.process(wineclass1, wineclass2)

    D.plot(hull_1, hull_2, (0, 4))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull_1.convex_hull, hull_2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
