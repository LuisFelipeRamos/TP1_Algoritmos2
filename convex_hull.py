from point import Point
from segment import Segment
import math
import random
import matplotlib.pyplot as plt

def gift_wrapping_convex_hull(set_of_points):
    anchor = min(set_of_points)
    curr_anchor = anchor
    dst = set_of_points[0] if set_of_points[0] != anchor else set_of_points[1]
    curr_hull_edge = Segment(anchor, dst)
    convex_hull = []
    while (dst != anchor):
        dst = set_of_points[0] if set_of_points[0] != curr_anchor else set_of_points[1]
        for point in set_of_points:
            if (point == curr_anchor or point == dst):
                continue
            possible_hull_edge = Segment(curr_anchor, point)
            if (curr_hull_edge.is_counter_clockwise(possible_hull_edge)): 
                curr_hull_edge = possible_hull_edge
                dst = point
        convex_hull.append(curr_hull_edge)
        curr_anchor = dst
        curr_hull_edge = Segment(curr_anchor, set_of_points[0] if set_of_points[0] != curr_anchor else set_of_points[1] )
    return convex_hull

set_of_points = []
for _ in range(100):
    x, y = random.randint(1, 100), random.randint(1, 100)
    set_of_points.append(Point(x, y))

hull = gift_wrapping_convex_hull(set_of_points)


xmin, xmax, ymin,ymax = -100, 100, -100, 100
ticks_frequency = 1
fig, ax = plt.subplots(figsize=(100, 100))
ax.scatter([point.x for point in set_of_points], [point.y for point in set_of_points], c=['b'])
ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)
for edge in hull:
    plt.plot([edge.points[0].x, edge.points[1].x], [edge.points[0].y, edge.points[1].y], 'r')
plt.show()