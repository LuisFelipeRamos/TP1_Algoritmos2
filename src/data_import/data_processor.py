from typing import cast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from src.convex_hull import ConvexHull
from src.point import Point
from src.segment import Segment


class DataProcessor:
    """Abstrai atvidades comuns no processamento de dados."""

    def __init__(
        self, classes: tuple[str, str], title: str, axes: tuple[str, str]
    ) -> None:
        self.class_1 = classes[0]
        self.class_2 = classes[1]

        self.title = title

        self.x_axes = axes[0]
        self.y_axes = axes[1]

    def split_df(self, df: pd.DataFrame) -> tuple:
        """Divide um dataframe `df` em dados de treino e de teste."""
        train, test = train_test_split(df, test_size=0.3)
        return train, test

    def create_point_list(self, df: pd.DataFrame) -> list[Point]:
        """Cria uma lista de pontos com base nos eixos escolhidos"""
        point_list: list[Point] = []
        for _, j in df.iterrows():
            aux: Point = Point(j[self.x_axes], j[self.y_axes])
            point_list.append(aux)
        return point_list

    def process(
        self, first_class: pd.DataFrame, second_class: pd.DataFrame
    ) -> tuple[ConvexHull, ConvexHull]:
        """Transforma dataframes com as colunas desejadas em envoltórias convexas."""
        class1_train, _ = self.split_df(first_class)
        class2_train, _ = self.split_df(second_class)

        point1_train: list[Point] = self.create_point_list(class1_train)
        point2_train: list[Point] = self.create_point_list(class2_train)

        hull_1: ConvexHull = ConvexHull(point1_train, alg="graham_scan")
        hull_2: ConvexHull = ConvexHull(point2_train, alg="graham_scan")

        return hull_1, hull_2

    def plot(self, ch1: ConvexHull, ch2: ConvexHull, space: tuple[int, int]) -> None:
        """Imprime conjunto de dados em arquivo `self.title`"""
        min_dist_segment: Segment = ch1.min_dist(ch2)

        _, ax = plt.subplots()
        ax = cast(plt.Axes, ax)

        ax.scatter(
            [point.x for point in ch1.set_of_points],
            [point.y for point in ch1.set_of_points],
            c=["red"],
            s=2,
            label="Class " + self.class_1,
        )
        ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
        for edge in ch1.convex_hull:
            plt.plot(
                [edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "red", linewidth=0.5
            )

        ax.scatter(
            [point.x for point in ch2.set_of_points],
            [point.y for point in ch2.set_of_points],
            c=["blue"],
            s=2,
            label="Class " + self.class_2,
        )
        for edge in ch2.convex_hull:
            plt.plot(
                [edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "blue", linewidth=0.5
            )

        plt.plot(
            [min_dist_segment.p0.x, min_dist_segment.p1.x],
            [min_dist_segment.p0.y, min_dist_segment.p1.y],
            "black",
            linewidth=0.8,
        )

        slope, b, _ = min_dist_segment.get_perpendicular_segment()
        x = np.linspace(space[0], space[1], 100)
        if slope != np.Inf:
            y = slope * x + b
            plt.plot(
                x, y, color="green", label=f"y = {round(slope, 2)}x + {round(b, 2)}"
            )
        else:
            plt.axvline(x=b, color="green", label=f"x = {round(b,2)}")
        plt.title(self.title, color="black")
        plt.xlabel(self.x_axes, color="black")
        plt.xticks()
        plt.ylabel(self.y_axes, color="black")
        plt.yticks()
        plt.legend(loc="upper right", labelcolor="black")
        plt.savefig(self.title.lower() + ".png")
