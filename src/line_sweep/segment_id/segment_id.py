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

    def __init__(self, seg: Segment, id: int) -> None:
        self.seg = seg
        self.id = id

    def compare(self, other: SegmentId) -> int:
        """
        Comparador usado na AVL
        """
        if self.seg.p0.y < other.seg.p0.y:
            return -1
        if self.seg.p0 == other.seg.p0 and self.seg.p1.y < other.seg.p1.y:
            return -1
        if self.seg == other.seg:
            return 0
        return 1

    def __gt__(self, other: SegmentId) -> bool:
        return self.compare(other) > 0

    def __eq__(self, other: SegmentId) -> bool:
        return self.seg == other.seg and self.id == other.id

    def __repr__(self):
        return f"<{self.seg}, {self.id}>"
