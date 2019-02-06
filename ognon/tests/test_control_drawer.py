from ..control import drawer
from .. import model
def test_draw(cursor):

	assert drawer.draw(cursor, [0,0,100,100]) is None
	assert cursor.get_element().lines[0].coords == [0,0,100,100]
	assert drawer.draw(cursor, [100,100,100,0]) is None
	assert drawer.draw(cursor, [50,50,50,10,50,100]) is None
	assert cursor.get_element().lines[0].coords == [0,0,100,100,100,0]
	assert cursor.get_element().lines[1].coords == [50,50,50,10,50,100]

def test__distance():
	assert drawer._distance((0,0),(0,10)) == 10
	assert drawer._distance((0,0),(0,0)) == 0
	assert drawer._distance((0,0),(3,4)) == 5
	assert drawer._distance((100,100),(100,150)) == 50

def test__pairwise():
	assert list(drawer._pairwise([0,1,2,3,4,5])) == [(0,1), (2,3), (4,5)]

def test_erease(cursor):
	cursor.get_element().lines = []
	
	cursor.get_element().lines.append(model.Line([0,0,100,100]))
	assert drawer.erease(cursor, (100,105), radius=10) is None
	assert len(cursor.get_element().lines) == 0

	cursor.get_element().lines.append(model.Line([0,0,100,100]))
	assert drawer.erease(cursor, (100,150), radius=10) is None
	assert len(cursor.get_element().lines) == 1

def test_clear(cursor):
	cursor.get_element().lines.append(model.Line([0,0,100,100]))
	assert drawer.clear(cursor) is None
	assert len(cursor.get_element().lines) == 0
