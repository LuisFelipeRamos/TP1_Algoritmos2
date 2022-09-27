from point import Point
import math

def gift_wrapping_convex_hull(list_of_points):
    min_polar_angle = float('inf')
    anchor_point = min(list_of_points)
    min_polar_angle_point = Point(float('inf'), float('inf'))
    convex_hull = []
    while (min_polar_angle_point != anchor_point):
        for point in list_of_points:
            if (point.x - anchor_point.x == 0):
                curr_point_polar_angle = 0;
            else:  
                curr_point_polar_angle = math.atan((point.y - anchor_point.y)/(point.x - anchor_point.x))
            if (curr_point_polar_angle < min_polar_angle):
                min_polar_angle = curr_point_polar_angle
                min_polar_angle_point = point
        convex_hull.append(min_polar_angle_point)
        anchor_point = min_polar_angle_point
    return convex_hull

list_of_points = [Point(1, 2), Point(5, 4), Point(-3, -2), Point(-3, 1)]

res = gift_wrapping_convex_hull(list_of_points)
for r in res: print(r)