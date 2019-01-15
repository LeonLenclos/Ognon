from model import Line, Point, Cell

class Drawer():
    """Allow to draw on cells"""

    def __init__(self, ognproject):
        self.ognproject = ognproject
        self.current_line = None
        self.tool = self.pen

    def set_tool(self, cursor, tool): self.tool = getattr(self, tool)

    def use_pen(self, cursor): self.set_tool(cursor, 'pen')

    def use_eraser(self, cursor): self.set_tool(cursor, 'eraser')

    def start_line(self, cursor, x, y):
        if type(cursor.get_frm()) is Cell:
            self.tool(cursor, x, y)

    def pen(self, cursor, x, y):
        if not self.current_line:
            self.current_line = Line()
            cursor.get_frm().lines.append(self.current_line)
        self.current_line.points.append(Point(x, y))

    def eraser(self, cursor, x, y):
        if not self.current_line:
            self.current_line = Line()
        self.current_line.points.append(Point(x, y))
        for i, l in enumerate(cursor.get_frm().lines):
            if intersection(self.current_line.get_data(), l.get_data()):
                del self.cursor.get_frm().lines[i]

    def eraser(self, cursor, x, y):
        if not self.current_line:
            self.current_line = Line()
        self.current_line.points.append(Point(x, y))
        for i, l in enumerate(cursor.get_frm().lines):
            if intersection(self.current_line.get_data(), l.get_data()):
                del self.cursor.get_frm().lines[i]

    def clear(self, cursor):
        if type(cursor.get_frm()) is Cell:
            cursor.get_frm().lines = []

    def end_line(self, cursor):
        self.current_line = None


def intersection(line1, line2):
    """Tell whether there is an intersection between the two Lines."""
    # A good function that I dont understand
    def intersect(A, B, C, D):
        def ccw(A, B, C):
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)
        return ccw(A, C, D) != ccw(B, C, D) \
           and ccw(A, B, C) != ccw(A, B, D)

    #for each segment of the first check each segment of the second
    for i, p1_first_point in enumerate(line1[:-1]):
        p1_second_point = line1[i + 1]

        for j, p2_first_point in enumerate(line2[:-1]):
            p2_second_point = line2[j + 1]

            if intersect(p1_first_point,
                         p1_second_point,
                         p2_first_point,
                         p2_second_point):
                return True
    return False
