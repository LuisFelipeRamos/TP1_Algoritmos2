import pandas as pd

from src.data_import.data_processor import DataProcessor


def check_mammographic(file):
    """Checa se o dataset `mammographic` é separável."""

    col_names_mammographic = [
        "BI-RADS",
        "Age",
        "Shape",
        "Margin",
        "Density",
        "Severity",
    ]
    mammographic = pd.read_csv(file, names=col_names_mammographic)

    class1 = mammographic[mammographic["Severity"] == 0]
    class2 = mammographic[mammographic["Severity"] == 1]
    class1 = class1[["Age", "Density"]]
    class2 = class2[["Age", "Density"]]

    D: DataProcessor = DataProcessor(("1", "2"), "Mammographic", ("Age", "Density"))

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (11, 15))

    if D.has_intersection(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    # Esses dados não são separáveis. Então não tratamos o caso de eles serem.
