# pylint: disable=missing-function-docstring, missing-module-docstring
from src.line_sweep import LineSweep
from src.line_sweep.lib.avl_tree import AVLTree
from src.point import Point
from src.segment import Segment


def test_polygons_intersect() -> None:
    L: LineSweep = LineSweep()

    A: Point = Point(1, 1)
    B: Point = Point(4, 4)
    C: Point = Point(3, 2)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
        Segment(C, A),
    ]
    D: Point = Point(3, 2.5)
    E: Point = Point(6, 3)
    F: Point = Point(6.5, 0.5)
    pol2: list[Segment] = [
        Segment(D, E),
        Segment(E, F),
        Segment(F, D),
    ]
    assert L.do_polygons_intersect(pol1, pol2)

    # Ponto em comum em dois "polígonos" diferentes (no caso linhas, para simplificar)
    pol1: list[Segment] = [Segment(A, B)]
    pol2: list[Segment] = [Segment(B, F)]
    assert L.do_polygons_intersect(pol1, pol2)


def test_polygons_intersect_pt2() -> None:
    L: LineSweep = LineSweep()

    A: Point = Point(1, 1)
    B: Point = Point(4, 4)
    C: Point = Point(3, 2)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
        Segment(C, A),
    ]
    D: Point = Point(3.5, 2.5)
    E: Point = Point(6, 3)
    F: Point = Point(6.5, 0.5)
    pol2: list[Segment] = [
        Segment(D, E),
        Segment(E, F),
        Segment(F, D),
    ]
    assert not L.do_polygons_intersect(pol1, pol2)


def test_polygons_intersect_pt3() -> None:
    L: LineSweep = LineSweep()

    A: Point = Point(1, 7)
    B: Point = Point(3, 1)
    C: Point = Point(10, 1)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
        Segment(C, A),
    ]
    D: Point = Point(6, 8)
    E: Point = Point(7, 7)
    F: Point = Point(9, 9)
    pol2: list[Segment] = [
        Segment(D, E),
        Segment(E, F),
        Segment(F, D),
    ]
    assert not L.do_polygons_intersect(pol1, pol2)


def test_polygons_intersect_pt4() -> None:
    L: LineSweep = LineSweep()

    A: Point = Point(9, 7)
    B: Point = Point(3, 1)
    C: Point = Point(5, 8)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
    ]

    D: Point = Point(4, 4)
    E: Point = Point(10, 3)
    F: Point = Point(9, 4)
    pol2: list[Segment] = [
        Segment(D, E),
        Segment(F, D),
    ]

    assert L.do_polygons_intersect(pol1, pol2)


def test_polygons_intersect_pt5() -> None:
    L: LineSweep = LineSweep()

    A: Point = Point(2, 9)
    B: Point = Point(10, 11)
    C: Point = Point(10, 4)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(A, C),
    ]

    D: Point = Point(4, 2)
    F: Point = Point(9, 6)
    pol2: list[Segment] = [
        Segment(F, D),
    ]

    assert L.do_polygons_intersect(pol1, pol2)


def test_polygons_intersect_pt6() -> None:
    L: LineSweep = LineSweep()

    A: Point = Point(4, 6)
    B: Point = Point(8, 5)
    C: Point = Point(1, 4)
    pol1: list[Segment] = [Segment(A, B), Segment(B, C)]

    D: Point = Point(5, 3)
    E: Point = Point(9, 5)
    F: Point = Point(9, 7)
    pol2: list[Segment] = [Segment(D, E), Segment(F, D)]

    assert L.do_polygons_intersect(pol1, pol2)


def test_polygons_intersect_pt7() -> None:
    L: LineSweep = LineSweep()

    A: Point = Point(3, 10)
    B: Point = Point(6, 10)
    C: Point = Point(8, 5)
    pol1: list[Segment] = [Segment(A, B), Segment(C, A)]

    D: Point = Point(8, 2)
    E: Point = Point(10, 5)
    F: Point = Point(3, 6)
    pol2: list[Segment] = [Segment(D, F), Segment(F, E)]

    assert L.do_polygons_intersect(pol1, pol2)


def test_polygons_intersect_pt8() -> None:
    L: LineSweep = LineSweep()

    A: Point = Point(4, 7)
    B: Point = Point(7, 1)
    C: Point = Point(5, 4)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(A, C),
    ]

    E: Point = Point(10, 7)
    F: Point = Point(2, 7)
    pol2: list[Segment] = [
        Segment(E, F),
    ]

    assert L.do_polygons_intersect(pol1, pol2)


def test_polygons_intersect_pt9() -> None:

    L: LineSweep = LineSweep()

    A: Point = Point(10, 4)
    B: Point = Point(2, 10)
    C: Point = Point(9, 7)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
    ]

    D: Point = Point(7, 7)
    E: Point = Point(5, 9)
    pol2: list[Segment] = [
        Segment(D, E),
    ]

    assert L.do_polygons_intersect(pol1, pol2)


def test_polygons_intersect_pt10() -> None:
    # Polígonos "de um lado só",
    # colineares e que compartilham o mesmo ponto

    L: LineSweep = LineSweep()

    A: Point = Point(0, 5)
    B: Point = Point(5, 5)
    pol1: list[Segment] = [Segment(A, B)]

    D: Point = Point(5, 5)
    E: Point = Point(10, 5)
    pol2: list[Segment] = [Segment(D, E)]

    assert L.do_polygons_intersect(pol1, pol2)


def test_get_above_and_below() -> None:
    L: LineSweep = LineSweep()
    tree: AVLTree = AVLTree()
    tree.insert(35)

    tree.insert(40)
    tree.insert(30)

    tree.insert(50)
    tree.insert(25)
    tree.insert(33)
    tree.insert(38)

    tree.insert(28)
    tree.insert(31)
    tree.insert(34)
    tree.insert(42)

    # Ambas subárvores existem
    node = tree.search(30)
    assert node is not None
    above, below = L._get_above_and_below(node, tree)

    assert above is not None
    assert above.val == 31
    assert below is not None
    assert below.val == 28

    # Não existe inferior, apenas superior
    node = tree.search(25)
    assert node is not None
    above, below = L._get_above_and_below(node, tree)

    assert above is not None
    assert above.val == 28
    assert below is None

    # Não existe superior, apenas inferior
    node = tree.search(50)
    assert node is not None
    above, below = L._get_above_and_below(node, tree)

    assert above is None
    assert below is not None
    assert below.val == 42

    # Ambas árvores nulas, mas o pai é superior
    node = tree.search(38)
    assert node is not None
    above, below = L._get_above_and_below(node, tree)

    assert above is not None
    assert above.val == 40
    assert below is not None
    assert below.val == 35

    # Ambas árvores nulas, mas o pai é inferior
    node = tree.search(34)
    assert node is not None
    above, below = L._get_above_and_below(node, tree)

    assert above is not None
    assert above.val == 35
    assert below is not None
    assert below.val == 33
