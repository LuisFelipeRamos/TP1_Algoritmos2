# pylint: disable=missing-function-docstring, missing-module-docstring
from src.line_sweep import LineSweep
from src.line_sweep.lib.avl_tree import AVLTree
from src.point import Point
from src.segment import Segment


def test_polygons_intersect():
    L: LineSweep = LineSweep()

    A = Point(1, 1)
    B = Point(4, 4)
    C = Point(3, 2)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
        Segment(C, A),
    ]
    D = Point(3, 2.5)
    E = Point(6, 3)
    F = Point(6.5, 0.5)
    pol2: list[Segment] = [
        Segment(D, E),
        Segment(E, F),
        Segment(F, D),
    ]
    sil: list[tuple[Segment, int]] = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)
    assert L.check_polygons_intersect(sil)

    # Ponto em comum em dois "polígonos" diferentes (no caso linhas, para simplificar)
    pol1 = [Segment(A, B)]
    pol2 = [Segment(B, F)]
    sil = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)
    assert L.check_polygons_intersect(sil)


def test_polygons_intersect_pt2():
    L: LineSweep = LineSweep()

    A = Point(1, 1)
    B = Point(4, 4)
    C = Point(3, 2)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
        Segment(C, A),
    ]
    D = Point(3.5, 2.5)
    E = Point(6, 3)
    F = Point(6.5, 0.5)
    pol2: list[Segment] = [
        Segment(D, E),
        Segment(E, F),
        Segment(F, D),
    ]
    sil: list[tuple[Segment, int]] = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)
    assert not L.check_polygons_intersect(sil)


def test_polygons_intersect_pt3():
    L: LineSweep = LineSweep()

    A = Point(1, 7)
    B = Point(3, 1)
    C = Point(10, 1)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
        Segment(C, A),
    ]
    D = Point(6, 8)
    E = Point(7, 7)
    F = Point(9, 9)
    pol2: list[Segment] = [
        Segment(D, E),
        Segment(E, F),
        Segment(F, D),
    ]
    sil: list[tuple[Segment, int]] = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)
    assert not L.check_polygons_intersect(sil)


def test_polygons_intersect_pt4():
    L: LineSweep = LineSweep()

    A = Point(9, 7)
    B = Point(3, 1)
    C = Point(5, 8)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
    ]

    D = Point(4, 4)
    E = Point(10, 3)
    F = Point(9, 4)
    pol2: list[Segment] = [
        Segment(D, E),
        Segment(F, D),
    ]

    sil: list[tuple[Segment, int]] = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)

    assert L.check_polygons_intersect(sil)


def test_polygons_intersect_pt5():
    L: LineSweep = LineSweep()

    A = Point(2, 9)
    B = Point(10, 11)
    C = Point(10, 4)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(A, C),
    ]

    D = Point(4, 2)
    F = Point(9, 6)
    pol2: list[Segment] = [
        Segment(F, D),
    ]

    sil: list[tuple[Segment, int]] = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)

    assert L.check_polygons_intersect(sil)


def test_polygons_intersect_pt6():
    L: LineSweep = LineSweep()

    A = Point(4, 6)
    B = Point(8, 5)
    C = Point(1, 4)
    pol1: list[Segment] = [Segment(A, B), Segment(B, C)]

    D = Point(5, 3)
    E = Point(9, 5)
    F = Point(9, 7)
    pol2: list[Segment] = [Segment(D, E), Segment(F, D)]

    sil: list[tuple[Segment, int]] = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)

    assert L.check_polygons_intersect(sil)


def test_get_above_and_below():
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
    above, below = L.get_above_and_below(node, tree)

    assert above is not None
    assert below is not None
    assert above.val == 31
    assert below.val == 28

    # Não existe inferior, apenas superior
    node = tree.search(25)
    above, below = L.get_above_and_below(node, tree)

    assert below is None
    assert above is not None
    assert above.val == 28

    # Não existe superior, apenas inferior
    node = tree.search(50)
    above, below = L.get_above_and_below(node, tree)

    assert below is not None
    assert below.val == 42
    assert above is None

    # Ambas árvores nulas, mas o pai é superior
    node = tree.search(38)
    above, below = L.get_above_and_below(node, tree)

    assert below is None
    assert above is not None
    assert above.val == 40

    # Ambas árvores nulas, mas o pai é inferior
    node = tree.search(34)
    above, below = L.get_above_and_below(node, tree)

    assert above is None
    assert below is not None
    assert below.val == 33


def test_invert_segments():
    L: LineSweep = LineSweep()
    set_of_segments: list[Segment] = [
        Segment(Point(4, 4), Point(1, 1)),
        Segment(Point(2, 3), Point(3, 2)),
    ]
    L.invert_segments(set_of_segments)

    inverted_segments: list[Segment] = [
        Segment(Point(1, 1), Point(4, 4)),
        Segment(Point(2, 3), Point(3, 2)),
    ]
    assert [p1 == p2 for p1, p2 in zip(set_of_segments, inverted_segments)]
