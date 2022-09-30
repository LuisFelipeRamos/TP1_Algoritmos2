from __future__ import annotations
from ..point.point import Point

class Segment():

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

        self.x = p1.x - p0.x
        self.y = p1.y - p0.y

        self.length = self.p0.get_distance(p1)
    
    def __repr__(self):
        return f"<{self.p0}, {self.p1}>"
    
    def __lt__(self, other):
        return not self.is_counter_clockwise(other)

    def cross_product(self, other):
        return self.x*other.y - self.y*other.x
    
    def is_colinear(self, other):
        return self.cross_product(other) == 0

    def is_counter_clockwise(self, other):
        if (self.is_colinear(other)):
            return self.length < other.length
        return self.cross_product(other) < 0