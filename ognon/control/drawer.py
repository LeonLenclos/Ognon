"""This module provide control functions to draw on cells"""
import math

from .. import model

def clear(cursor):
    cursor.get_element().lines = []

# OLD =>
# def use_tool(cursor, tool, *args):
#     globals()[tool](cursor, *args)

def draw(cursor, coords):
    e = cursor.get_element()
    try:
        assert e.lines[-1].coords[-2:] == coords[:2]
        e.lines[-1].coords.extend(coords[2:])
    except (AssertionError, IndexError):
        e.lines.append(model.Line(coords))


def erease(cursor, coords, radius=5):
    """
    erease the first line in the current Cell that has a point in a distance
    from `coords` lower than `radius`
    """
    for i, l in enumerate(cursor.get_element().lines):
        for point in _pairwise(l.coords):
            if _distance(coords, point):
                del cursor.get_element().lines[i]
                return

def _distance(p0, p1):
    """Return the distance between two points."""
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def _pairwise(iterable):
    """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
    a = iter(iterable)
    return zip(a, a)