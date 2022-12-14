import pandas as pd

from src.data_import.data_processor import DataProcessor


def check_haberman(file: str) -> None:
    """Checa se o dataset `haberman` é separável."""
    col_names_haberman = ["Age", "Year", "Positive", "Survival"]
    haberman = pd.read_csv(file, names=col_names_haberman)

    class1 = haberman[haberman["Survival"] == " positive"]
    class2 = haberman[haberman["Survival"] == " negative"]
    class1 = class1[["Age", "Positive"]]
    class2 = class2[["Age", "Positive"]]

    d: DataProcessor = DataProcessor(
        ("Positive", "Negative"), "Haberman", ("Age", "Positive")
    )

    hull1, hull2 = d.process(class1, class2)

    d.plot(hull1, hull2, (30, 90))

    if d.has_intersection(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    # Esses dados não são separáveis. Então não tratamos o caso de eles serem.
