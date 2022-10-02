from src.line_sweep.event import Event
from src.line_sweep.lib.avl_tree import AVLTree
from src.segment import Segment


def invert_segments(set_of_segments: list[Segment]):
    for segment in set_of_segments:
        if segment.p0.x > segment.p1.x:
            segment.invert()


class LineSweep:
    def any_segments_intersect(self, S: list[tuple[Segment, int]]):
        treeSegments: AVLTree = AVLTree()
        invert_segments([segment for segment, _ in S])
        events: list[Event] = [
            Event(segment.p0.x, segment.p0.y, True, segment, id) for segment, id in S
        ]
        events.extend(
            Event(segment.p1.x, segment.p1.y, False, segment, id) for segment, id in S
        )
        events.sort()
        for e in events:
            if e.isLeft:
                s = e.segment, e.id
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
                    and s[0].intersects(above.val[0])
                    and s[1] != above.val[1]
                    or below != None
                    and s[0].intersects(below.val[0])
                    and s[1] != below.val[1]
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
                if (
                    above != None
                    and below != None
                    and above.val[0].intersects(below[0].val)
                    and above.val[1] != above[0].val
                ):
                    return True
                treeSegments.delete(s)
        return False
