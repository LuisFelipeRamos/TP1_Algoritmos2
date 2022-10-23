# pylint: skip-file
# flake8: noqa
from __future__ import annotations

import math
import random
from typing import cast

import matplotlib.pyplot as plt

X = -math.inf


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __lt__(self, other: Point) -> bool:
        return self.y < other.y if self.y != other.y else self.x < other.x

    def __gt__(self, other: Point) -> bool:
        return self.y > other.y if self.y != other.y else self.x > other.x

    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: Point) -> bool:
        return self.x != other.x or self.y != other.y

    def get_distance(self, other: Point) -> float:
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def is_inside(self, polygon: list) -> bool:
        """Confere se um ponto está dentro de um polígono."""
        crossings: int = 0
        for edge in polygon:
            cond1: bool = edge.p0.x <= self.x and self.x < edge.p1.x
            cond2: bool = edge.p1.x <= self.x and self.x < edge.p0.x
            above: bool = self.y < (edge.slope * (self.x - edge.p0.x) + edge.p0.y)
            if (cond1 or cond2) and above:
                crossings += 1
        return (crossings % 2) != 0


class Segment:
    def __init__(self, p0: Point, p1: Point) -> None:
        self.p0 = p0
        self.p1 = p1

        self.x = p1.x - p0.x
        self.y = p1.y - p0.y

        self.slope = (
            (self.p1.y - self.p0.y) / (self.p1.x - self.p0.x)
            if self.p1.x != self.p0.x
            else 0
        )

        self.linear = self.p0.y - self.slope * self.p0.x

        self.length = self.p0.get_distance(p1)

    def __repr__(self) -> str:
        return f"[{self.p0}, {self.p1}]"

    def __lt__(self, other: Segment) -> bool:
        return not self.is_counter_clockwise(other)

    def __gt__(self, other: Segment) -> bool:
        """Comparador usado na AVL (LineSweep)."""
        y_self = self.slope * X + self.linear
        y_other = other.slope * X + other.linear
        return y_self < y_other

    def __eq__(self, other: Segment) -> bool:
        y_self = self.slope * X + self.linear
        y_other = other.slope * X + other.linear
        return y_self == y_other

    def __ge__(self, other: Segment) -> bool:
        return self > other or self == other

    def cross_product(self, other: Segment) -> float:
        return self.x * other.y - self.y * other.x

    def is_colinear(self, other: Segment) -> bool:
        return self.cross_product(other) == 0

    def is_counter_clockwise(self, other: Segment) -> bool:
        if self.is_colinear(other):
            return self.length < other.length
        return self.cross_product(other) < 0

    def get_inverse(self) -> Segment:
        return Segment(self.p1, self.p0)

    def invert(self) -> None:
        """
        Inverte os pontos de um segmento
        Não troca outros membros da classe.
        """
        self.p0, self.p1 = self.p1, self.p0

    def contains(self, point: Point) -> bool:
        """
        Confere se um ponto está no intervalo aberto do segmento
        """
        return (
            point.x <= max(self.p0.x, self.p1.x)
            and point.x >= min(self.p0.x, self.p1.x)
            and point.y <= max(self.p0.y, self.p1.y)
            and point.y >= min(self.p0.y, self.p1.y)
        )

    def orientation(self, point: Point) -> int:
        """
        Checa se um ponto é colinear, está orientado no sentido horário ou anti-horário
        """
        key: float = (self.p1.y - self.p0.y) * (point.x - self.p1.x) - (
            self.p1.x - self.p0.x
        ) * (point.y - self.p1.y)
        if key > 0:
            return 1
        if key < 0:
            return -1
        return 0

    def intersects(self, other: Segment) -> bool:
        """
        Confere se um segmento intersecta outro
        """
        d_1: int = self.orientation(other.p0)
        d_2: int = self.orientation(other.p1)
        d_3: int = other.orientation(self.p0)
        d_4: int = other.orientation(self.p1)

        if d_1 != d_2 and d_3 != d_4:
            return True

        if d_1 == 0 and self.contains(other.p0):
            return True

        if d_2 == 0 and self.contains(other.p1):
            return True

        if d_3 == 0 and other.contains(self.p0):
            return True

        if d_4 == 0 and other.contains(self.p1):
            return True

        return False

    def get_perpendicular_segment(self) -> tuple[float, float, Point]:
        negative_inverse_slope: float = -1 / self.slope if self.slope != 0 else 0
        midpoint: Point = Point(
            (self.p0.x + self.p1.x) / 2, (self.p0.y + self.p1.y) / 2
        )
        linear: float = midpoint.y - negative_inverse_slope * midpoint.x
        return negative_inverse_slope, linear, midpoint


class ConvexHull:
    def __init__(self, set_of_points: list[Point], alg: str) -> None:
        self.set_of_points = set_of_points
        self.alg = alg
        self.num_of_vertexes = 0
        if self.alg == "gift_wrapping":
            self.convex_hull = self.generate_through_gift_wrapping_alg()
        elif self.alg == "graham_scan":
            self.convex_hull = self.generate_through_graham_scan_alg()
        elif self.alg == "incremental":
            self.convex_hull = self.generate_through_incremental_alg()
        else:
            print("I don't know this alg...")

    def generate_through_gift_wrapping_alg(self) -> list[Segment]:
        anchor: Point = min(self.set_of_points)
        curr_anchor: Point = anchor
        dst: Point = (
            self.set_of_points[0]
            if self.set_of_points[0] != anchor
            else self.set_of_points[1]
        )
        curr_hull_edge: Segment = Segment(anchor, dst)
        convex_hull: list[Segment] = []
        while dst != anchor:
            dst = (
                self.set_of_points[0]
                if self.set_of_points[0] != curr_anchor
                else self.set_of_points[1]
            )
            for point in self.set_of_points:
                if point == curr_anchor or point == dst:
                    continue
                possible_hull_edge: Segment = Segment(curr_anchor, point)
                if curr_hull_edge.is_counter_clockwise(possible_hull_edge):
                    curr_hull_edge = possible_hull_edge
                    dst = point
            convex_hull.append(curr_hull_edge)
            self.num_of_vertexes += 1
            curr_anchor = dst
            curr_hull_edge = Segment(
                curr_anchor,
                self.set_of_points[0]
                if self.set_of_points[0] != curr_anchor
                else self.set_of_points[1],
            )
        return convex_hull

    def generate_through_graham_scan_alg(self) -> list[Segment]:
        anchor: Point = min(self.set_of_points)
        anchor_to_points_segments: list[Segment] = []
        convex_hull: list[Segment] = []
        for point in self.set_of_points:
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
            possible_hull_edge: Segment = Segment(
                points_ordered_by_polar_angle[i], points_ordered_by_polar_angle[i + 1]
            )
            if possible_hull_edge.is_counter_clockwise(convex_hull[-1]):
                convex_hull.append(possible_hull_edge)
                curr_point = points_ordered_by_polar_angle[i + 1]
                i += 1
            else:
                del convex_hull[-1]
                del points_ordered_by_polar_angle[i]
                i -= 1
        return convex_hull

    def generate_through_incremental_alg(self) -> list[Segment]:

        self.set_of_points.sort(key=lambda point: (point.x, point.y))

        lower_hull: list[Segment] = []
        upper_hull: list[Segment] = []

        anchor_to_next: Segment = Segment(self.set_of_points[0], self.set_of_points[1])
        anchor_to_next_next: Segment = Segment(
            self.set_of_points[0], self.set_of_points[2]
        )
        if anchor_to_next.is_counter_clockwise(anchor_to_next_next):
            s0: Segment = Segment(self.set_of_points[0], self.set_of_points[2])
            s1: Segment = Segment(self.set_of_points[2], self.set_of_points[1])
            s2: Segment = Segment(self.set_of_points[1], self.set_of_points[0])
        else:
            s0: Segment = Segment(self.set_of_points[0], self.set_of_points[1])
            s1: Segment = Segment(self.set_of_points[1], self.set_of_points[2])
            s2: Segment = Segment(self.set_of_points[2], self.set_of_points[0])
        lower_hull.append(s0)
        upper_hull.append(s1)
        upper_hull.append(s2)
        hull_farest_right_point: Point = lower_hull[-1].p1
        for point in self.set_of_points[3:]:

            hull_farest_right_point_to_new_point: Segment = Segment(
                hull_farest_right_point, point
            )
            if hull_farest_right_point_to_new_point.is_counter_clockwise(
                lower_hull[-1]
            ):
                lower_point: Point = upper_hull[0].p0
                upper_point: Point = upper_hull[0].p1
                del upper_hull[0]

            else:
                lower_point: Point = lower_hull[-1].p0
                upper_point: Point = lower_hull[-1].p1
                del lower_hull[-1]

            lower_hull.append(Segment(lower_point, point))
            upper_hull = [Segment(point, upper_point)] + upper_hull
            hull_farest_right_point = lower_hull[-1].p1

            while len(upper_hull) >= 2 and not upper_hull[1].is_counter_clockwise(
                upper_hull[0]
            ):
                new_edge_p0: Point = upper_hull[0].p0
                new_edge_p1: Point = upper_hull[1].p1
                del upper_hull[0:2]
                upper_hull = [Segment(new_edge_p0, new_edge_p1)] + upper_hull
            while len(lower_hull) >= 2 and not lower_hull[-1].is_counter_clockwise(
                lower_hull[-2]
            ):
                new_edge_p0: Point = lower_hull[-2].p0
                new_edge_p1: Point = lower_hull[-1].p1
                del lower_hull[-1:-3:-1]
                lower_hull.append(Segment(new_edge_p0, new_edge_p1))

        convex_hull: list[Segment] = lower_hull + upper_hull
        return convex_hull

    def plot(self) -> None:
        _, ax = plt.subplots()
        ax = cast(plt.Axes, ax)
        ax.scatter(
            [point.x for point in self.set_of_points],
            [point.y for point in self.set_of_points],
            c=["k"],
            s=2,
        )
        ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
        for edge in self.convex_hull:
            plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], "k", linewidth=0.5)
        plt.savefig("envoltória.png")

    def is_inside(self, other: ConvexHull) -> bool:
        """
        Checa se `other` está dentro de `self`, dado que os polígonos não se interceptam
        """
        # Se um polígono não intersecta outro,
        # então para um estar contido no outro basta que um ponto esteja.
        point: Point = other.convex_hull[0].p0
        return point.is_inside(self.convex_hull)

    def min_dist(self, other: ConvexHull) -> Segment:
        """
        Retorna o segmento de menor distância entre duas envoltórias convexas.
        """
        points_hull_1: list[Point] = [edge.p0 for edge in self.convex_hull]
        points_hull_2: list[Point] = [edge.p0 for edge in other.convex_hull]
        min_dist: float = float("inf")
        min_dist_segment: Segment = Segment(Point(0, 0), Point(0, 0))
        for p in points_hull_1:
            for q in points_hull_2:
                curr_dist: float = p.get_distance(q)
                if curr_dist < min_dist:
                    min_dist = curr_dist
                    min_dist_segment = Segment(p, q)
        return min_dist_segment


class Event:
    """
    Esta classe tem dois propósitos:
        1. Evitar o uso de tuplas, provendo acesso direto aos membros com nomes mais descritivos
        2. Prover um comparador para os eventos, levando em consideração coordenadas e orientação
    """

    def __init__(self, point: Point, left: bool, seg: Segment, i: int = -1) -> None:
        self.x = point.x
        self.y = point.y
        self.is_left = left
        self.segment = seg
        self.identifier = i

    def __repr__(self) -> str:
        return f"[({self.x}, {self.y}, {self.is_left})]"

    def compare(self, other: Event) -> int:
        """
        Compare inicialmente pelo x,
        use orientação como critério de desempate (esquerda é menor),
        use y como segundo critério de desempate
        """
        if self.x < other.x:
            return -1
        if self.x == other.x and self.is_left is True and other.is_left is False:
            return -1
        if self.x == other.x and self.is_left is False and other.is_left is True:
            return 1
        if self.x == other.x and self.y < other.y:
            return -1
        if self.x == other.x and self.y == other.y:
            return 0
        return 1

    def __lt__(self, other: Event) -> bool:
        return self.compare(other) < 0


class LineSweep:
    """
    Esta classe implementa uma versão modificada da varredura linear
    para buscar pela interseção de dois ou mais polígonos
    """

    def do_polygons_intersect(
        self, polygon1: list[Segment], polygon2: list[Segment]
    ) -> bool:
        """
        Confere se um conjunto de polígonos se possui alguma interseção entre pelo menos 2 polígonos
        Cada polígono é uma lista de tuplas (Segmento, ID). Todos os segmentos são buscados
        para verificar a interseção, de modo que a flag ID é usada
        para descartar interseções de um polígono com ele mesmo.
        """

        polygons: list[tuple[Segment, int]] = [(segment, 1) for segment in polygon1]
        polygons.extend((segment, 2) for segment in polygon2)

        # Inverte os segmentos para pode inseri-los mais facilmente na lista de eventos
        for segment, _ in polygons:
            if segment.p0.x > segment.p1.x:
                segment.invert()

        events: list[Event] = [
            Event(segment.p0, True, segment, id) for segment, id in polygons
        ]
        events.extend(Event(segment.p1, False, segment, id) for segment, id in polygons)
        events.sort()

        tree_segments: AVLTree = AVLTree()
        eps: float = 0.000001

        # Alguma variáveis não podem ser tipadas porque a biblioteca de AVL não é tipada
        for event in events:

            # O python dá chilique quando se usa pares, então usa-se uma classe
            # para facilitar a comparação
            segment_id: tuple[Segment, int] = (event.segment, event.identifier)

            if event.is_left:
                X = segment_id[0].p0.x + eps
                tree_segments.insert(segment_id)
                node = tree_segments.search(segment_id)
                if node is not None:
                    above, below = self.get_above_and_below(node, tree_segments)

                    # Não basta que um segmento intercepte outro,
                    # é necessário que eles sejam de polígonos diferentes,
                    # ou seja, é preciso conferir os identificadores
                    if (
                        above is not None
                        and segment_id[0].intersects(above.val[0])
                        and segment_id[1] != above.val[1]
                    ):
                        return True
                    if (
                        below is not None
                        and segment_id[0].intersects(below.val[0])
                        and segment_id[1] != below.val[1]
                    ):
                        return True
            else:
                node = tree_segments.search(segment_id)
                if node is not None:
                    above, below = self.get_above_and_below(node, tree_segments)

                    if (
                        above is not None
                        and below is not None
                        and above.val[0].intersects(below.val[0])
                        and above.val[1] != below.val[1]
                    ):
                        return True

                tree_segments.delete(segment_id)
        return False

    def get_above_and_below(self, node: AVLNode, tree: AVLTree):
        """
        Função auxiliar para determinar os nós que estão em cima (menor maior)
        ou em baixo (maior menor) de um dado nó em uma árvore

        Como essa função só é usada na varredura linear e para evitar alterações na biblioteca,
        averiguou-se adequado manter a função nesta classe
        """
        above = None
        below = None
        # O segmento que melhor aproxima o atual por BAIXO é o MAIOR da subárvore da esquerda
        # (quando ela existe)
        if node.left is not None:
            below = tree.findBiggest(node.left)
        # O segmento que melhor aproxima o atual por CIMA é o MENOR da subárvore da direita
        # (quando ela existe)
        if node.right is not None:
            above = tree.findSmallest(node.right)
        # Caso as subárvores a partir do nó não existam, é necessário olhar os ancestrais
        value = node.val
        if below is None:
            if node.parent is not None:
                node_iterator = node.parent
                while node_iterator is not None:
                    # Procura-se o primeiro ancestral menor para ser o inferior
                    if value > node_iterator.val:
                        below = node_iterator
                        break
                    node_iterator = node_iterator.parent
        if above is None:
            if node.parent is not None:
                node_iterator = node.parent
                while node_iterator is not None:
                    # Procura-se o primeiro ancestral maior para ser o superior
                    if node_iterator.val >= value:
                        above = node_iterator
                        break
                    node_iterator = node_iterator.parent
        return above, below


class AVLNode:
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    def isLeaf(self):
        return self.height == 0

    def maxChildrenHeight(self):
        if self.left and self.right:
            return max(self.left.height, self.right.height)
        elif self.left and not self.right:
            return self.left.height
        elif not self.left and self.right:
            return self.right.height
        else:
            return -1

    def balanceFactor(self):
        return (self.left.height if self.left else -1) - (
            self.right.height if self.right else -1
        )

    def __str__(self):
        return "AVLNode(" + str(self.val) + ", Height: %d )" % self.height


class AVLTree:
    def __init__(self):
        self.root = None
        self.rebalance_count = 0
        self.nodes_count = 0

    def setRoot(self, val):
        """
        Set the root value
        """
        self.root = AVLNode(val)

    def countNodes(self):
        return self.nodes_count

    def getDepth(self):
        """
        Get the max depth of the BST
        """
        if self.root:
            return self.root.height
        else:
            return -1

    def findSmallest(self, start_node):
        assert not start_node is None
        node = start_node
        while node.left:
            node = node.left
        return node

    def findBiggest(self, start_node):
        assert not start_node is None
        node = start_node
        while node.right:
            node = node.right
        return node

    def insert(self, val):
        """
        insert a val into AVLTree
        """
        if self.root is None:
            self.setRoot(val)
        else:
            self._insertNode(self.root, val)
        self.nodes_count += 1

    def _insertNode(self, currentNode, val):
        """
        Helper function to insert a value into AVLTree.
        """
        node_to_rebalance = None
        if currentNode.val > val:
            if currentNode.left:
                self._insertNode(currentNode.left, val)
            else:
                child_node = AVLNode(val)
                currentNode.left = child_node
                child_node.parent = currentNode
                if currentNode.height == 0:
                    self._recomputeHeights(currentNode)
                    node = currentNode
                    while node:
                        if node.balanceFactor() in [-2, 2]:
                            node_to_rebalance = node
                            break  # we need the one that is furthest from the root
                        node = node.parent
        else:
            if currentNode.right:
                self._insertNode(currentNode.right, val)
            else:
                child_node = AVLNode(val)
                currentNode.right = child_node
                child_node.parent = currentNode
                if currentNode.height == 0:
                    self._recomputeHeights(currentNode)
                    node = currentNode
                    while node:
                        if node.balanceFactor() in [-2, 2]:
                            node_to_rebalance = node
                            break  # we need the one that is furthest from the root
                        node = node.parent
        if node_to_rebalance:
            self._rebalance(node_to_rebalance)

    def _rebalance(self, node_to_rebalance):
        A = node_to_rebalance
        F = A.parent  # allowed to be NULL
        if A.balanceFactor() == -2:
            if A.right.balanceFactor() <= 0:
                B = A.right
                C = B.right
                assert not A is None and not B is None and not C is None
                A.right = B.left
                if A.right:
                    A.right.parent = A
                B.left = A
                A.parent = B
                if F is None:
                    self.root = B
                    self.root.parent = None
                else:
                    if F.right == A:
                        F.right = B
                    else:
                        F.left = B
                    B.parent = F
                self._recomputeHeights(A)
                self._recomputeHeights(B.parent)
            else:
                B = A.right
                C = B.left
                assert not A is None and not B is None and not C is None
                B.left = C.right
                if B.left:
                    B.left.parent = B
                A.right = C.left
                if A.right:
                    A.right.parent = A
                C.right = B
                B.parent = C
                C.left = A
                A.parent = C
                if F is None:
                    self.root = C
                    self.root.parent = None
                else:
                    if F.right == A:
                        F.right = C
                    else:
                        F.left = C
                    C.parent = F
                self._recomputeHeights(A)
                self._recomputeHeights(B)
        else:
            assert node_to_rebalance.balanceFactor() == +2
            if node_to_rebalance.left.balanceFactor() >= 0:
                B = A.left
                C = B.left
                assert not A is None and not B is None and not C is None
                A.left = B.right
                if A.left:
                    A.left.parent = A
                B.right = A
                A.parent = B
                if F is None:
                    self.root = B
                    self.root.parent = None
                else:
                    if F.right == A:
                        F.right = B
                    else:
                        F.left = B
                    B.parent = F
                self._recomputeHeights(A)
                self._recomputeHeights(B.parent)
            else:
                B = A.left
                C = B.right
                assert not A is None and not B is None and not C is None
                A.left = C.right
                if A.left:
                    A.left.parent = A
                B.right = C.left
                if B.right:
                    B.right.parent = B
                C.left = B
                B.parent = C
                C.right = A
                A.parent = C
                if F is None:
                    self.root = C
                    self.root.parent = None
                else:
                    if F.right == A:
                        F.right = C
                    else:
                        F.left = C
                    C.parent = F
                self._recomputeHeights(A)
                self._recomputeHeights(B)
        self.rebalance_count += 1

    def _recomputeHeights(self, start_from_node):
        changed = True
        node = start_from_node
        while node and changed:
            old_height = node.height
            node.height = (
                node.maxChildrenHeight() + 1 if (node.right or node.left) else 0
            )
            changed = node.height != old_height
            node = node.parent

    def search(self, key):
        """
        Search a AVLNode satisfies AVLNode.val = key.
        if found return AVLNode, else return None.
        """
        return self._dfsSearch(self.root, key)

    def _dfsSearch(self, currentNode, key):
        """
        Helper function to search a key in AVLTree.
        """
        if currentNode is None:
            return None
        elif currentNode.val == key:
            return currentNode
        elif currentNode.val > key:
            return self._dfsSearch(currentNode.left, key)
        else:
            return self._dfsSearch(currentNode.right, key)

    def delete(self, key):
        """
        Delete a key from AVLTree
        """
        # first find
        node = self.search(key)

        if not node is None:
            self.nodes_count -= 1
            #     There are three cases:
            #
            #     1) The node is a leaf.  Remove it and return.
            #
            #     2) The node is a branch (has only 1 child). Make the pointer to this node
            #        point to the child of this node.
            #
            #     3) The node has two children. Swap items with the successor
            #        of the node (the smallest item in its right subtree) and
            #        delete the successor from the right subtree of the node.
            if node.isLeaf():
                self._removeLeaf(node)
            elif (bool(node.left)) ^ (bool(node.right)):
                self._removeBranch(node)
            else:
                assert (node.left) and (node.right)
                self._swapWithSuccessorAndRemove(node)

    def _removeLeaf(self, node):
        parent = node.parent
        if parent:
            if parent.left == node:
                parent.left = None
            else:
                assert parent.right == node
                parent.right = None
            self._recomputeHeights(parent)
        else:
            self.root = None
        del node
        # rebalance
        node = parent
        while node:
            if not node.balanceFactor() in [-1, 0, 1]:
                self._rebalance(node)
            node = node.parent

    def _removeBranch(self, node):
        parent = node.parent
        if parent:
            if parent.left == node:
                parent.left = node.right if node.right else node.left
            else:
                assert parent.right == node
                parent.right = node.right if node.right else node.left
            if node.left:
                node.left.parent = parent
            else:
                assert node.right
                node.right.parent = parent
            self._recomputeHeights(parent)
        del node
        # rebalance
        node = parent
        while node:
            if not node.balanceFactor() in [-1, 0, 1]:
                self._rebalance(node)
            node = node.parent

    def _swapWithSuccessorAndRemove(self, node):
        successor = self.findSmallest(node.right)
        self._swapNodes(node, successor)
        assert node.left is None
        if node.height == 0:
            self._removeLeaf(node)
        else:
            self._removeBranch(node)

    def _swapNodes(self, node1, node2):
        assert node1.height > node2.height
        parent1 = node1.parent
        leftChild1 = node1.left
        rightChild1 = node1.right
        parent2 = node2.parent
        assert not parent2 is None
        assert parent2.left == node2 or parent2 == node1
        leftChild2 = node2.left
        assert leftChild2 is None
        rightChild2 = node2.right

        # swap heights
        tmp = node1.height
        node1.height = node2.height
        node2.height = tmp

        if parent1:
            if parent1.left == node1:
                parent1.left = node2
            else:
                assert parent1.right == node1
                parent1.right = node2
            node2.parent = parent1
        else:
            self.root = node2
            node2.parent = None

        node2.left = leftChild1
        leftChild1.parent = node2
        node1.left = leftChild2  # None
        node1.right = rightChild2
        if rightChild2:
            rightChild2.parent = node1
        if not (parent2 == node1):
            node2.right = rightChild1
            rightChild1.parent = node2
            parent2.left = node1
            node1.parent = parent2
        else:
            node2.right = node1
            node1.parent = node2

def hull():
    set_of_points: list[Point] = []
    for _ in range(100):
        x: int
        y: int
        x, y = random.randint(1, 100), random.randint(1, 100)
        set_of_points.append(Point(x, y))
    
    hull: ConvexHull = ConvexHull(set_of_points, alg="gift_wrapping")
    return hull

def plot_polygon(polygon: list[Segment], color: str):
    """
    Imprime as arestas de um polígono usando a cor `color`
    """
    for edge in polygon:
        plt.plot([edge.p0.x, edge.p1.x], [edge.p0.y, edge.p1.y], color, linewidth=0.5)

def separable():
    polygon_a = hull().convex_hull
    polygon_b = hull().convex_hull
    _, ax = plt.subplots()
    ax = cast(plt.Axes, ax)
    ax.grid(which="both", color="grey", linewidth=0.5, linestyle="-", alpha=0.2)
    plot_polygon(polygon_a, "blue")
    plot_polygon(polygon_b, "green")
    plt.savefig("polígonos.png")
    line_sweeper = LineSweep()
    return not line_sweeper.do_polygons_intersect(polygon_a,polygon_b)




if __name__ == "__main__":
    print("""O programa tem duas funções
          1. A partir de um conjunto de pontos aleatório gerar uma envoltória convexa
          2. Verificar se dois polígonos são linearmente separáveis.
          Para visualizar isso, são geradas duas figuras: envoltória.png e polígonos.png
          É impresso na tela se os polígonos são linearmente separáveis ou não.""")
    convex_hull = hull()
    convex_hull.plot()
    if separable():
        print("Polígonos são linearmente separáveis")
    else:
        print("Polígonos não são linearmente separáveis")
