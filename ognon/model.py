class Project():
    def __init__(self, name):
        self.name = name
        self.anims = {'master':Anim()}
        self.config = {}
        

class Anim():
    def __init__(self):
        self.layers = [Layer()]

class Layer():
    def __init__(self):
        self.elements = [Cell()]

class Cell():
    def __init__(self):
        self.lines = []

class AnimRef():
    def __init__(self, name):
        self.name = name

class Line():
    def __init__(self, x1, y1, x2, y2):
        self.coords = (x1, y1, x2, y2)

