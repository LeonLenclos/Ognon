from ..control import drawer
from .. import model
def test_draw(cursor):

	assert drawer.draw(cursor, [0,0,100,100]) is None
	assert cursor.get_element().lines[0].coords == [0,0,100,100]
	assert drawer.draw(cursor, [100,100,100,0]) is None
	assert drawer.draw(cursor, [50,50,50,10,50,100]) is None
	assert cursor.get_element().lines[0].coords == [0,0,100,100,100,0]
	assert cursor.get_element().lines[1].coords == [50,50,50,10,50,100]

def test_erease(cursor):
	# erease
	cursor.get_element().lines.append(model.Line([0,0,100,100]))
	assert drawer.erease(cursor, [100,0,0,100]) is None
	assert len(cursor.get_element().lines) == 0

def test_clear(cursor):
	cursor.get_element().lines.append(model.Line([0,0,100,100]))
	assert drawer.clear(cursor) is None
	assert len(cursor.get_element().lines) == 0