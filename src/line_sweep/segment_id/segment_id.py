# pylint: disable=missing-module-docstring
from __future__ import annotations

from src.segment import Segment


class SegmentId:
    """
    Esta classe tem dois propósitos:
        1. Evitar o uso de tuplas, provendo acesso direto aos membros com nomes mais descritivos
        2. Prover um comparador para os elementos da AVL,
        não interferindo com o comparador de segmentos.

        Isso também evita um erro de execução.
    """

    def __init__(self, seg: Segment, identifier: int) -> None:
        self.seg = seg
        self.identifier = identifier
        self.slope = (
            (seg.p1.y - seg.p0.y) / (seg.p1.x - seg.p0.x) if seg.p1.x != seg.p0.x else 0
        )

    def compare(self, other: SegmentId) -> int:
        """
        Comparador usado na AVL
        """
        if self.seg.p0.y < other.seg.p0.y:
            return -1
        if self.seg.p0.y == other.seg.p0.y and self.seg.p0.x < other.seg.p0.x:
            return -1
        if self.seg.p0 == other.seg.p0 and self.slope < other.slope:
            return -1
        if self.seg.p0 == other.seg.p0 and self.seg.p1 == other.seg.p1:
            return 0
        return 1

    def __gt__(self, other: SegmentId) -> bool:
        return self.compare(other) > 0

    def __eq__(self, other: SegmentId) -> bool:
        return self.seg == other.seg and self.identifier == other.identifier

    def __repr__(self):
        return f"<{self.seg}, {self.identifier}>"
