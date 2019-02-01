"""This module provide control functions to draw on cells"""

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


def erease(cursor, coords):
    def intersect(line1, line2):
        A, B, C, D = (
            line1.coords[:2],
            line1.coords[2:],
            line2.coords[:2],
            line2.coords[2:],
        )
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    for i, l in enumerate(cursor.get_element().lines):
        if intersect(l, model.Line(coords)):
            del cursor.get_element().lines[i]
            continue
