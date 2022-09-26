class Segment():
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        """ ver nome melhor pra esses atributos aqui embaixo"""
        self.x = p1.x - p0.x
        self.y = p1.y - p0.y

    def __str__(self):
        return f"<{self.x}, {self.y}>"

    def cross_product(self, s):
        result = self.x*s.y - self.y*s.x
        return result
    
    def is_counter_clockwise(self, s):
        aux_segment = Segment(s.p0, self.p1)
        return self.cross_product(aux_segment) < 0
