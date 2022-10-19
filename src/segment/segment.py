# pylint: disable=missing-module-docstring
from __future__ import annotations

from src.point import Point


class Segment:
    def __init__(self, p0: Point, p1: Point) -> None:
        self.p0 = p0
        self.p1 = p1

        self.x = p1.x - p0.x
        self.y = p1.y - p0.y

        self.slope = (
            (self.p1.y - self.p0.y) / (self.p1.x - self.p0.x)
            if self.p1.x != self.p0.x
            else 0
        )

        self.length = self.p0.get_distance(p1)

    def __repr__(self) -> str:
        return f"[{self.p0}, {self.p1}]"

    def __lt__(self, other: Segment) -> bool:
        return not self.is_counter_clockwise(other)

    def cross_product(self, other: Segment) -> float:
        return self.x * other.y - self.y * other.x

    def is_colinear(self, other: Segment) -> bool:
        return self.cross_product(other) == 0

    def is_counter_clockwise(self, other: Segment) -> bool:
        if self.is_colinear(other):
            return self.length < other.length
        return self.cross_product(other) < 0

    def get_inverse(self):
        return Segment(self.p1, self.p0)

    def invert(self) -> None:
        """
        Inverte os pontos de um segmento
        Não troca outros membros da classe.
        """
        self.p0, self.p1 = self.p1, self.p0

    def contains(self, point: Point) -> bool:
        """
        Confere se um ponto está no intervalo aberto do segmento
        """
        return (
            point.x <= max(self.p0.x, self.p1.x)
            and point.x >= min(self.p0.x, self.p1.x)
            and point.y <= max(self.p0.y, self.p1.y)
            and point.y >= min(self.p0.y, self.p1.y)
        )

    def orientation(self, point: Point) -> int:
        """
        Checa se um ponto é colinear, está orientado no sentido horário ou anti-horário
        """
        key: float = (self.p1.y - self.p0.y) * (point.x - self.p1.x) - (
            self.p1.x - self.p0.x
        ) * (point.y - self.p1.y)
        if key > 0:
            return 1
        if key < 0:
            return -1
        return 0

    def intersects(self, other: Segment) -> bool:
        """
        Confere se um segmento intersecta outro
        """
        d_1: int = self.orientation(other.p0)
        d_2: int = self.orientation(other.p1)
        d_3: int = other.orientation(self.p0)
        d_4: int = other.orientation(self.p1)

        if d_1 != d_2 and d_3 != d_4:
            return True

        if d_1 == 0 and self.contains(other.p0):
            return True

        if d_2 == 0 and self.contains(other.p1):
            return True

        if d_3 == 0 and other.contains(self.p0):
            return True

        if d_4 == 0 and other.contains(self.p1):
            return True

        return False
