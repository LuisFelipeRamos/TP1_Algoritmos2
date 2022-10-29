from src.convex_hull import ConvexHull
from src.segment import Segment


class Classifier:
    def __init__(self, class1: list, class2: list):
        self.class1 = class1
        self.class2 = class2

        self.slope, self.linear, self.mid_point = self.fit()

        if class1[0].y > (class1[0].x * self.slope + self.linear):
            self.class_gt = 1
            self.class_lt = 2
        else:
            self.class_gt = 2
            self.class_lt = 1

    def __repr__(self) -> str:
        return f"[{self.fit()}]"

    def fit(self):
        convex_hull_1: ConvexHull = ConvexHull(self.class1, alg="graham_scan")
        convex_hull_2: ConvexHull = ConvexHull(self.class2, alg="graham_scan")
        min_dist_segment: Segment = convex_hull_1.min_dist(convex_hull_2)
        return min_dist_segment.get_perpendicular_segment()

    def test(self, data: list):
        result = []
        for i in range(len(data)):
            if data[i].y > data[i].x * self.slope + self.linear:
                result.append(self.class_gt)
            else:
                result.append(self.class_lt)
        return result
