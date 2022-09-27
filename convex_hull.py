from point import Point
import math
import random
import matplotlib.pyplot as plt

def gift_wrapping_convex_hull(list_of_points):
    min_polar_angle = float('inf')
    anchor_point = min(list_of_points)
    curr_anchor_point = anchor_point
    min_polar_angle_point = Point(float('inf'), float('inf'))
    convex_hull = [anchor_point]
    while (min_polar_angle_point != anchor_point):
        for point in list_of_points:
            if (point == curr_anchor_point):
                continue

            curr_point_polar_angle = point.polar_angle(curr_anchor_point)
            
            if (curr_point_polar_angle < min_polar_angle):
                min_polar_angle = curr_point_polar_angle
                min_polar_angle_point = point
        convex_hull.append(min_polar_angle_point)
        print(min_polar_angle_point)
        curr_anchor_point = min_polar_angle_point
        min_polar_angle = float('inf')
    return convex_hull

list_of_points = []
for _ in range(5):
    x, y = random.randint(1, 10), random.randint(1, 10)
    list_of_points.append(Point(x, y))

listaux = [Point(1, 2), Point(3, 10), Point(9, 6),Point(9, 1), Point(4 ,8)]
for i in listaux:
    for j in listaux:
        print(i, end=' - ')
        print(j, end=' : ')
        print(j.polar_angle(i))


""" res = gift_wrapping_convex_hull(listaux)
for r in res: print (r) """

xmin, xmax, ymin,ymax = -10, 10, -10, 10
ticks_frequency = 1
fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter([point.x for point in listaux], [point.y for point in listaux], c=['b'])
ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)
plt.show()