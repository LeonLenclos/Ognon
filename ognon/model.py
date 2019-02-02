"""
This module define the Ognon model

It describes every data that can be write on the disk. they are nested python
classes. With no method description.
"""

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

class Element():
    pass
    
class Cell(Element):
    def __init__(self):
        self.lines = []

class AnimRef(Element):
    def __init__(self, name):
        self.name = name

class Line():
    def __init__(self, coords):
        self.coords = coords

