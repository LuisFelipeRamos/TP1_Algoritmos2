class Segment:
    def __init__(self, p0, p1):
        self.points = p0, p1
        """ ver nome melhor pra esses atributos aqui embaixo"""
        self.x = p1.x - p0.x
        self.y = p1.y - p0.y

    def __str__(self):
        return f"<{self.points[0]}, {self.points[1]}>"

    def cross_product(self, s):
        return self.x * s.y - self.y * s.x

    def is_counter_clockwise(self, s):
        return self.cross_product(s) < 0
