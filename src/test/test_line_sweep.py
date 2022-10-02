from src.point import Point
from src.segment import Segment
from src.line_sweep import LineSweep


def test_any_segments_intersect():
    L: LineSweep = LineSweep()

    pol1_a = Point(1, 1)
    pol1_b = Point(4, 4)
    pol1_c = Point(3, 2)
    pol1: list[Segment] = [
        Segment(pol1_a, pol1_b, 1),
        Segment(pol1_b, pol1_c, 1),
        Segment(pol1_c, pol1_a, 1),
    ]
    pol2_a = Point(3, 2.5)
    pol2_b = Point(6, 3)
    pol2_c = Point(6.5, 0.5)
    pol2: list[Segment] = [
        Segment(pol2_a, pol2_b, 2),
        Segment(pol2_b, pol2_c, 2),
        Segment(pol2_c, pol2_a, 2),
    ]
    assert L.any_segments_intersect(pol1, pol2)

def test_any_segments_intersect_pt2():
    L: LineSweep = LineSweep()

    pol1_a = Point(1, 1)
    pol1_b = Point(4, 4)
    pol1_c = Point(3, 2)
    pol1: list[Segment] = [
        Segment(pol1_a, pol1_b, 1),
        Segment(pol1_b, pol1_c, 1),
        Segment(pol1_c, pol1_a, 1),
    ]
    pol2_a = Point(3.5, 2.5)
    pol2_b = Point(6, 3)
    pol2_c = Point(6.5, 0.5)
    pol2: list[Segment] = [
        Segment(pol2_a, pol2_b, 2),
        Segment(pol2_b, pol2_c, 2),
        Segment(pol2_c, pol2_a, 2),
    ]
    assert not L.any_segments_intersect(pol1, pol2)
