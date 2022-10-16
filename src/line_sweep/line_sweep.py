# pylint: disable=missing-module-docstring
from src.line_sweep.event import Event
from src.line_sweep.lib.avl_tree import AVLTree
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
        para descartar intereseções de um polígono com ele mesmo.
        """

        # Inverte os segmentos para pode inseri-los mais facilmente na lista de eventos
        self.invert_segments([segment for segment, _ in polygons])

        events: list[Event] = [
            Event(segment.p0, True, segment, id) for segment, id in polygons
        ]
        events.extend(Event(segment.p1, False, segment, id) for segment, id in polygons)
        events.sort()

        tree_segments: AVLTree = AVLTree()

        # Alguma variáveis não podem ser tipadas porque a biblioteca de AVL não é tipada
        for event in events:

            # O python dá chilique quando se usa pares, então usa-se uma classe
            # para facilitar a comparação
            segment: SegmentId = SegmentId(event.segment, event.identifier)

            if event.is_left:
                tree_segments.insert(segment)
                node = tree_segments.search(segment)
                above, below = self.get_above_and_below(node, tree_segments)

                # Não basta que um segmento intesecte outro,
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

    def get_above_and_below(self, node, tree: AVLTree):
        """
        Função auxiliar para determinar os nós que estão em cima (menor maior)
        ou em baixo (maior menor) de um dado nó em uma árvore

        Como essa função só é usada na varredura linear e para evitar alterações na biblioteca,
        averigou-se adequado manter a função nesta classe
        """
        above = None
        below = None
        if node is not None:
            # Assume-se que os nós de cima e de baixo estão, na subárvore que começa no pai
            # O segmento que melhor aproxima o atual por BAIXO é o MAIOR da sub-árvore da esquerda
            # O maior da esquerda é o "menor maior" da sub-árvore
            if node.left is not None:
                below = tree.findBiggest(node.left)
            # O segmento que melhor aproxima o atual por CIMA é o MENOR da sub-árvore da direita
            # O menor da direita é o "maior menor" da sub-árvore
            if node.right is not None:
                above = tree.findSmallest(node.right)
            if node.parent is not None:
                # Existe a possibilidade de o superior (above) ser nulo
                # e o nodo em questão ser o filho da esquerda (menor que o pai)
                #
                # Como não existe ninguém maior que o nodo na sua sub-árvore da direita
                # o maior mais próximo é seu pai
                #
                #       7
                #      / \
                #    *4 NULL
                #    / \
                #   3 NULL
                #
                # Árvore não balanceada a título de ilustração
                if node.parent.left == node and above is None:
                    above = node.parent
                # Similarmente, é possível considerar o caso análogo: inferior (below) ser nulo
                # e ser o filho da direita (maior que o pai), logo o menor mais próximo é o pai
                #
                #       7
                #      / \
                #    NULL 9*
                #        / \
                #      NULL 11
                #
                # Árvore não balanceada a título de ilustração
                if node.parent.right == node and below is None:
                    below = node.parent
        return above, below

    def invert_segments(self, set_of_segments: list[Segment]) -> None:
        """
        Função auxiliar para inserir os pontos da esquerda do segmento antes
        """
        for segment in set_of_segments:
            if segment.p0.x > segment.p1.x:
                segment.invert()
