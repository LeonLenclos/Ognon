# -*-coding:Utf-8 -*


class Pencil():
    """Allow to draw on cells"""

    def __init__(self):
        """Construct a Pencil"""
        self.is_drawing = False

    def draw_tmp_line(self, line, cell):
        """Add a new line to the cell that will be deleted if the drawing
        continue"""
        if self.is_drawing:
            del cell.lines[-1]
        else:
            self.is_drawing = True
        cell.add_line(line)

    def save_line(self):
        """Finish the drawing"""
        self.is_drawing = False

    def erase(self, line, cell):
        """Delete cell's lines that intersects with the given line."""
        for i, l in enumerate(cell.lines):
            if self.intersection(line, l):
                cell.remove_line(i)
                break

    def intersection(self, poly1, poly2):
        """Tell whether there is an intersection between the two polylines."""
        # A Point class to deal with the intersect function.
        class Point():
            def __init__(self, t):
                self.x = t[0]
                self.y = t[1]

        # A good function that I dont understand
        def intersect(A, B, C, D):
            def ccw(A, B, C):
                return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)
            return ccw(A, C, D) != ccw(B, C, D) \
               and ccw(A, B, C) != ccw(A, B, D)

        #grouping lines coords two by two
        poly1 = tuple(zip(poly1[0::2], poly1[1::2]))
        poly2 = tuple(zip(poly2[0::2], poly2[1::2]))

        #for each segment of the first check each segment of the second
        for i, p1_first_point in enumerate(poly1[:-1]):
            p1_second_point = poly1[i + 1]

            for j, p2_first_point in enumerate(poly2[:-1]):
                p2_second_point = poly2[j + 1]

                if intersect(Point(p1_first_point),
                             Point(p1_second_point),
                             Point(p2_first_point),
                             Point(p2_second_point)):
                    return True
        return False
