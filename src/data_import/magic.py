import pandas as pd

from src.data_import.data_processor import DataProcessor


def check_magic(file):
    """Checa se o dataset `magic` é separável."""

    col_names_magic = [
        "FLength",
        "FWidth",
        "FSize",
        "FConc",
        "FConc1",
        "FAsym",
        "FM3Long",
        "FM3Trans",
        "FAlpha",
        "FDist",
        "Class",
    ]
    magic = pd.read_csv(file, names=col_names_magic)

    class1 = magic[magic["Class"] == "g"]
    class2 = magic[magic["Class"] == "h"]
    class1 = class1[["FLength", "FWidth"]]
    class2 = class2[["FLength", "FWidth"]]

    D: DataProcessor = DataProcessor(("g", "h"), "Magic", ("FLength", "FWidth"))

    hull1, hull2 = D.process(class1, class2)

    D.plot(hull1, hull2, (0, 300))

    if not D.is_separable(hull1, hull2):
        print("Os dados não são linearmente separáveis")
    # Esses dados não são separáveis. Então não tratamos o caso de eles serem.
