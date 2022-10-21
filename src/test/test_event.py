# pylint: disable=missing-function-docstring, missing-module-docstring
from src.line_sweep.event import Event
from src.point import Point
from src.segment import Segment


def test_compare() -> None:
    dummy: Segment = Segment(Point(0, 0), Point(0, 0))

    i: Event = Event(Point(10, 10), True, dummy)
    j: Event = Event(Point(11, 11), True, dummy)

    assert i < j

    k: Event = Event(Point(10, 3), False, dummy)

    assert i < k

    l: Event = Event(Point(10, 20), True, dummy)

    assert i < l
