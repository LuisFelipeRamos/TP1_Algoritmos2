from __future__ import annotations


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __lt__(self, other: Point) -> bool:
        return self.y < other.y if self.y != other.y else self.x < other.x

    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: Point) -> bool:
        return self.x != other.x or self.y != other.y
