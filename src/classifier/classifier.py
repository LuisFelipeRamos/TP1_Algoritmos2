from numpy import Inf
from sklearn.metrics import f1_score, precision_score, recall_score

from src.convex_hull import ConvexHull
from src.point.point import Point
from src.segment import Segment


class Classifier:
    def __init__(self, class1: ConvexHull, class2: ConvexHull):
        self.class1 = class1
        self.class2 = class2

        self.slope, self.coef, self.mid_point = self.fit()

        if self.slope != Inf:
            # Se o primeiro ponto da classe 1 estiver em cima da reta, a classe 1 que é maior
            if class1.set_of_points[0].y > (
                class1.set_of_points[0].x * self.slope + self.coef
            ):
                self.class_gt = 1
                self.class_lt = 2
            else:
                self.class_gt = 2
                self.class_lt = 1
        else:
            # Quando a reta é vertical, quem está mais a direita é maior
            if class1.set_of_points[0].x > self.coef:
                self.class_gt = 1
                self.class_lt = 2
            else:
                self.class_gt = 2
                self.class_lt = 1

    def __repr__(self) -> str:
        return f"[{self.fit()}]"

    def fit(self):
        """
        Pegue a reta de classificação.
        """
        min_dist_segment: Segment = self.class1.min_dist(self.class2)
        return min_dist_segment.get_perpendicular_segment()

    def test(self, data: list[Point]) -> list[int]:
        """
        Classifique um conjunto de pontos.
        """
        result = []
        for i in data:
            if self.slope != Inf:
                if i.y > i.x * self.slope + self.coef:
                    result.append(self.class_gt)
                else:
                    result.append(self.class_lt)
            else:
                if i.x > self.coef:
                    result.append(self.class_gt)
                else:
                    result.append(self.class_lt)
        return result

    def get_statistics(self, actual: list[int], prediction: list[int]) -> None:
        """
        Colete as estatísticas a partir de dois conjuntos de dados.
        """
        f_1 = f1_score(actual, prediction)
        precision = precision_score(actual, prediction)
        recall = recall_score(actual, prediction)
        print(f"precisão: {precision}, revocação: {recall}, f1-escore: {f_1}")
