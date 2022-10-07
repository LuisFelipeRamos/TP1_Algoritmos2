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

    def __gt__(self, other: SegmentId) -> bool:
        """
        Comparador usado na AVL
        y do primeiro ponto (ponto da esquerda)
        """
        return self.seg.p0.y > other.seg.p0.y

    def __repr__(self):
        return f"<{self.seg}, {self.id}>"
