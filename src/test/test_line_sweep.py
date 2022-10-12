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
    B = Point(9, 10)
    C = Point(10, 4)
    pol1: list[Segment] = [
        Segment(A, B),
        Segment(B, C),
    ]

    D = Point(4, 2)
    E = Point(8, 1)
    F = Point(9, 5)
    pol2: list[Segment] = [
        Segment(D, E),
        Segment(F, D),
    ]

    sil: list[tuple[Segment, int]] = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)

    assert L.check_polygons_intersect(sil)


def test_get_above_and_below():
    L: LineSweep = LineSweep()
    T: AVLTree = AVLTree()
    T.insert(35)

    T.insert(40)
    T.insert(30)

    T.insert(50)
    T.insert(25)
    T.insert(33)
    T.insert(38)

    T.insert(28)
    T.insert(31)
    T.insert(34)
    T.insert(42)

    # Ambas sub-árvores existem
    node = T.search(30)
    above, below = L.get_above_and_below(node, T)

    assert above is not None
    assert below is not None
    assert above.val == 31
    assert below.val == 28

    # Não existe inferior, apenas superior
    node = T.search(25)
    above, below = L.get_above_and_below(node, T)

    assert below is None
    assert above is not None
    assert above.val == 28

    # Não existe superior, apenas inferior
    node = T.search(50)
    above, below = L.get_above_and_below(node, T)

    assert below is not None
    assert below.val == 42
    assert above is None

    # Ambas árvores nulas, mas o pai é superior
    node = T.search(38)
    above, below = L.get_above_and_below(node, T)

    assert below is None
    assert above is not None
    assert above.val == 40

    # Ambas árvores nulas, mas o pai é inferior
    node = T.search(34)
    above, below = L.get_above_and_below(node, T)

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
