import argparse

from src.data_import import *


def run() -> None:
    """
    Roda o programa principal.
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Recebe arquivos .dat para checar se são linearmente separáveis"
    )
    parser.add_argument(
        "--file",
        dest="file",
        required=False,
        type=str,
        help="arquivo .dat que contêm dados a serem treinados",
    )
    args: argparse.Namespace = parser.parse_args()
