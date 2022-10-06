import time

import pygame

from src.point import Point
from src.segment import Segment

pygame.init()

# colors
WHITE = 255, 255, 255
BLACK = 0, 0, 0
BLUE = 0, 0, 255
RED = 255, 0, 0
GREEN = 0, 255, 0


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
        elif alg == "incremental":
            self.animate_using_incremental_alg(set_of_points)
        else:
            print(
                "Não temos uma animação pronta para esse algoritmo de envoltória convexa"
            )

    def draw_curr_hull(self, screen, set_of_points, curr_hull):
        for point_to_draw in set_of_points:
            pygame.draw.circle(
                screen,
                WHITE,
                (point_to_draw.x, point_to_draw.y),
                3,
                0,
            )
        for edge in curr_hull:
            pygame.draw.line(
                screen,
                WHITE,
                (edge.p0.x, edge.p0.y),
                (edge.p1.x, edge.p1.y),
                1,
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

            anchor: Point = min(set_of_points)
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

            anchor: Point = min(set_of_points)
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

    def animate_using_incremental_alg(self, set_of_points):
        self.SCREEN: pygame.surface.Surface = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(
            "Incremental Algorithm Convex Hull Algorithm Animation"
        )
        clock: pygame.time.Clock = pygame.time.Clock()
        run: bool = True

        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            set_of_points.sort(key=lambda point: (point.x, point.y))

            lower_hull = []
            upper_hull = []

            anchor_to_next: Segment = Segment(set_of_points[0], set_of_points[1])
            anchor_to_next_next: Segment = Segment(set_of_points[0], set_of_points[2])
            if anchor_to_next.is_counter_clockwise(anchor_to_next_next):
                s0: Segment = Segment(set_of_points[0], set_of_points[2])
                s1: Segment = Segment(set_of_points[2], set_of_points[1])
                s2: Segment = Segment(set_of_points[1], set_of_points[0])
            else:
                s0: Segment = Segment(set_of_points[0], set_of_points[1])
                s1: Segment = Segment(set_of_points[1], set_of_points[2])
                s2: Segment = Segment(set_of_points[2], set_of_points[0])
            lower_hull.append(s0)
            upper_hull.append(s1)
            upper_hull.append(s2)
            convex_hull = lower_hull + upper_hull
            hull_farest_right_point = lower_hull[-1].p1
            for point in set_of_points[3:]:

                self.SCREEN.fill(BLACK)

                self.draw_curr_hull(self.SCREEN, set_of_points, convex_hull)

                for edge in convex_hull:
                    pygame.draw.line(
                        self.SCREEN,
                        WHITE,
                        (edge.p0.x, edge.p0.y),
                        (edge.p1.x, edge.p1.y),
                        1,
                    )

                if point.y >= hull_farest_right_point.y:
                    lower_point: Point = upper_hull[0].p0
                    upper_point: Point = upper_hull[0].p1
                    del upper_hull[0]

                else:
                    lower_point: Point = lower_hull[-1].p0
                    upper_point: Point = lower_hull[-1].p1
                    del lower_hull[-1]

                lower_hull_new_edge: Segment = Segment(lower_point, point)
                lower_hull.append(lower_hull_new_edge)

                upper_hull_new_edge = Segment(point, upper_point)
                upper_hull = [upper_hull_new_edge] + upper_hull

                hull_farest_right_point = lower_hull[-1].p1

                while len(upper_hull) >= 2 and not upper_hull[1].is_counter_clockwise(
                    upper_hull[0]
                ):
                    self.SCREEN.fill(BLACK)
                    self.draw_curr_hull(self.SCREEN, set_of_points, convex_hull)
                    pygame.draw.line(
                        self.SCREEN,
                        BLUE,
                        (lower_hull_new_edge.p0.x, lower_hull_new_edge.p0.y),
                        (lower_hull_new_edge.p1.x, lower_hull_new_edge.p1.y),
                        1,
                    )
                    pygame.draw.line(
                        self.SCREEN,
                        BLUE,
                        (upper_hull_new_edge.p0.x, upper_hull_new_edge.p0.y),
                        (upper_hull_new_edge.p1.x, upper_hull_new_edge.p1.y),
                        1,
                    )
                    time.sleep(0.2)
                    new_edge_p0: Point = upper_hull[0].p0
                    new_edge_p1: Point = upper_hull[1].p1
                    del upper_hull[0:2]
                    upper_hull_new_edge = Segment(new_edge_p0, new_edge_p1)
                    upper_hull = [upper_hull_new_edge] + upper_hull
                    convex_hull = lower_hull + upper_hull
                    pygame.display.flip()
                    time.sleep(0.2)
                time.sleep(0.2)
                while len(lower_hull) >= 2 and not lower_hull[-1].is_counter_clockwise(
                    lower_hull[-2]
                ):
                    self.SCREEN.fill(BLACK)
                    self.draw_curr_hull(self.SCREEN, set_of_points, convex_hull)
                    pygame.draw.line(
                        self.SCREEN,
                        BLUE,
                        (lower_hull_new_edge.p0.x, lower_hull_new_edge.p0.y),
                        (lower_hull_new_edge.p1.x, lower_hull_new_edge.p1.y),
                        1,
                    )
                    pygame.draw.line(
                        self.SCREEN,
                        BLUE,
                        (upper_hull_new_edge.p0.x, upper_hull_new_edge.p0.y),
                        (upper_hull_new_edge.p1.x, upper_hull_new_edge.p1.y),
                        1,
                    )
                    time.sleep(0.2)
                    new_edge_p0: Point = lower_hull[-2].p0
                    new_edge_p1: Point = lower_hull[-1].p1
                    del lower_hull[-1:-3:-1]
                    lower_hull_new_edge = Segment(new_edge_p0, new_edge_p1)

                    lower_hull.append(lower_hull_new_edge)
                    convex_hull = lower_hull + upper_hull
                    pygame.display.flip()
                    time.sleep(0.2)

                pygame.display.flip()
                convex_hull = lower_hull + upper_hull
            time.sleep(0.2)
            self.SCREEN.fill(BLACK)
            self.draw_curr_hull(self.SCREEN, set_of_points, convex_hull)
            pygame.display.flip()
            pygame.time.wait(3000)
            run = False
