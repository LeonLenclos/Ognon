class OgnObject():
    pass


class Anim(OgnObject):
    def __init__(self):
        self.layers = [Layer()]

    def __getstate__(self):
        state = self.__dict__
        return state

    def __len__(self):
        """Renvoie len(self)
        La longueur du film"""
        return len(max(self.layers, key=len))

    def __str__(self):
    	return 'anim'

class Layer():
    def __init__(self):
        self.frms = [Cell()]

    def __getstate__(self):
        state = self.__dict__
        return state

    def __len__(self):
        # TODO: Implement it
        return len(self.frms)


class Tag(OgnObject):
    OPEN = 1
    CLOSE = 0
    def __init__(self, name, value, orientation):
        """Init a tag with a name, value and orientation"""
        self.name = name
        self.value = value
        self.orientation = orientation

    def __len__(self):
        return 0

    def __str__(self):
        return 'tag'



class Cell(OgnObject):
    def __init__(self):
        self.lines = []

    def __getstate__(self):
        state = self.__dict__
        return state

    def __len__(self):
        return 1

    def __str__(self):
    	return 'cell'

class Line():
    def __init__(self):
        self.points = []

    def __getstate__(self):
        state = self.__dict__
        return state

    def get_data(self):
    	return [point.get_data() for point in self.points]


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_data(self):
    	return {'x':self.x, 'y':self.y}

def eg():
	anim = Anim()
	for i in range(1,10):
		line = Line()
		line.points.append(Point(0,0))
		line.points.append(Point(10*i,50))
		cell = Cell()
		cell.lines.append(line)
		anim.layers[0].append(cell)
	return anim