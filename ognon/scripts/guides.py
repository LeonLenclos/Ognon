"""
This module contain bunch of stateless functions used to draw on elements.
They all takes a :class:`Cursor` object as first argument.
"""

from ognon.control import drawer

def hline(c, y):
    """Draw a horizontal line"""
    width = c.proj.config['view']['width']
    drawer.draw(c, [0, y, width, y])

def vline(c, x):
    """Draw a vertical line"""
    height = c.proj.config['view']['height']
    drawer.draw(c, [x, 0, x, height])

def rect(c, x1, y1, x2, y2):
    """Draw a rectangle"""
    drawer.draw(c, [x1, y1, x2, y1, x2, y2, x1, y2, x1, y1,])
