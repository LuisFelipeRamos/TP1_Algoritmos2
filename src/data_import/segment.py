import pandas as pd

from src.data_import.data_processor import DataProcessor


def pre_process_segment(file: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Preprocessa os dados de `segment`, os dividindo em classes (separáveis)."""
    col_names_segment = [
        "Region-centroid-col",
        "Region-centroid-row",
        "Region-pixel-count",
        "Short-line-density-5",
        "Short-line-density-2",
        "Vedge-mean",
        "Vegde-sd",
        "Hedge-mean",
        "Hedge-sd",
        "Intensity-mean",
        "Rawred-mean",
        "Rawblue-mean",
        "Rawgreen-mean",
        "Exred-mean",
        "Exblue-mean",
        "Exgreen-mean",
        "Value-mean",
        "Saturatoin-mean",
        "Hue-mean",
        "Class",
    ]
    segment = pd.read_csv(file, names=col_names_segment)

    class1 = segment[segment["Class"] == 1]
    class2 = segment[segment["Class"] == 2]
    class1 = class1[["Region-centroid-col", "Rawblue-mean", "Class"]]
    class2 = class2[["Region-centroid-col", "Rawblue-mean", "Class"]]

    return class1, class2


def check_segment(file: str) -> None:
    """
    Checa se o dataset `segment` é separável.

    Se for, suas estatísticas são impressas na tela.
    """
    d: DataProcessor = DataProcessor(
        ("1", "2"), "Segment", ("Region-centroid-col", "Rawblue-mean")
    )

    class1, class2 = pre_process_segment(file)

    hull1, hull2 = d.process(class1, class2)

    d.plot(hull1, hull2, (10, 300))

    if d.has_intersection(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    else:
        classify_segment(d, class1, class2)


def classify_segment(
    d: DataProcessor, class1: pd.DataFrame, class2: pd.DataFrame
) -> None:
    """Simule uma classificação dos dados de `segment`, imprimindo estatísticas no final."""
    test_data = d.create_test_data(class1, class2)

    actual: list[int] = []
    for _, row in test_data.iterrows():
        if row["Class"] == 1:
            actual.append(1)
        elif row["Class"] == 2:
            actual.append(2)

    d.classify(class1, class2, actual, test_data)
