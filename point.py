import math

class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __lt__(self, other):
        return self.y < other.y if self.y != other.y else self.x < other.x
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    
    def polar_angle(self, p):
        curr_point_polar_angle = math.atan2((self.y - p.y), (self.x - p.x))*180/math.pi
        curr_point_polar_angle = curr_point_polar_angle if (curr_point_polar_angle >= 0) else 360 + curr_point_polar_angle
        return curr_point_polar_angle

    