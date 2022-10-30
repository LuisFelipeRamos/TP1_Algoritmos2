import pandas as pd

from src.data_import.data_processor import DataProcessor


def check_banana(file):
    """Checa se o dataset `banana` é separável."""

    D: DataProcessor = DataProcessor(("1", "2"), "Banana", ("At1", "At2"))

    col_names_banana = ["At1", "At2", "Class"]
    banana = pd.read_csv(file, names=col_names_banana)

    class1 = banana[banana["Class"] == 1.0]
    class2 = banana[banana["Class"] == -1.0]

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (-3, 3))

    # Aqui, a título de exemplo, é checado se uma envoltória está dentro da outra
    # Como esse caso geralmente não acontece, essa checagem foi omitida em outros datasets
    linear_separable = False
    if not D.is_separable(hull1, hull2):
        linear_separable = not (hull1.is_inside(hull2) or hull2.is_inside(hull1))
    if not linear_separable:
        print("Os dados não são linearmente separáveis")
    # Esses dados não são separáveis. Então não tratamos o caso de eles serem.
