from src.event import Event
from src.line_sweep.lib.avl_tree import AVLTree
from src.segment import Segment


def invert_segments(set_of_segments: list[Segment]):
    for segment in set_of_segments:
        if segment.p0.x > segment.p1.x:
            segment.invert()


class LineSweep:
    def any_segments_intersect(self, poly1: list[Segment], poly2: list[Segment]):
        treeSegments: AVLTree = AVLTree()
        invert_segments(poly1)
        invert_segments(poly2)
        events: list[Event] = [
            Event(segment.p0.x, segment.p0.y, True, segment) for segment in poly1
        ]
        events.extend(
            Event(segment.p1.x, segment.p1.y, False, segment) for segment in poly1
        )
        events.extend(
            Event(segment.p0.x, segment.p0.y, True, segment) for segment in poly2
        )
        events.extend(
            Event(segment.p0.x, segment.p0.y, True, segment) for segment in poly2
        )
        events.sort()
        for e in events:
            if e.isLeft:
                s: Segment = e.segment
                # FIXME: Consertar inserção. Usar um comparador baseado na altura
                # da interseção com a reta de eventos
                treeSegments.insert(s)
                node = treeSegments.search(s)
                above = None
                below = None
                if node != None:
                    above = node.right
                    below = node.left
                if above == None and node != None:
                    if node.parent != None:
                        if node.parent.left == node:
                            above = node.parent
                if below == None and node != None:
                    if node.parent != None:
                        if node.parent.right == node:
                            below = node.parent
                if (
                    above != None
                    and s.intersects(above.val)
                    or below != None
                    and s.intersects(below.val)
                ):
                    return True
            else:
                s = e.segment
                node = treeSegments.search(s)
                above = None
                below = None
                if node != None:
                    above = node.right
                    below = node.left
                if above != None and below != None and above.val.intersects(below.val):
                    return True
                treeSegments.delete(s)
        return False
