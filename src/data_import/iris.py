import pandas as pd

from src.data_import.data_processor import DataProcessor


def pre_process_iris(file: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Preprocessa os dados da `iris`, os dividindo em classes (separáveis)."""
    col_names_iris = ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth", "Class"]
    iris = pd.read_csv(file, names=col_names_iris)

    class1 = iris[iris["Class"] != " Iris-setosa"]
    class2 = iris[iris["Class"] == " Iris-setosa"]
    class1 = class1[["PetalLength", "PetalWidth", "Class"]]
    class2 = class2[["PetalLength", "PetalWidth", "Class"]]

    return class1, class2


def check_iris(file: str) -> None:
    """
    Checa se o dataset `iris` é separável.

    Se for, suas estatísticas são impressas na tela.
    """
    d: DataProcessor = DataProcessor(
        ("Iris-setosa", "not Iris-setosa"), "Iris", ("PetalLength", "PetalWidth")
    )

    class1, class2 = pre_process_iris(file)

    hull1, hull2 = d.process(class1, class2)

    d.plot(hull1, hull2, (1, 4))

    if d.has_intersection(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    else:
        classify_iris(d, class1, class2)


def classify_iris(d: DataProcessor, class1: pd.DataFrame, class2: pd.DataFrame) -> None:
    """Simule uma classificação dos dados de `iris`, imprimindo estatísticas no final."""
    test_data: pd.DataFrame = d.create_test_data(class1, class2)

    # Faz a classificação "correta" dos dados
    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["Class"] == " Iris-setosa":
            actual.append(2)
        else:
            actual.append(1)

    d.classify(class1, class2, actual, test_data)
