# pylint: disable=missing-module-docstring
from __future__ import annotations

import src.line_sweep.glob as gb
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

    def compare(self, other: SegmentId) -> int:
        """
        Comparador usado na AVL
        """
        y_self = self.seg.slope * gb.xxx + self.seg.linear
        y_other = other.seg.slope * gb.xxx + other.seg.linear
        return y_self < y_other

    def __gt__(self, other: SegmentId) -> bool:
        return self.compare(other) > 0

    def __eq__(self, other: SegmentId) -> bool:
        return self.seg == other.seg and self.identifier == other.identifier

    def __repr__(self):
        return f"<{self.seg}, {self.identifier}>"
