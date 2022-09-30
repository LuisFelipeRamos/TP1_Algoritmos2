from __future__ import annotations

from src.point import Point


class Segment:
    def __init__(self, p0: Point, p1: Point) -> None:
        self.p0 = p0
        self.p1 = p1

        self.x = p1.x - p0.x
        self.y = p1.y - p0.y

        self.length = self.p0.get_distance(p1)

    def __repr__(self) -> str:
        return f"<{self.p0}, {self.p1}>"

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
