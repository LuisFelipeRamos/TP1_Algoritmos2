from src.point import Point
from src.segment import Segment
from src.line_sweep import LineSweep
from src.line_sweep.lib.avl_tree import AVLTree


def test_polygons_intersect():
    L: LineSweep = LineSweep()

    pol1_a = Point(1, 1)
    pol1_b = Point(4, 4)
    pol1_c = Point(3, 2)
    pol1: list[Segment] = [
        Segment(pol1_a, pol1_b),
        Segment(pol1_b, pol1_c),
        Segment(pol1_c, pol1_a),
    ]
    pol2_a = Point(3, 2.5)
    pol2_b = Point(6, 3)
    pol2_c = Point(6.5, 0.5)
    pol2: list[Segment] = [
        Segment(pol2_a, pol2_b),
        Segment(pol2_b, pol2_c),
        Segment(pol2_c, pol2_a),
    ]
    sil: list[tuple[Segment, int]] = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)
    assert L.check_polygons_intersect(sil)

    # Ponto em comum em dois "polígonos" diferentes (no caso linhas, para simplificar)
    pol1 = [Segment(pol1_a, pol1_b)]
    pol2 = [Segment(pol1_b, pol2_c)]
    sil = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)
    assert L.check_polygons_intersect(sil)


def test_polygons_intersect_pt2():
    L: LineSweep = LineSweep()

    pol1_a = Point(1, 1)
    pol1_b = Point(4, 4)
    pol1_c = Point(3, 2)
    pol1: list[Segment] = [
        Segment(pol1_a, pol1_b),
        Segment(pol1_b, pol1_c),
        Segment(pol1_c, pol1_a),
    ]
    pol2_a = Point(3.5, 2.5)
    pol2_b = Point(6, 3)
    pol2_c = Point(6.5, 0.5)
    pol2: list[Segment] = [
        Segment(pol2_a, pol2_b),
        Segment(pol2_b, pol2_c),
        Segment(pol2_c, pol2_a),
    ]
    sil: list[tuple[Segment, int]] = [(seg, 1) for seg in pol1]
    sil.extend((seg, 2) for seg in pol2)
    assert not L.check_polygons_intersect(sil)


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

    assert above != None
    assert below != None
    assert above.val == 31
    assert below.val == 28

    # Não existe inferior, apenas superior
    node = T.search(25)
    above, below = L.get_above_and_below(node, T)

    assert below == None
    assert above != None
    assert above.val == 28

    # Não existe superior, apenas inferior
    node = T.search(50)
    above, below = L.get_above_and_below(node, T)

    assert below != None
    assert below.val == 42
    assert above == None

    # Ambas árvores nulas, mas o pai é superior
    node = T.search(38)
    above, below = L.get_above_and_below(node, T)

    assert below == None
    assert above != None
    assert above.val == 40

    # Ambas árvores nulas, mas o pai é inferior
    node = T.search(34)
    above, below = L.get_above_and_below(node, T)

    assert above == None
    assert below != None
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
