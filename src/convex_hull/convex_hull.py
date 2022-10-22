from __future__ import annotations

from typing import cast

import matplotlib.pyplot as plt

from src.point import Point
from src.segment import Segment


class ConvexHull:
    def __init__(self, set_of_points: list[Point], alg: str) -> None:
        self.set_of_points = set_of_points
        self.alg = alg
        self.num_of_vertexes = 0
        if self.alg == "gift_wrapping":
            self.convex_hull = self.generate_through_gift_wrapping_alg()
        elif self.alg == "graham_scan":
            self.convex_hull = self.generate_through_graham_scan_alg()
        elif self.alg == "incremental":
            self.convex_hull = self.generate_through_incremental_alg()
        else:
            print("I don't know this alg...")

    def generate_through_gift_wrapping_alg(self) -> list[Segment]:
        anchor: Point = min(self.set_of_points)
        curr_anchor: Point = anchor
        dst: Point = (
            self.set_of_points[0]
            if self.set_of_points[0] != anchor
            else self.set_of_points[1]
        )
        curr_hull_edge: Segment = Segment(anchor, dst)
        convex_hull: list[Segment] = []
        while dst != anchor:
            dst = (
                self.set_of_points[0]
                if self.set_of_points[0] != curr_anchor
                else self.set_of_points[1]
            )
            for point in self.set_of_points:
                if point == curr_anchor or point == dst:
                    continue
                possible_hull_edge: Segment = Segment(curr_anchor, point)
                if curr_hull_edge.is_counter_clockwise(possible_hull_edge):
                    curr_hull_edge = possible_hull_edge
                    dst = point
            convex_hull.append(curr_hull_edge)
            self.num_of_vertexes += 1
            curr_anchor = dst
            curr_hull_edge = Segment(
                curr_anchor,
                self.set_of_points[0]
                if self.set_of_points[0] != curr_anchor
                else self.set_of_points[1],
            )
        return convex_hull

    def generate_through_graham_scan_alg(self) -> list[Segment]:
        anchor: Point = min(self.set_of_points)
        anchor_to_points_segments: list[Segment] = []
        convex_hull: list[Segment] = []
        for point in self.set_of_points:
            if point != anchor:
                anchor_to_points_segments.append(Segment(anchor, point))
        anchor_to_points_segments.sort()
        points_ordered_by_polar_angle: list[Point] = [
            segment.p1 for segment in anchor_to_points_segments
        ]
        points_ordered_by_polar_angle.append(anchor)
        curr_point: Point = points_ordered_by_polar_angle[0]
        convex_hull.append(Segment(anchor, curr_point))
        i: int = 0
        while curr_point != anchor:
            possible_hull_edge: Segment = Segment(
                points_ordered_by_polar_angle[i], points_ordered_by_polar_angle[i + 1]
            )
            if possible_hull_edge.is_counter_clockwise(convex_hull[-1]):
                convex_hull.append(possible_hull_edge)
                curr_point = points_ordered_by_polar_angle[i + 1]
                i += 1
            else:
                del convex_hull[-1]
                del points_ordered_by_polar_angle[i]
                i -= 1
        return convex_hull

    def generate_through_incremental_alg(self) -> list[Segment]:

        self.set_of_points.sort(key=lambda point: (point.x, point.y))

        lower_hull: list[Segment] = []
        upper_hull: list[Segment] = []

        anchor_to_next: Segment = Segment(self.set_of_points[0], self.set_of_points[1])
        anchor_to_next_next: Segment = Segment(
            self.set_of_points[0], self.set_of_points[2]
        )
        if anchor_to_next.is_counter_clockwise(anchor_to_next_next):
            s0: Segment = Segment(self.set_of_points[0], self.set_of_points[2])
            s1: Segment = Segment(self.set_of_points[2], self.set_of_points[1])
            s2: Segment = Segment(self.set_of_points[1], self.set_of_points[0])
        else:
            s0: Segment = Segment(self.set_of_points[0], self.set_of_points[1])
            s1: Segment = Segment(self.set_of_points[1], self.set_of_points[2])
            s2: Segment = Segment(self.set_of_points[2], self.set_of_points[0])
        lower_hull.append(s0)
        upper_hull.append(s1)
        upper_hull.append(s2)
        hull_farest_right_point: Point = lower_hull[-1].p1
        for point in self.set_of_points[3:]:

            hull_farest_right_point_to_new_point: Segment = Segment(
                hull_farest_right_point, point
            )
            if hull_farest_right_point_to_new_point.is_counter_clockwise(
                lower_hull[-1]
            ):
                lower_point: Point = upper_hull[0].p0
                upper_point: Point = upper_hull[0].p1
                del upper_hull[0]

            else:
                lower_point: Point = lower_hull[-1].p0
                upper_point: Point = lower_hull[-1].p1
                del lower_hull[-1]

            lower_hull.append(Segment(lower_point, point))
            upper_hull = [Segment(point, upper_point)] + upper_hull
            hull_farest_right_point = lower_hull[-1].p1

            while len(upper_hull) >= 2 and not upper_hull[1].is_counter_clockwise(
                upper_hull[0]
            ):
                new_edge_p0: Point = upper_hull[0].p0
                new_edge_p1: Point = upper_hull[1].p1
                del upper_hull[0:2]
                upper_hull = [Segment(new_edge_p0, new_edge_p1)] + upper_hull
            while len(lower_hull) >= 2 and not lower_hull[-1].is_counter_clockwise(
                lower_hull[-2]
            ):
                new_edge_p0: Point = lower_hull[-2].p0
                new_edge_p1: Point = lower_hull[-1].p1
                del lower_hull[-1:-3:-1]
                lower_hull.append(Segment(new_edge_p0, new_edge_p1))

        convex_hull: list[Segment] = lower_hull + upper_hull
        return convex_hull

    def plot(self) -> None:
        _, ax = plt.subplots(figsize=(100, 100))
        ax = cast(plt.Axes, ax)
        ax.scatter(
            [point.x for point in self.set_of_points],
            [point.y for point in self.set_of_points],
            c=["k"],
            s=2,
        )
        ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
        for edge in self.convex_hull:
            plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "k", linewidth=0.5)
        plt.show()

    def is_inside(self, other: ConvexHull) -> bool:
        """
        Checa se `other` está dentro de `self`, dado que os polígonos não se interceptam
        """
        # Se um polígono não intersecta outro,
        # então para um estar contido no outro basta que um ponto esteja.
        point: Point = other.convex_hull[0].p0
        return point.is_inside(self.convex_hull)
