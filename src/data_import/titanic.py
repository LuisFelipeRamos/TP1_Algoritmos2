import pandas as pd

from src.data_import.data_processor import DataProcessor


def check_titanic(file):
    """Checa se o dataset `titanic` é separável."""

    col_names_titanic = [
        "Class",
        "Age",
        "Sex",
        "Survived",
    ]
    wine = pd.read_csv(file, names=col_names_titanic)

    class1 = wine[wine["Survived"] == 1]
    class2 = wine[wine["Survived"] == -1]
    class1 = class1[["Class", "Age"]]
    class2 = class2[["Class", "Age"]]

    D: DataProcessor = DataProcessor(
        ("Survived", "Didn't Survive"), "Titanic", ("Class", "Age")
    )

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (-2, 2))

    if D.has_intersection(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    # Esses dados não são separáveis. Então não tratamos o caso de eles serem.
