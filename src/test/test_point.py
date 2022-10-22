# pylint: disable=missing-function-docstring, missing-module-docstring

from src.point import Point
from src.segment import Segment


def test_is_inside() -> None:
    polygon: list[Segment] = [
        Segment(Point(0, 0), Point(5, 0)),
        Segment(Point(5, 0), Point(3, 3)),
        Segment(Point(3, 3), Point(0, 0)),
    ]

    A: Point = Point(1, 2)
    assert not A.is_inside(polygon)

    B: Point = Point(3, 1)
    assert B.is_inside(polygon)
