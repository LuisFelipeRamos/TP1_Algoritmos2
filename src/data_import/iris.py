import pandas as pd

from src.data_import.data_processor import DataProcessor


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


def check_iris(file) -> None:
    """Checa se o dataset `iris` é separável."""

    D: DataProcessor = DataProcessor(
        ("Iris-setosa", "not Iris-setosa"), "Iris", ("PetalLength", "PetalWidth")
    )

    class1, class2 = pre_process_iris(file)

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (1, 4))

    if not D.is_separable(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    else:
        classify_iris(D, class1, class2)


def classify_iris(D: DataProcessor, class1: pd.DataFrame, class2: pd.DataFrame) -> None:
    """
    Simule uma classificação dos dados de `iris`, imprimindo estatísticas no final.
    """
    test_data: pd.DataFrame = D.create_test_data(class1, class2)

    # Faz a classificação "correta" dos dados
    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["Class"] == " Iris-setosa":
            actual.append(2)
        else:
            actual.append(1)

    D.classify(class1, class2, actual, test_data)
