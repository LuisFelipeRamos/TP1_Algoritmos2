import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def check_banana(file):
    """Checa se o dataset `banana` é separável."""

    col_names_banana = ["At1", "At2", "Class"]
    banana = pd.read_csv(file, names=col_names_banana)

    bananaclass1 = banana[banana["Class"] == 1.0]
    bananaclass2 = banana[banana["Class"] == -1.0]

    D: DataProcessor = DataProcessor(("1", "2"), "Banana", ("At1", "At2"))

    hull_1, hull_2 = D.process(bananaclass1, bananaclass2)

    D.plot(hull_1, hull_2, (-3, 3))

    line_sweep = LineSweep()
    intersect = line_sweep.do_polygons_intersect(hull_1.convex_hull, hull_2.convex_hull)

    # Aqui, a título de exemplo, é checado se uma envoltória está dentro da outra
    # Como esse caso geralmente não acontece, essa checagem foi omitida em outros datasets
    linear_separable = False
    if not intersect:
        linear_separable = not (hull_1.is_inside(hull_2) or hull_2.is_inside(hull_1))
    if not linear_separable:
        print("Os dados não são linearmente separáveis")
