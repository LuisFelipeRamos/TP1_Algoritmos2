import time

import pygame

from src.point import Point
from src.segment import Segment

import time
import pygame

pygame.init()

# colors
WHITE = 255, 255, 255
BLACK = 0, 0, 0
BLUE = 0, 0, 255
RED = 255, 0, 0

class AlgorithmVisualization:
    def __init__(
        self, screen_width: int, screen_height: int, screen_margin: int, fps: int
    ) -> None:
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.SCREEN_MARGIN = screen_margin
        self.FPS = fps

    def animate_convex_hull(self, alg: str, set_of_points: list[Point]) -> None:

        if alg == "gift_wrapping":
            self.animate_using_gift_wrapping(set_of_points)
        elif alg == "graham_scan":
            self.animate_using_graham_scan(set_of_points)
        else:
            print(
                "Não temos uma animação pronta para esse algoritmo de envoltória convexa"
            )

    def animate_using_gift_wrapping(self, set_of_points: list[Point]) -> None:
        self.SCREEN: pygame.surface.Surface = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Gift Wrapping Convex Hull Algorithm Animation")
        clock: pygame.time.Clock = pygame.time.Clock()
        run: bool = True

        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            anchor: Point = max(set_of_points)
            curr_anchor: Point = anchor
            dst: Point = (
                set_of_points[0] if set_of_points[0] != anchor else set_of_points[1]
            )
            curr_hull_edge: Segment = Segment(anchor, dst)
            convex_hull: list[Segment] = []
            while dst != anchor:
                dst = (
                    set_of_points[0]
                    if set_of_points[0] != curr_anchor
                    else set_of_points[1]
                )
                for point in set_of_points:
                    self.SCREEN.fill(BLACK)

                    if point == curr_anchor or point == dst:
                        continue
                    possible_hull_edge: Segment = Segment(curr_anchor, point)
                    for point_to_draw in set_of_points:
                        pygame.draw.circle(
                            self.SCREEN,
                            WHITE,
                            (point_to_draw.x, point_to_draw.y),
                            3,
                            0,
                        )
                    for edge in convex_hull:
                        pygame.draw.line(
                            self.SCREEN,
                            WHITE,
                            (edge.p0.x, edge.p0.y),
                            (edge.p1.x, edge.p1.y),
                            1,
                        )
                    pygame.draw.line(
                        self.SCREEN,
                        BLUE,
                        (curr_hull_edge.p0.x, curr_hull_edge.p0.y),
                        (curr_hull_edge.p1.x, curr_hull_edge.p1.y),
                        1,
                    )
                    pygame.draw.line(
                        self.SCREEN,
                        RED,
                        (possible_hull_edge.p0.x, possible_hull_edge.p0.y),
                        (possible_hull_edge.p1.x, possible_hull_edge.p1.y),
                        1,
                    )
                    time.sleep(0.1)
                    pygame.display.flip()
                    if curr_hull_edge.is_counter_clockwise(possible_hull_edge):
                        curr_hull_edge = possible_hull_edge
                        dst = point

                convex_hull.append(curr_hull_edge)
                curr_anchor: Point = dst
                curr_hull_edge = Segment(
                    curr_anchor,
                    set_of_points[0]
                    if set_of_points[0] != curr_anchor
                    else set_of_points[1],
                )

            self.SCREEN.fill(BLACK)
            for point_to_draw in set_of_points:
                pygame.draw.circle(
                    self.SCREEN, WHITE, (point_to_draw.x, point_to_draw.y), 3, 0
                )
            for edge in convex_hull:
                pygame.draw.line(
                    self.SCREEN,
                    WHITE,
                    (edge.p0.x, edge.p0.y),
                    (edge.p1.x, edge.p1.y),
                    1,
                )

            pygame.display.flip()
            pygame.time.wait(5000)
            run = False

    def animate_using_graham_scan(self, set_of_points: list[Point]) -> None:
        self.SCREEN: pygame.surface.Surface = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Graham Scan Convex Hull Algorithm Animation")
        clock: pygame.time.Clock = pygame.time.Clock()
        run: bool = True

        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            anchor: Point = max(set_of_points)
            anchor_to_points_segments: list[Segment] = []
            convex_hull: list[Segment] = []
            for point in set_of_points:
                if point != anchor:
                    anchor_to_points_segments.append(Segment(anchor, point))
            anchor_to_points_segments.sort()
            points_ordered_by_polar_angle: list[Point] = [
                segment.p1 for segment in anchor_to_points_segments
            ]
            points_ordered_by_polar_angle.append(anchor)
            curr_point: Point = points_ordered_by_polar_angle[0]
            convex_hull.append(Segment(anchor, curr_point))
            i: int = 0
            while curr_point != anchor:

                self.SCREEN.fill(BLACK)
                for point_to_draw in set_of_points:
                    pygame.draw.circle(
                        self.SCREEN, WHITE, (point_to_draw.x, point_to_draw.y), 3, 0
                    )
                for edge in convex_hull:
                    pygame.draw.line(
                        self.SCREEN,
                        WHITE,
                        (edge.p0.x, edge.p0.y),
                        (edge.p1.x, edge.p1.y),
                        1,
                    )
                possible_hull_edge: Segment = Segment(
                    points_ordered_by_polar_angle[i],
                    points_ordered_by_polar_angle[i + 1],
                )
                time.sleep(0.1)
                pygame.draw.line(
                    self.SCREEN,
                    RED,
                    (possible_hull_edge.p0.x, possible_hull_edge.p0.y),
                    (possible_hull_edge.p1.x, possible_hull_edge.p1.y),
                    1,
                )
                if possible_hull_edge.is_counter_clockwise(convex_hull[-1]):
                    convex_hull.append(possible_hull_edge)
                    curr_point = points_ordered_by_polar_angle[i + 1]
                    i += 1
                else:
                    del convex_hull[-1]
                    del points_ordered_by_polar_angle[i]
                    i -= 1
                time.sleep(0.1)
                pygame.display.flip()

            self.SCREEN.fill(BLACK)
            for point_to_draw in set_of_points:
                pygame.draw.circle(
                    self.SCREEN, WHITE, (point_to_draw.x, point_to_draw.y), 3, 0
                )
            for edge in convex_hull:
                pygame.draw.line(
                    self.SCREEN,
                    WHITE,
                    (edge.p0.x, edge.p0.y),
                    (edge.p1.x, edge.p1.y),
                    1,
                )
            pygame.display.flip()

            pygame.time.wait(5000)
            run = False
