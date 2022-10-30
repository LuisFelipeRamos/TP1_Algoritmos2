import pandas as pd

from src.data_import.data_processor import DataProcessor


def pre_process_glass(file) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Preprocessa os dados da `glass`, os dividindo em classes (separáveis).
    """

    col_names_glass = ["RI", "Na", "Mg", "Al", "Si", "K", "Ca", "Ba", "Fe", "TypeGlass"]
    glass = pd.read_csv(file, names=col_names_glass)

    class1 = glass[glass["TypeGlass"] == 1]
    class2 = glass[glass["TypeGlass"] == 6]
    class1 = class1[["Na", "Mg", "TypeGlass"]]
    class2 = class2[["Na", "Mg", "TypeGlass"]]

    return class1, class2


def check_glass(file) -> None:
    """Checa se o dataset `glass` é separável.
    Se for, suas estatísticas são impressas na tela."""

    D: DataProcessor = DataProcessor(("1", "6"), "Glass", ("Na", "Mg"))

    class1, class2 = pre_process_glass(file)

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (11, 15))

    if not D.is_separable(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    else:
        classify_glass(D, class1, class2)


def classify_glass(
    D: DataProcessor, class1: pd.DataFrame, class2: pd.DataFrame
) -> None:
    """
    Simule uma classificação dos dados de `glass`, imprimindo estatísticas no final.
    """
    test_data = D.create_test_data(class1, class2)

    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["TypeGlass"] == 1:
            actual.append(1)
        elif row["TypeGlass"] == 6:
            actual.append(2)

    D.classify(class1, class2, actual, test_data)
