import pandas as pd

from src.data_import.data_processor import DataProcessor
from src.line_sweep.line_sweep import LineSweep


def pre_process_iris(file) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Pré-processa os dados da `iris`, os dividindo em classes (separáveis).
    """
    col_names_iris = ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth", "Class"]
    iris = pd.read_csv(file, names=col_names_iris)

    class1 = iris[iris["Class"] != " Iris-setosa"]
    class2 = iris[iris["Class"] == " Iris-setosa"]
    class1 = class1[["PetalLength", "PetalWidth", "Class"]]
    class2 = class2[["PetalLength", "PetalWidth", "Class"]]

    return class1, class2


def check_iris(file):
    """Checa se o dataset `iris` é separável."""

    D: DataProcessor = DataProcessor(
        ("Iris-setosa", "not Iris-setosa"), "Iris", ("PetalLength", "PetalWidth")
    )

    class1, class2 = pre_process_iris(file)

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (1, 4))

    line_sweep = LineSweep()
    linear_separable = not line_sweep.do_polygons_intersect(
        hull1.convex_hull, hull2.convex_hull
    )

    if not linear_separable:
        print("Os dados não são linearmente separáveis")


def classify_iris(file):
    """
    Simule uma classificação dos dados de `iris`.
    """
    class1, class2 = pre_process_iris(file)

    D: DataProcessor = DataProcessor(
        ("Iris-setosa", "not Iris-setosa"), "Iris", ("PetalLength", "PetalWidth")
    )

    test_data = D.create_test_data(class1, class2)

    # Faz a classificação "correta" dos dados
    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["Class"] == " Iris-setosa":
            actual.append(2)
        else:
            actual.append(1)

    D.classify(class1, class2, actual, test_data)
