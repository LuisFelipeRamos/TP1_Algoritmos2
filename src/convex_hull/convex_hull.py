from src.segment import Segment


def gift_wrapping_convex_hull(set_of_points):
    anchor = min(set_of_points)
    curr_anchor = anchor
    dst = set_of_points[0] if set_of_points[0] != anchor else set_of_points[1]
    curr_hull_edge = Segment(anchor, dst)
    convex_hull = []
    while dst != anchor:
        dst = set_of_points[0] if set_of_points[0] != curr_anchor else set_of_points[1]
        for point in set_of_points:
            if point == curr_anchor or point == dst:
                continue
            possible_hull_edge = Segment(curr_anchor, point)
            if curr_hull_edge.is_counter_clockwise(possible_hull_edge):
                curr_hull_edge = possible_hull_edge
                dst = point
        convex_hull.append(curr_hull_edge)
        curr_anchor = dst
        curr_hull_edge = Segment(
            curr_anchor,
            set_of_points[0] if set_of_points[0] != curr_anchor else set_of_points[1],
        )
    return convex_hull
