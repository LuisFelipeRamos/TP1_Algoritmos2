import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def pre_process_glass(file) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Pré-processa os dados da `glass`, os dividindo em classes (separáveis).
    """

    col_names_glass = ["RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "TypeGlass"]
    glass = pd.read_csv(file, names=col_names_glass)

    class1 = glass[glass["TypeGlass"] == 1]
    class2 = glass[glass["TypeGlass"] == 6]
    class1 = class1[["Na", "Mg", "TypeGlass"]]
    class2 = class2[["Na", "Mg", "TypeGlass"]]

    return class1, class2


def check_glass(file):
    """Checa se o dataset `glass` é separável."""

    D: DataProcessor = DataProcessor(("1", "6"), "Glass", ("Na", "Mg"))

    class1, class2 = pre_process_glass(file)

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (11, 15))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull1.convex_hull, hull2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")


def classify_glass(file):
    """
    Simule uma classificação dos dados de `glass`.
    """
    class1, class2 = pre_process_glass(file)

    D: DataProcessor = DataProcessor(("1", "6"), "Glass", ("Na", "Mg"))

    test_data = D.create_test_data(class1, class2)

    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["TypeGlass"] == 1:
            actual.append(1)
        elif row["TypeGlass"] == 6:
            actual.append(2)

    D.classify(class1, class2, actual, test_data)
