"""This module provide control functions to draw on cells"""

import math

from .. import model
from . import change_project_draw_state

@change_project_draw_state
def clear(cursor):
    """Clear all the current element content."""
    cursor.get_element().lines = []

@change_project_draw_state
def draw(cursor, coords):
    """Draw a line in the current element."""
    e = cursor.get_element()
    if not hasattr(e, 'lines'): return

    if len(e.lines) and e.lines[-1].coords[-2:] == coords[:2]:
        e.lines[-1].coords.extend(coords[2:])
    else:
        e.lines.append(model.Line(coords))

@change_project_draw_state
def erease(cursor, coords, radius=5):
    """
    erease the first line in the current Cell that has a point in a distance
    from `coords` lower than `radius`.
    """
    e = cursor.get_element()
    if not hasattr(e, 'lines'): return

    for i, l in enumerate(e.lines):
        for erease_point in _pairwise(coords):
            for line_point in _pairwise(l.coords):
                if _distance(erease_point, line_point) < radius:
                    del e.lines[i]
                    return

@change_project_draw_state
def move(cursor, coords):
    """
    move all the Cell lines.
    """
    e = cursor.get_element()
    if not hasattr(e, 'lines'): return
    
    offset_x = coords[-2] - coords[0]
    offset_y = coords[-1] - coords[1]

    for i, l in enumerate(e.lines):
        for j, point in enumerate(_pairwise(l.coords)):
            e.lines[i].coords[j*2] = point[0] + offset_x
            e.lines[i].coords[j*2+1] = point[1] + offset_y

def _distance(p0, p1):
    """Return the distance between two points."""
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def _pairwise(iterable):
    """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
    a = iter(iterable)
    return zip(a, a)
