# pylint: disable=missing-module-docstring
import src.line_sweep.glob as gb
from src.line_sweep.event import Event
from src.line_sweep.lib.avl_tree import AVLNode, AVLTree
from src.line_sweep.segment_id import SegmentId
from src.segment import Segment


class LineSweep:
    """
    Esta classe implementa uma versão modificada da varredura linear
    para buscar pela interseção de dois ou mais polígonos
    """

    def check_polygons_intersect(self, polygons: list[tuple[Segment, int]]) -> bool:
        """
        Confere se um conjunto de polígonos se possui alguma interseção entre pelo menos 2 polígonos
        Cada polígono é uma lista de tuplas (Segmento, ID). Todos os segmentos são buscados
        para verificar a interseção, de modo que a flag ID é usada
        para descartar interseções de um polígono com ele mesmo.
        """

        # Inverte os segmentos para pode inseri-los mais facilmente na lista de eventos
        self.invert_segments([segment for segment, _ in polygons])

        events: list[Event] = [
            Event(segment.p0, True, segment, id) for segment, id in polygons
        ]
        events.extend(Event(segment.p1, False, segment, id) for segment, id in polygons)
        events.sort()

        tree_segments: AVLTree = AVLTree()
        eps = 0.000001

        # Alguma variáveis não podem ser tipadas porque a biblioteca de AVL não é tipada
        for event in events:

            # O python dá chilique quando se usa pares, então usa-se uma classe
            # para facilitar a comparação
            segment: SegmentId = SegmentId(event.segment, event.identifier)

            if event.is_left:
                gb.xxx = segment.seg.p0.x + eps
                tree_segments.insert(segment)
                node = tree_segments.search(segment)
                if node is not None:
                    above, below = self.get_above_and_below(node, tree_segments)

                    # Não basta que um segmento intercepte outro,
                    # é necessário que eles sejam de polígonos diferentes,
                    # ou seja, é preciso conferir os identificadores
                    if (
                        above is not None
                        and segment.seg.intersects(above.val.seg)
                        and segment.identifier != above.val.identifier
                    ):
                        return True
                    if (
                        below is not None
                        and segment.seg.intersects(below.val.seg)
                        and segment.identifier != below.val.identifier
                    ):
                        return True
            else:
                node = tree_segments.search(segment)
                if node is not None:
                    above, below = self.get_above_and_below(node, tree_segments)

                    if (
                        above is not None
                        and below is not None
                        and above.val.seg.intersects(below.val.seg)
                        and above.val.identifier != below.val.identifier
                    ):
                        return True

                tree_segments.delete(segment)
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
                    if node_iterator.val > value:
                        above = node_iterator
                        break
                    node_iterator = node_iterator.parent
        return above, below

    def invert_segments(self, set_of_segments: list[Segment]) -> None:
        """
        Função auxiliar para inserir os pontos da esquerda do segmento antes
        """
        for segment in set_of_segments:
            if segment.p0.x > segment.p1.x:
                segment.invert()
