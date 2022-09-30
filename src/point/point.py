from __future__ import annotations

import math

class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def __lt__(self, other):
        return self.y < other.y if self.y != other.y else self.x < other.x
    
    def __gt__(self, other):
        return self.y > other.y if self.y != other.y else self.x > other.x
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    
    def get_distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))