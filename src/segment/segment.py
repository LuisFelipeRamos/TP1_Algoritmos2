from __future__ import annotations

from src.point import Point


class Segment:
    def __init__(self, p0: Point, p1: Point, id: int = 0) -> None:
        self.p0 = p0
        self.p1 = p1

        self.x = p1.x - p0.x
        self.y = p1.y - p0.y

        self.length = self.p0.get_distance(p1)
        # Compare pontos de polígonos diferentes
        self.pol_id = id

    def __repr__(self) -> str:
        return f"<{self.p0}, {self.p1}>"

    def __lt__(self, other: Segment) -> bool:
        return not self.is_counter_clockwise(other)

    # Compare pelo y do primeiro ponto na AVL
    def __gt__(self, other: Segment) -> bool:
        return self.p0.y > other.p0.y

    def cross_product(self, other: Segment) -> float:
        return self.x * other.y - self.y * other.x

    def is_colinear(self, other: Segment) -> bool:
        return self.cross_product(other) == 0

    def is_counter_clockwise(self, other: Segment) -> bool:
        if self.is_colinear(other):
            return self.length < other.length
        return self.cross_product(other) < 0

    def invert(self) -> None:
        temp: Point = self.p0
        self.p0 = self.p1
        self.p1 = temp

    def contains(self, p: Point) -> bool:
        return (
            p.x < max(self.p0.x, self.p1.x)
            and p.x > min(self.p0.x, self.p1.x)
            and p.y < max(self.p0.y, self.p1.y)
            and p.y > min(self.p0.y, self.p1.y)
        )

    def orientation(self, p: Point) -> int:
        key: float = (self.p1.y - self.p0.y) * (p.x - self.p1.x) - (
            self.p1.x - self.p0.x
        ) * (p.y - self.p1.y)
        if key > 0:
            return 1
        elif key < 0:
            return -1
        else:
            return 0

    def intersects(self, other: Segment) -> bool:
        # Quando estamos no mesmo polígono, podemos compartilhar um ponto
        if self.pol_id == other.pol_id:
            if (
                self.p0 == other.p0
                and self.p1 != other.p1
                or self.p0 == other.p1
                and self.p1 != other.p0
            ):
                return False
            if (
                self.p1 == other.p1
                and self.p0 != other.p0
                or self.p1 == other.p0
                and self.p0 != other.p1
            ):
                return False

        # Quando o segmento repete ele se intercepta
        if self == other:
            return True

        d1: int = self.orientation(other.p0)
        d2: int = self.orientation(other.p1)
        d3: int = other.orientation(self.p0)
        d4: int = other.orientation(self.p1)

        if d1 != d2 and d3 != d4:
            return True

        if d1 == 0 and self.contains(other.p0):
            return True

        if d2 == 0 and self.contains(other.p1):
            return True

        if d3 == 0 and other.contains(self.p0):
            return True

        if d4 == 0 and other.contains(self.p1):
            return True

        return False
