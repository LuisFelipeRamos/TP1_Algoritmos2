import math
from __future__ import annotations

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __lt__(self, other: Point) -> bool:
        return self.y < other.y if self.y != other.y else self.x < other.x

    def __gt__(self, other: Point) -> bool:
        return self.y > other.y if self.y != other.y else self.x > other.x

    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: Point) -> bool:
        return self.x != other.x or self.y != other.y

    def get_distance(self, other: Point) -> float:
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def is_inside(self, polygon: list) -> bool:
        """Confere se um ponto está dentro de um polígono."""
        crossings: int = 0
        for edge in polygon:
            cond1: bool = edge.p0.x <= self.x and self.x < edge.p1.x
            cond2: bool = edge.p1.x <= self.x and self.x < edge.p0.x
            above: bool = self.y < (edge.slope * (self.x - edge.p0.x) + edge.p0.y)
            if (cond1 or cond2) and above:
                crossings += 1
        return (crossings % 2) != 0

