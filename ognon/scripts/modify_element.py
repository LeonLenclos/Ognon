"""
This module contain bunch of stateless functions used to modify elements.
They all takes a :class:`Element` object as first argument.
"""

def move(e, x=0, y=0):
    """Move the element lines"""
    for l in e.lines:  
        l.coords = [(c+x if not i%2 else c+y) for (i, c) in enumerate(l.coords)]

def xsym(e):
    """Do a x symmetry on element"""
    for l in e.lines:  
        l.coords = [(0-c+3000 if not i%2 else c) for (i, c) in enumerate(l.coords)]

def ysym(e):
    """Do a y symmetry"""
    for l in e.lines:  
        l.coords = [(0-c+3000 if i%2 else c) for (i, c) in enumerate(l.coords)]

def scale(e, factor):
    """Scale the elemnent by a factor"""
    for l in e.lines:  
        l.coords = [int(c*factor) for c in l.coords]