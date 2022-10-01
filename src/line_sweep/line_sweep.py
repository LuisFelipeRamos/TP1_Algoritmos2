from src.event import Event
from src.line_sweep.lib.avl_tree import AVLTree
from src.segment import Segment


def invert_segments(set_of_segments: list[Segment]):
    for segment in set_of_segments:
        if segment.p0.x > segment.p1.x:
            segment.invert()


class LineSweep:
    def any_segments_intersect(self, S: list[Segment]):
        treeSegments: AVLTree = AVLTree()
        invert_segments(S)
        events: list[Event] = [
            Event(segment.p0.x, segment.p0.y, True, segment) for segment in S
        ]
        events.extend(
            Event(segment.p1.x, segment.p1.y, False, segment) for segment in S
        )
        events.sort()
        for e in events:
            if e.isLeft:
                s = e.segment
                # FIXME: Consertar inserção. Usar um comparador baseado na altura
                # da interseção com a reta de eventos
                treeSegments.insert(s)
                above = treeSegments.above(s)
                below = treeSegments.below(s)
                if (
                    above != None
                    and s.intersects(above.val.segment)
                    or below != None
                    and s.intersects(below.val.segment)
                ):
                    return True
            else:
                s = e.segment
                above = treeSegments.above(s)
                below = treeSegments.below(s)
                if (
                    above != None
                    and below != None
                    and above.val.segment.intersects(below.val.segment)
                ):
                    return True
                treeSegments.delete(s)
        return False
