import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def pre_process_newthyroid(file) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Pré-processa os dados de `newthyroid`, os dividindo em classes (separáveis).
    """
    col_names_newthyroid = [
        "T3resin",
        "Thyroxin",
        "Triiodothyronine",
        "Thyroidstimulating",
        "TSH_value",
        "Class",
    ]
    newthyroid = pd.read_csv(file, names=col_names_newthyroid)

    class1 = newthyroid[newthyroid["Class"] == 2]
    class2 = newthyroid[newthyroid["Class"] == 3]
    class1 = class1[["Thyroxin", "TSH_value", "Class"]]
    class2 = class2[["Thyroxin", "TSH_value", "Class"]]

    return class1, class2


def check_newthyroid(file) -> None:
    """Checa se o dataset `newthyroid` é separável."""

    D: DataProcessor = DataProcessor(
        ("2", "3"), "Newthyroid", ("Thyroxin", "TSH_value")
    )

    class1, class2 = pre_process_newthyroid(file)

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (0, 10))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull1.convex_hull, hull2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")


def classify_newthyroid(file) -> None:
    """
    Simule uma classificação dos dados de `newthyroid`.
    """
    class1, class2 = pre_process_newthyroid(file)

    D: DataProcessor = DataProcessor(
        ("2", "3"), "Newthyroid", ("Thyroxin", "TSH_value")
    )

    test_data = D.create_test_data(class1, class2)

    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["Class"] == 2:
            actual.append(1)
        elif row["Class"] == 3:
            actual.append(2)

    D.classify(class1, class2, actual, test_data)
