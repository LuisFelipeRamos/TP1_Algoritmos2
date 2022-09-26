from modules import *

def convex_hull(list_of_points):
    anchor_point = min(list_of_points)
    

list_of_points = [Point(1,2), Point(5, 4), Point(-3, -2), Point(-3, 1)]
convex_hull(list_of_points)