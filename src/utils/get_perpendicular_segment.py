from src.point import Point
from src.segment import Segment


def get_perpendicular_segment(segment: Segment) -> tuple[float, float, Point]:
    negative_inverse_slope: float = -1 / segment.slope if segment.slope != 0 else 0
    midpoint: Point = Point(
        (segment.p0.x + segment.p1.x) / 2, (segment.p0.y + segment.p1.y) / 2
    )
    linear: float = midpoint.y - negative_inverse_slope * midpoint.x
    return negative_inverse_slope, linear, midpoint
