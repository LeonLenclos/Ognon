"""This module provide control functions to draw on cells"""

from ..model import Line

def clear(cursor):
    cursor.get_element().lines = []

# OLD =>
# def use_tool(cursor, tool, *args):
#     globals()[tool](cursor, *args)

def draw(cursor, x1, y1, x2, y2):
    cursor.get_element().lines.append(Line(x1, y1, x2, y2))

def erease(cursor, x1, y1, x2, y2):
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
        if intersect(l, Line(x1, y1, x2, y2)):
            del cursor.get_element().lines[i]
            continue
