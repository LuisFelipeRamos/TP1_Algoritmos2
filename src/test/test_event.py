from src.line_sweep.event import Event
from src.segment import Segment
from src.point import Point


def test_compare():
    dummy: Segment = Segment(Point(0, 0), Point(0, 0))

    a: Event = Event(10, 10, True, dummy)
    b: Event = Event(11, 11, True, dummy)

    assert a < b

    c: Event = Event(10, 3, False, dummy)

    assert a < c

    d: Event = Event(10, 20, True, dummy)

    assert a < d

    assert not a < a
