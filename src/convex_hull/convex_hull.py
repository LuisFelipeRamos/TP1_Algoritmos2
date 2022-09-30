from typing import cast

import matplotlib.pyplot as plt

from src.point import Point
from src.segment import Segment

class ConvexHull:

    def __init__(self, set_of_points: list[Point], alg: str) -> None:
        self.set_of_points = set_of_points
        self.alg = alg
        self.num_of_vertexes = 0
        if (self.alg == 'gift_wrapping'):
            self.convex_hull = self.generate_throught_gift_wrapping_alg()
        else:
            self.convex_hull = self.generate_throught_graham_scan_alg()
    
    def generate_throught_gift_wrapping_alg(self) -> list[Segment]:
        anchor: Point = min(self.set_of_points)
        curr_anchor: Point = anchor
        dst: Point = self.set_of_points[0] if self.set_of_points[0] != anchor else self.set_of_points[1]
        curr_hull_edge: Segment = Segment(anchor, dst)
        convex_hull: list[Segment] = []
        while (dst != anchor):
            dst = self.set_of_points[0] if self.set_of_points[0] != curr_anchor else self.set_of_points[1]
            for point in self.set_of_points:
                if (point == curr_anchor or point == dst):
                    continue
                possible_hull_edge: Segment = Segment(curr_anchor, point)
                if (curr_hull_edge.is_counter_clockwise(possible_hull_edge)): 
                    curr_hull_edge = possible_hull_edge
                    dst = point
            convex_hull.append(curr_hull_edge)
            self.num_of_vertexes += 1
            curr_anchor = dst
            curr_hull_edge = Segment(curr_anchor, self.set_of_points[0] if self.set_of_points[0] != curr_anchor else self.set_of_points[1])
        return convex_hull
    
    def generate_throught_graham_scan_alg(self) -> list[Segment]:
        anchor: Point = min(self.set_of_points)
        anchor_to_points_segments: list[Segment] = []
        convex_hull: list[Segment] = []
        for point in self.set_of_points:
            if point != anchor:
                anchor_to_points_segments.append(Segment(anchor, point))
        anchor_to_points_segments.sort()
        points_ordered_by_polar_angle: list[Point] = [segment.p1 for segment in anchor_to_points_segments]
        points_ordered_by_polar_angle.append(anchor)
        curr_point: Point = points_ordered_by_polar_angle[0]
        convex_hull.append(Segment(anchor, curr_point))
        i: int = 0
        while (curr_point != anchor):
            possible_hull_edge: Segment = Segment(points_ordered_by_polar_angle[i], points_ordered_by_polar_angle[i + 1])
            if (possible_hull_edge.is_counter_clockwise(convex_hull[-1])):
                convex_hull.append(possible_hull_edge)
                curr_point = points_ordered_by_polar_angle[i + 1]
                i += 1
            else:
                del convex_hull[-1]
                del points_ordered_by_polar_angle[i]
                i -= 1
        return convex_hull

    def plot(self, size: int) -> None:
        _, ax = plt.subplots(figsize=(size, size))
        ax = cast(plt.Axes, ax)
        ax.scatter([point.x for point in self.set_of_points], [point.y for point in self.set_of_points], c=['k'], s=2)
        ax.grid(which='both', color='grey', linewidth=0.5, linestyle='-', alpha=0.2)
        for edge in self.convex_hull:
            plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], 'k', linewidth=0.5)
        plt.show()
