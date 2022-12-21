import pandas as pd

from src.data_import.data_processor import DataProcessor


def pre_process_wine(file: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Preprocessa os dados da `wine`, os dividindo em classes (separáveis)."""
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


def check_wine(file: str) -> None:
    """
    Checa se o dataset `wine` é separável.

    Se for, suas estatísticas são impressas na tela.
    """
    d: DataProcessor = DataProcessor(("1", "3"), "Wine", ("TotalPhenols", "flavanoids"))

    class1, class2 = pre_process_wine(file)

    hull1, hull2 = d.process(class1, class2)

    d.plot(hull1, hull2, (0, 4))

    if d.has_intersection(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    else:
        classify_wine(d, class1, class2)


def classify_wine(d: DataProcessor, class1: pd.DataFrame, class2: pd.DataFrame) -> None:
    """Simule uma classificação dos dados de `wine`, imprimindo estatísticas no final."""
    test_data: pd.DataFrame = d.create_test_data(class1, class2)

    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["Class"] == 1:
            actual.append(1)
        elif row["Class"] == 3:
            actual.append(2)

    d.classify(class1, class2, actual, test_data)
