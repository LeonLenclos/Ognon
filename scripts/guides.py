"""
Create a .ogn file with guides.
"""

from ognon import projects
from ognon.model import Cell, Line, Anim, Layer

project_name = 'to'
guide_name = 'cache'
width, height = 2048, 1080
hlines = [] # list of horizontal lines y positions
vlines = [25, width-25, 400] # list of vertical lines x positions
rectangles = [(75,50,width-75,height-75)] # list of rectangles (x1,y1,x2,y2) position


cell = Cell(lines=[
    *[Line([x, 0, x, height]) for x in vlines],
    *[Line([0, y, width, y]) for y in hlines],
    *[Line([x1, y1, x2, y1, x2, y2, x1, y2, x1, y1,])
        for x1, y1, x2, y2 in rectangles],
])

anim = Anim(layers=[Layer(elements=[cell])])

proj = projects.get(project_name)
proj.anims[guide_name] = anim
projects.save(proj)

