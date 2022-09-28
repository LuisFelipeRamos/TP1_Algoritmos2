from src.point import Point
from src.convex_hull import gift_wrapping_convex_hull
import random
import matplotlib.pyplot as plt

set_of_points = []
for _ in range(100):
    x, y = random.randint(1, 100), random.randint(1, 100)
    set_of_points.append(Point(x, y))

hull = gift_wrapping_convex_hull(set_of_points)


xmin, xmax, ymin, ymax = -100, 100, -100, 100
ticks_frequency = 1
fig, ax = plt.subplots(figsize=(100, 100))
ax.scatter(
    [point.x for point in set_of_points], [point.y for point in set_of_points], c=["b"]
)
ax.grid(which="both", color="grey", linewidth=1, linestyle="-", alpha=0.2)
for edge in hull:
    plt.plot(
        [edge.points[0].x, edge.points[1].x], [edge.points[0].y, edge.points[1].y], "r"
    )
plt.show()
