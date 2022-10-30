import pandas as pd

from src.data_import.data_processor import DataProcessor


def pre_process_newthyroid(file) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Preprocessa os dados de `newthyroid`, os dividindo em classes (separáveis).
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
    """Checa se o dataset `newthyroid` é separável.
    Se for, suas estatísticas são impressas na tela."""

    D: DataProcessor = DataProcessor(
        ("2", "3"), "Newthyroid", ("Thyroxin", "TSH_value")
    )

    class1, class2 = pre_process_newthyroid(file)

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (0, 10))

    if not D.is_separable(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    else:
        classify_newthyroid(D, class1, class2)


def classify_newthyroid(
    D: DataProcessor, class1: pd.DataFrame, class2: pd.DataFrame
) -> None:
    """
    Simule uma classificação dos dados de `newthyroid`, imprimindo estatísticas no final.
    """
    test_data = D.create_test_data(class1, class2)

    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["Class"] == 2:
            actual.append(1)
        elif row["Class"] == 3:
            actual.append(2)

    D.classify(class1, class2, actual, test_data)
