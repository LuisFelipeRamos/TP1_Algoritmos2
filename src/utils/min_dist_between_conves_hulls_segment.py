from src.convex_hull import ConvexHull
from src.point import Point
from src.segment import Segment


def min_dist_between_convex_hulls_segment(
    convex_hull_1: ConvexHull, convex_hull_2: ConvexHull
) -> Segment:
    points_hull_1: list = [edge.p0 for edge in convex_hull_1.convex_hull]
    points_hull_2: list = [edge.p0 for edge in convex_hull_2.convex_hull]
    min_dist: float = float("inf")
    min_dist_segment: Segment = Segment(Point(0, 0), Point(0, 0))
    for p in points_hull_1:
        for q in points_hull_2:
            curr_dist: float = p.get_distance(q)
            if curr_dist < min_dist:
                min_dist = curr_dist
                min_dist_segment = Segment(p, q)
    return min_dist_segment
