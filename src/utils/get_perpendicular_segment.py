from src.point import Point
from src.segment import Segment

def get_perpendicular_segment(segment: Segment):
    slope: float = (segment.p1.y - segment.p0.y)/(segment.p1.x - segment.p0.x) if segment.p1.x - segment.p0.x != 0 else 0
    negative_inverse_slope: float = -1 / slope if slope != 0 else 0
    midpoint: Point = Point((segment.p0.x + segment.p1.x)/2, (segment.p0.y + segment.p1.y)/2)
    b: float = midpoint.y - negative_inverse_slope*midpoint.x
    return negative_inverse_slope, b
