import argparse

import src.globals as g
from src.data_import import (
    check_banana,
    check_glass,
    check_haberman,
    check_iris,
    check_magic,
    check_mammographic,
    check_newthyroid,
    check_segment,
    check_titanic,
    check_wine,
)


def run() -> None:
    """
    Roda o programa principal: analisa um dataset, gerando seu gráfico (em ./images)
    e imprimindo suas métricas se for separável ou imprimindo que não é separável.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Recebe o nome do dataset que será checado."
    )
    parser.add_argument(
        "--data",
        dest="data",
        required=False,
        type=str,
        help="Dataset que será checado",
    )
    args: argparse.Namespace = parser.parse_args()

    if args.data == g.BANANA:
        check_banana("data/banana.dat")
    elif args.data == g.GLASS:
        check_glass("data/glass.dat")
    elif args.data == g.HABERMAN:
        check_haberman("data/haberman.dat")
    elif args.data == g.IRIS:
        check_iris("data/iris.dat")
    elif args.data == g.MAGIC:
        check_magic("data/magic.dat")
    elif args.data == g.MAMMOGRAPHIC:
        check_mammographic("data/mammographic.dat")
    elif args.data == g.NEWTHYROID:
        check_newthyroid("data/newthyroid.dat")
    elif args.data == g.SEGMENT:
        check_segment("data/segment.dat")
    elif args.data == g.TITANIC:
        check_titanic("data/titanic.dat")
    elif args.data == g.WINE:
        check_wine("data/wine.dat")
    else:
        print("Esse dataset não existe no nosso trabalho!")
