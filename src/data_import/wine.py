import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def pre_process_wine(file) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Pré-processa os dados da `wine`, os dividindo em classes (separáveis).
    """
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

    class1 = wine[wine["Class"] == 1]
    class2 = wine[wine["Class"] == 3]
    class1 = class1[["TotalPhenols", "flavanoids", "Class"]]
    class2 = class2[["TotalPhenols", "flavanoids", "Class"]]

    return class1, class2


def check_wine(file) -> None:
    """Checa se o dataset `wine` é separável."""

    D: DataProcessor = DataProcessor(("1", "3"), "Wine", ("TotalPhenols", "flavanoids"))

    class1, class2 = pre_process_wine(file)

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (0, 4))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull1.convex_hull, hull2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")


def classify_wine(file):
    """
    Simule uma classificação dos dados de `wine`.
    """
    class1, class2 = pre_process_wine(file)

    D: DataProcessor = DataProcessor(("1", "3"), "Wine", ("TotalPhenols", "flavanoids"))

    test_data = D.create_test_data(class1, class2)

    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["Class"] == 1:
            actual.append(1)
        elif row["Class"] == 3:
            actual.append(2)

    D.classify(class1, class2, actual, test_data)
