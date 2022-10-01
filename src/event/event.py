from __future__ import annotations

from src.segment import Segment

class Event:
    def __init__(self, x: float, y: float, l: bool, s: Segment) -> None:
        self.x = x
        self.y = y
        self.isLeft = l
        self.segment = s

    def __repr__(self) -> str:
        return f"[({self.x}, {self.y}, {self.isLeft})]"

    def compare(self, other: Event):
        if self.x < other.x:
            return -1
        if self.x == other.x and self.isLeft == True and other.isLeft == False:
            return -1
        if self.x == other.x and self.isLeft == False and other.isLeft == True:
            return 1
        if self.x == other.x and self.y < other.y:
            return -1
        if self.x == other.x and self.y == other.y:
            return 0
        else:
            return 1

    def __lt__(self, other: Event):
        return self.compare(other) < 0

