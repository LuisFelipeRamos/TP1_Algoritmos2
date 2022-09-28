from point import Point
from segment import Segment

n = int(input())
for _ in range(n):
    v = input()
    v = [int(x) for x in v.split()]
    p0 = Point(v[0], v[1])
    p1 = Point(v[2], v[3])
    p2 = Point(v[4], v[5])
    s1 = Segment(p0,p1)
    s2 = Segment(p1, p2)
    print("YES") if s2.is_counter_clockwise(s1) else print("N0")
