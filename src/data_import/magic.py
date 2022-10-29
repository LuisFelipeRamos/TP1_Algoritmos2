import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_magic(file):
    """Checa se o dataset `magic` é separável."""

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

    D: DataProcessor = DataProcessor(("g", "h"), "Magic", ("FLength", "FWidth"))

    hull_1, hull_2 = D.process(magicclass1, magicclass2)

    D.plot(hull_1, hull_2, (0, 300))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull_1.convex_hull, hull_2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")
