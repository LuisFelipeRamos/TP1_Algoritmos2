from __future__ import annotations
from point import Point

class Segment:
    def __init__(self, p0: Point, p1: Point) -> None:
        self.points = p0, p1
        """ ver nome melhor pra esses atributos aqui embaixo"""
        self.x = p1.x - p0.x
        self.y = p1.y - p0.y

    def __str__(self) -> str:
        return f"<{self.points[0]}, {self.points[1]}>"

    def cross_product(self, s: Segment) -> float:
        return self.x * s.y - self.y * s.x

    def is_counter_clockwise(self, s: Segment) -> bool:
        return self.cross_product(s) < 0
