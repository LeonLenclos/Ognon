from .. import control
from .. import model

class DebugCell(model.Cell):
	def __init__(self, debug):
		super().__init__()
		self.debug = debug
		
def debugs_list(cursor):
	return [c.debug if type(c) is DebugCell else None for c in cursor.get_layer().elements]

def init_orga(cursor):
	control.navigator.first_frm(cursor)
	cursor.get_layer().elements = [DebugCell(i) for i in range(5)]

def test_add_element_after(cursor):
	init_orga(cursor)
	assert control.elementsorganizer.add_element_after(cursor, DebugCell('new')) is None
	assert debugs_list(cursor) == [0,'new',1,2,3,4]
	assert cursor.get_pos('frm') == 1

	control.navigator.last_frm(cursor)
	assert control.elementsorganizer.add_element_after(cursor, DebugCell('new')) is None
	assert debugs_list(cursor) == [0,'new',1,2,3,4,'new']
	assert cursor.get_pos('frm') == 6

def test_add_element_before(cursor):
	init_orga(cursor)
	assert control.elementsorganizer.add_element_before(cursor, DebugCell('new')) is None
	assert debugs_list(cursor) == ['new',0,1,2,3,4]
	assert cursor.get_pos('frm') == 0

def test_add_cell_after_and_add_cell_before(cursor):
	assert control.elementsorganizer.add_cell_before(cursor) is None
	assert isinstance(cursor.get_element(), model.Cell)
	assert control.elementsorganizer.add_cell_after(cursor) is None
	assert isinstance(cursor.get_element(), model.Cell)

def test_add_animref_after_and_add_animref_before(cursor):
	assert control.elementsorganizer.add_animref_before(cursor, 'testing-anim') is None
	assert isinstance(cursor.get_element(), model.AnimRef)
	assert control.elementsorganizer.add_animref_after(cursor, 'testing-anim') is None
	assert isinstance(cursor.get_element(), model.AnimRef)

def test_del_element(cursor):
	init_orga(cursor)
	assert control.elementsorganizer.del_element(cursor) is None
	assert debugs_list(cursor) == [1,2,3,4]
	assert cursor.get_pos('frm') == 0
	assert control.elementsorganizer.del_element(cursor) is None
	assert debugs_list(cursor) == [2,3,4]
	assert cursor.get_pos('frm') == 0
	control.navigator.last_frm(cursor)
	assert control.elementsorganizer.del_element(cursor) is None
	assert debugs_list(cursor) == [2,3]
	assert cursor.get_pos('frm') == 1

def test_move_element_forward(cursor):
	init_orga(cursor)
	assert control.elementsorganizer.move_element_forward(cursor) is None
	assert debugs_list(cursor) == [1,0,2,3,4]
	assert cursor.get_pos('frm') == 1
	assert control.elementsorganizer.move_element_forward(cursor) is None
	assert debugs_list(cursor) == [1,2,0,3,4]
	assert cursor.get_pos('frm') == 2
	control.navigator.last_frm(cursor)
	assert control.elementsorganizer.move_element_forward(cursor) is None
	assert debugs_list(cursor) == [1,2,0,3,4]
	assert cursor.get_pos('frm') == 4

def test_move_element_backward(cursor):
	init_orga(cursor)
	assert control.elementsorganizer.move_element_backward(cursor) is None
	assert debugs_list(cursor) == [0,1,2,3,4]
	assert cursor.get_pos('frm') == 0
	control.navigator.last_frm(cursor)
	assert control.elementsorganizer.move_element_backward(cursor) is None
	assert debugs_list(cursor) == [0,1,2,4,3]
	assert cursor.get_pos('frm') == 3
	assert control.elementsorganizer.move_element_backward(cursor) is None
	assert debugs_list(cursor) == [0,1,4,2,3]
	assert cursor.get_pos('frm') == 2

def test__pop_element_at(cursor):
	element = cursor.get_layer().elements[0]
	assert control.elementsorganizer._pop_element_at(cursor, 0) is element
	assert len(cursor.get_layer().elements) == 1
