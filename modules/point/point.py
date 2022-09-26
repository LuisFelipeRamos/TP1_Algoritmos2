class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __lt__(self, other):
        return self.y < other.y if self.y != other.y else self.x < other.x
    

    