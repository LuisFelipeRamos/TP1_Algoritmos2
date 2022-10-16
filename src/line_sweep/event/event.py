from __future__ import annotations

from src.point.point import Point
from src.segment import Segment


class Event:
    """
    Esta classe tem dois propósitos:
        1. Evitar o uso de tuplas, provendo acesso direto aos membros com nomes mais descritivos
        2. Prover um comparador para os eventos, levando em consideração coordenadas e orientação
    """

    def __init__(self, point: Point, left: bool, seg: Segment, i: int = -1) -> None:
        self.x = point.x
        self.y = point.y
        self.is_left = left
        self.segment = seg
        self.identifier = i

    def __repr__(self) -> str:
        return f"[({self.x}, {self.y}, {self.is_left})]"

    def compare(self, other: Event) -> int:
        """
        Compare inicialmente pelo X,
        use orientação como critério de desempate (esquerda é menor),
        use y como segundo critério de desempate
        """
        if self.x < other.x:
            return -1
        if self.x == other.x and self.is_left is True and other.is_left is False:
            return -1
        if self.x == other.x and self.is_left is False and other.is_left is True:
            return 1
        if self.x == other.x and self.y < other.y:
            return -1
        if self.x == other.x and self.y == other.y:
            return 0
        return 1

    def __lt__(self, other: Event) -> bool:
        return self.compare(other) < 0
